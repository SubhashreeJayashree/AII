import tkinter as tk
from tkinter import messagebox
import random

# Pet sounds mapping with animal emojis
pet_sounds = {
    "Dog": ("woof woof", "🐕"),
    "Cat": ("meow meow", "🐱"),
    "Cow": ("moo moo", "🐄"),
    "Sheep": ("baa baa", "🐑"),
    "Pig": ("oink oink", "🐷"),
    "Duck": ("quack quack", "🦆"),
    "Chicken": ("cluck cluck", "🐔"),
    "Horse": ("neigh neigh", "🐴"),
    "Lion": ("roar roar", "🦁"),
    "Frog": ("ribbit ribbit", "🐸"),
    "Bee": ("bzzzz bzzzz", "🐝"),
    "Owl": ("hoo hoo", "🦉"),
    "Sparrow": ("tweet tweet", "🐦"),
    "Snake": ("hisss hisss", "🐍"),
    "Donkey": ("hee haw", "🫏"),
    "Elephant": ("trumpet trumpet", "🐘"),
    "Monkey": ("ooh ooh", "🐵"),
    "Parrot": ("squawk squawk", "🦜"),
    "Crow": ("caw caw", "🐦"),
    "Turkey": ("gobble gobble", "🦃"),
    "Goat": ("bleat bleat", "🐐"),
    "Rooster": ("cock-a-doodle-doo", "🐓"),
    "Penguin": ("waak waak", "🐧"),
    "Seal": ("ark ark", "🦭"),
    "Wolf": ("howwwwl howwwwl", "🐺"),
    "Bear": ("growwwl growwwl", "🐻"),
    "Deer": ("snort snort", "🦌"),
    "Raccoon": ("chitter chitter", "🦝"),
    "Fox": ("yip yip", "🦊"),
    "Coyote": ("awoo awoo", "🐕"),
    "Hog": ("grunt grunt", "🐗"),
    "Giraffe": ("humm humm", "🦒"),
    "Zebra": ("whinny whinny", "🦓"),
    "Kangaroo": ("click click", "🦘"),
    "Koala": ("bellow bellow", "🐨"),
    "Panda": ("mew mew", "🐼"),
    "Tiger": ("roaarrr roaarrr", "🐅"),
    "Cheetah": ("purrrr purrrr", "🐆"),
    "Leopard": ("snarl snarl", "🐆"),
    "Jaguar": ("cough cough", "🐆"),
    "Hippo": ("whuff whuff", "🦛"),
    "Rhino": ("snuffle snuffle", "🦏"),
    "Camel": ("groan groan", "🐫"),
    "Llama": ("hum hum", "🦙"),
    "Alpaca": ("humm humm", "🦙"),
    "Rabbit": ("stomp stomp", "🐰"),
    "Squirrel": ("chit chit", "🐿"),
    "Chipmunk": ("chirrup chirrup", "🐿"),
    "Otter": ("squeak squeak", "🦦"),
    "Badger": ("hiss hiss", "🦡"),
    "Skunk": ("stamp stamp", "🦨"),
    "Hedgehog": ("snuffle snuffle", "🦔"),
    "Porcupine": ("quill quill", "🦔"),
    "Turtle": ("hiss hiss", "🐢"),
    "Lizard": ("click click", "🦎"),
    "Crocodile": ("croak croak", "🐊"),
    "Alligator": ("growl growl", "🐊"),
    "Dolphin": ("whistle whistle", "🐬"),
    "Whale": ("boom boom", "🐋"),
    "Shark": ("silence silence", "🦈"),
    "Fish": ("blub blub", "🐟"),
    "Flamingo": ("honk honk", "🦩"),
    "Swan": ("honk honk", "🦢"),
    "Goose": ("honk honk", "🦆"),
    "Hawk": ("screee screee", "🦅"),
    "Eagle": ("screee screee", "🦅"),
    "Vulture": ("croak croak", "🦅"),
    "Raven": ("caw caw", "🐦"),
    "Dove": ("coo coo", "🕊"),
    "Pigeon": ("coo coo", "🐦"),
    "Woodpecker": ("tap tap", "🪶"),
    "Peacock": ("scream scream", "🦚"),
    "Pheasant": ("squawk squawk", "🐦"),
    "Quail": ("bob-white bob-white", "🐦"),
    "Ostrich": ("thump thump", "🐦"),
    "Emu": ("boom boom", "🐦"),
    "Bat": ("screech screech", "🦇"),
    "Butterfly": ("flutter flutter", "🦋"),
    "Cricket": ("chirp chirp", "🦗"),
    "Grasshopper": ("chirp chirp", "🦗"),
    "Cicada": ("buzzzz buzzzz", "🦗"),
    "Mosquito": ("whine whine", "🦟"),
    "Wasp": ("bzzzz bzzzz", "🐝"),
    "Termite": ("tick tick", "🦗"),
    "Ant": ("march march", "🐜")
}

