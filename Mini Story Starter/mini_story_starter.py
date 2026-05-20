import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyttsx3
import random
import threading
import queue
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',
                   handlers=[logging.FileHandler('mini_story_tts_log.txt'), logging.StreamHandler()])

words_file = 'mini_story_words_log.txt'

def get_today_words():
    try:
        with open(words_file) as f:
            w = f.read().strip().split(', ')
            return w if len(w) == 3 else force_new_words()
    except:
        return force_new_words()

def force_new_words():
    w = random.sample(['magic','forest','dragon','crystal','ancient','mystical','treasure','quest','wizard','enchanted','portal','adventure'], 3)
    with open(words_file, 'w') as f:
        f.write(', '.join(w))
    return w

def generate_stories(words, count=3):
    templates = ["{0} discovered {1} in the {2}", "A {2} guarded {1} and {0}",
                 "The {0} found {1} near {2}", "{0} and {1} explored {2}", "Beyond {2}, {0} met {1}"]
    stories = []
    for i in range(count):
        rotated = words[i % len(words):] + words[:i % len(words)]
        stories.append(templates[i % len(templates)].format(*rotated[:3]))
    return stories

class TTSWorker:
    def __init__(self):
        self.queue = queue.Queue()
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()
    
    def _worker(self):
        try:
            import comtypes
            comtypes.CoInitialize()
        except:
            try:
                import pythoncom
                pythoncom.CoInitialize()
            except:
                pass
        
        while True:
            try:
                item = self.queue.get(timeout=1)
                if item is None:
                    break
                    
                texts, callback = item
                logging.info(f"SPEAK: {len(texts)} lines")
                
                for idx, txt in enumerate(texts):
                    if self.stop_event.is_set():
                        break
                    
                    try:
                        if callback:
                            callback(idx)
                        
                        engine = pyttsx3.init()
                        engine.setProperty('rate', 150)
                        engine.setProperty('volume', 0.9)
                        engine.say(txt)
                        engine.runAndWait()
                        del engine
                        
                        logging.info(f"Done line {idx}")
                        time.sleep(1.0)
                        
                    except Exception as e:
                        logging.error(f"Line {idx} error: {e}", exc_info=True)
                
            except queue.Empty:
                pass
            except Exception as e:
                logging.error(f"Worker error: {e}", exc_info=True)
    
    def speak(self, texts, callback=None):
        self.stop_event.clear()
        self.queue.put((texts, callback))
    
    def stop(self):
        self.stop_event.set()

worker = TTSWorker()

def show_words(w=None):
    w = w or get_today_words()
    words_label.config(text=f"Your words:\n{', '.join(w)}")

def on_regen():
    show_words(force_new_words())

def on_show():
    stories = generate_stories(get_today_words(), int(count_spinbox.get()))
    stories_label.config(state='normal')
    stories_label.delete('1.0', 'end')
    for idx, s in enumerate(stories, 1):
        stories_label.insert('end', f'{idx}. {s}\n')
    stories_label.config(state='disabled')

def on_speak():
    stories_label.config(state='normal')
    text = stories_label.get('1.0', 'end').strip()
    stories_label.config(state='disabled')
    if not text:
        return
    
    stories = [s.strip() for s in text.split('\n') if s.strip()]
    status_label.config(text="Status: Speaking...", fg="green")
    
    def hl(idx):
        try:
            stories_label.config(state='normal')
            stories_label.tag_remove('hl', '1.0', 'end')
            line_num = idx + 1
            stories_label.tag_add('hl', f'{line_num}.0', f'{line_num}.end')
            stories_label.see(f'{line_num}.0')
            stories_label.config(state='disabled')
        except:
            pass
    
    worker.speak(stories, hl)
    
    def reset():
        time.sleep(len(stories) * 1.5)
        status_label.config(text="Status: Idle", fg="blue")
    
    threading.Thread(target=reset, daemon=True).start()

def on_stop():
    worker.stop()
    status_label.config(text="Status: Stopped", fg="red")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Mini Story Starter")
    root.geometry("900x650")
    
    tk.Label(root, text="Mini Story Starter", font=("Arial", 20, "bold")).pack(pady=10)
    
    f = tk.Frame(root)
    f.pack(pady=10)
    tk.Button(f, text="Get Words", command=show_words).pack(side='left', padx=3)
    tk.Button(f, text="Regen", command=on_regen).pack(side='left', padx=3)
    tk.Button(f, text="Show Stories", command=on_show).pack(side='left', padx=3)
    tk.Button(f, text="Speak", command=on_speak, bg='lightgreen').pack(side='left', padx=3)
    tk.Button(f, text="Stop", command=on_stop, bg='lightcoral').pack(side='left', padx=3)
    tk.Label(f, text="Count:").pack(side='left', padx=3)
    count_spinbox = tk.Spinbox(f, from_=1, to=20, width=2)
    count_spinbox.insert(0, '3')
    count_spinbox.pack(side='left', padx=2)
    
    status_label = tk.Label(root, text="Status: Idle", fg="blue")
    status_label.pack()
    
    words_label = tk.Label(root, text="", font=("Arial", 11, "bold"), fg="green")
    words_label.pack(pady=5)
    
    sf = tk.Frame(root)
    sf.pack(fill='both', expand=True, padx=10, pady=10)
    stories_label = scrolledtext.ScrolledText(sf, height=18, width=90, state='disabled', wrap='word')
    stories_label.pack(fill='both', expand=True)
    stories_label.tag_config('hl', background='yellow')
    
    show_words()
    root.mainloop()