import tkinter as tk
import sounddevice as sd
import numpy as np
import random
import traceback
from queue import Queue, Empty

# Default settings
CLAP_THRESHOLD = 0.02  # default sensitivity (lower value = more sensitive)
DURATION = 0.1  # seconds per audio sample (used for blocksize suggestion)
SAMPLERATE = 44100

colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "cyan"]

# Globals set in main
root = None
threshold_var = None
level_label = None
device_var = None
_stream = None
_level_queue = Queue(maxsize=10)


def _audio_callback(indata, frames, time, status):
    """Called in a background thread by sounddevice; push RMS level to the queue."""
    try:
        if status:
            # Non-fatal status information
            print('InputStream status:', status)
        # indata is shape (frames, channels); use first channel
        if indata.size == 0:
            return
        samples = indata[:, 0].astype(float)
        rms = float(np.sqrt(np.mean(samples * samples)))
        try:
            _level_queue.put_nowait(rms)
        except Exception:
            # drop if queue full
            pass
    except Exception:
        traceback.print_exc()


def _poll_queue():
    """Called on the Tk main thread to consume audio levels and update GUI."""
    global root, threshold_var, level_label
    try:
        while True:
            level = _level_queue.get_nowait()
            if level_label is not None:
                level_label.config(text=f"Level: {level:.4f}")
            threshold = threshold_var.get() if threshold_var is not None else CLAP_THRESHOLD
            if level > threshold:
                new_color = random.choice(colors)
                if root is not None:
                    root.config(bg=new_color)
    except Empty:
        pass
    finally:
        if root is not None:
            root.after(50, _poll_queue)


def _start_stream(device=None):
    """Start sounddevice InputStream in non-blocking mode."""
    global _stream
    try:
        if _stream is not None:
            _stream.close()
            _stream = None
        # Choose a sensible blocksize: number of frames per callback
        blocksize = int(SAMPLERATE * DURATION)
        _stream = sd.InputStream(samplerate=SAMPLERATE, channels=1, callback=_audio_callback,
                                 blocksize=blocksize, device=device)
        _stream.start()
    except Exception:
        traceback.print_exc()
        _stream = None


def _stop_stream():
    global _stream
    try:
        if _stream is not None:
            _stream.stop()
            _stream.close()
            _stream = None
    except Exception:
        traceback.print_exc()
        _stream = None


def build_gui():
    global root, threshold_var, level_label, device_var
    root = tk.Tk()
    root.title("Sound Color Mapper")
    root.geometry("600x320")
    root.config(bg="white")

    title_label = tk.Label(root, text="Sound Color Mapper", font=("Arial", 18, "bold"), bg="white")
    title_label.pack(pady=(12, 6))

    instructions = tk.Label(root, text="Clap or make a short loud sound to change the color.", bg="white")
    instructions.pack(pady=(0, 12))

    # Device selector
    dev_frame = tk.Frame(root, bg='white')
    dev_frame.pack(fill='x', padx=20)
    tk.Label(dev_frame, text='Input device:', bg='white').pack(side='left')

    device_var = tk.StringVar(value='default')
    device_menu = tk.OptionMenu(dev_frame, device_var, 'default')
    device_menu.pack(side='left', padx=(6,0))

    # Populate devices
    try:
        devices = sd.query_devices()
        input_devices = [(i, d) for i, d in enumerate(devices) if d['max_input_channels'] > 0]
        menu = device_menu['menu']
        menu.delete(0, 'end')
        menu.add_command(label='default', command=lambda: device_var.set('default'))
        for idx, d in input_devices:
            label = f"{idx}: {d['name']}"
            menu.add_command(label=label, command=lambda v=idx: device_var.set(str(v)))
    except Exception:
        traceback.print_exc()

    # Threshold slider
    threshold_var = tk.DoubleVar(value=CLAP_THRESHOLD)
    slider = tk.Scale(root, from_=0.0, to=1.0, resolution=0.001, orient=tk.HORIZONTAL,
                      label='Sensitivity (lower = more sensitive)', variable=threshold_var)
    slider.pack(fill='x', padx=20, pady=(10,0))

    # Level display
    level_label = tk.Label(root, text="Level: 0.0000", bg="white")
    level_label.pack(pady=8)

    # Start polling queue
    root.after(50, _poll_queue)

    return root


def on_device_change(*args):
    """Called when device selection changes; restart stream with the selected device."""
    global device_var
    val = device_var.get()
    if val == 'default':
        device = None
    else:
        try:
            device = int(val)
        except Exception:
            device = None
    _stop_stream()
    _start_stream(device=device)


def on_close():
    _stop_stream()
    if root is not None:
        root.destroy()


def main():
    # Build GUI but do not start stream until after GUI is ready
    app = build_gui()

    # Wire up device_var trace now that it's created
    try:
        device_var.trace_add('write', on_device_change)
    except Exception:
        try:
            device_var.trace('w', on_device_change)
        except Exception:
            pass

    # Start stream with default device
    _start_stream()

    # Ensure stream stops on close
    app.protocol('WM_DELETE_WINDOW', on_close)
    app.mainloop()


if __name__ == '__main__':
    main()