class PetSoundGuesser:
    def __init__(self, root):
        self.root = root
        self.root.title("Pet Sound Guesser")
        self.root.geometry("750x700")
        self.root.configure(bg="#f0f0f0")
        
        self.current_pet = None
        self.score = 0
        self.total_questions = 0
        self.game_running = True
        
        self.setup_ui()
        self.new_sound()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Top frame for title and quit button
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(pady=15, fill="x", padx=10)
        
        # Title
        title_label = tk.Label(
            top_frame,
            text="Pet Sound Guesser",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(side="left")
        
        # Quit button
        quit_btn = tk.Button(
            top_frame,
            text="QUIT",
            font=("Arial", 11, "bold"),
            bg="#ff6b6b",
            fg="white",
            command=self.quit_game,
            width=12,
            padx=10
        )
        quit_btn.pack(side="right")
        
        # Score display
        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.score}/{self.total_questions}",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#666"
        )
        self.score_label.pack(pady=10)
        
        # Animal picture display
        self.picture_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 80),
            bg="#f0f0f0"
        )
        self.picture_label.pack(pady=15)
        
        # Sound display (Question)
        self.sound_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 13, "italic"),
            bg="#f0f0f0",
            fg="#0066cc"
        )
        self.sound_label.pack(pady=8)
        
        # Question label
        self.question_label = tk.Label(
            self.root,
            text="Which animal makes this sound?",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        self.question_label.pack(pady=8)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=15, expand=True)
        
        self.buttons = []
        self.button_vars = []
        
        # Create 4 answer buttons
        for i in range(4):
            btn = tk.Button(
                buttons_frame,
                text="",
                font=("Arial", 11),
                width=25,
                command=lambda idx=i: self.check_answer(idx)
            )
            btn.pack(pady=6)
            self.buttons.append(btn)
            self.button_vars.append(None)
        
        # Answer display (shows correct answer after answering)
        self.answer_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#228B22"
        )
        self.answer_label.pack(pady=10)
        
        # Bottom frame with instructions
        bottom_frame = tk.Frame(self.root, bg="#f0f0f0")
        bottom_frame.pack(pady=10, fill="x", padx=10)
        
        info_label = tk.Label(
            bottom_frame,
            text=f"Total animals: {len(pet_sounds)} | To quit: Click the RED QUIT button",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#999"
        )
        info_label.pack()
    
    def new_sound(self):
        """Select a new sound and create options"""
        if not self.game_running:
            return
            
        self.current_pet = random.choice(list(pet_sounds.keys()))
        sound, picture = pet_sounds[self.current_pet]
        
        self.picture_label.config(text=picture)
        self.sound_label.config(text=f'Question: "{sound}"')
        self.answer_label.config(text="")
        
        # Create options (correct answer + 3 random wrong answers)
        options = [self.current_pet]
        available = [p for p in pet_sounds.keys() if p != self.current_pet]
        options.extend(random.sample(available, 3))
        random.shuffle(options)
        
        # Store the correct button index
        self.correct_button_index = options.index(self.current_pet)
        
        # Update buttons
        for i, btn in enumerate(self.buttons):
            self.button_vars[i] = options[i]
            btn.config(text=options[i], state="normal", bg="#e0e0e0")
    
    def check_answer(self, button_index):
        """Check if the selected answer is correct"""
        if not self.game_running:
            return
            
        self.total_questions += 1
        selected_pet = self.button_vars[button_index]
        
        # Disable all buttons
        for btn in self.buttons:
            btn.config(state="disabled")
        
        if button_index == self.correct_button_index:
            self.score += 1
            self.buttons[button_index].config(bg="#90EE90")
            self.answer_label.config(
                text=f"Correct Answer: {self.current_pet}",
                fg="#228B22"
            )
            messagebox.showinfo("Correct!", f"Yes! It's a {self.current_pet}!")
        else:
            self.buttons[button_index].config(bg="#FFB6C6")
            self.buttons[self.correct_button_index].config(bg="#90EE90")
            self.answer_label.config(
                text=f"Correct Answer: {self.current_pet}",
                fg="#DC143C"
            )
            messagebox.showinfo(
                "Wrong!",
                f"Sorry! It's a {self.current_pet}, not a {selected_pet}."
            )
        
        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
        
        # Next question after a short delay
        if self.game_running:
            self.root.after(2000, self.new_sound)
    
    def quit_game(self):
        """Quit the game"""
        self.game_running = False
        
        if self.total_questions > 0:
            percentage = (self.score / self.total_questions) * 100
            final_message = f"""GAME OVER!

Final Score: {self.score}/{self.total_questions}
Accuracy: {percentage:.1f}%

Thanks for playing Pet Sound Guesser!"""
            messagebox.showinfo("Game Over", final_message)
        else:
            messagebox.showinfo("Exit", "Thanks for playing Pet Sound Guesser!")
        
        self.root.quit()

def main():
    root = tk.Tk()
    app = PetSoundGuesser(root)
    root.mainloop()

if __name__ == "__main__":
    main()
