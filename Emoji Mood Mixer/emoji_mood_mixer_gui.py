import random
import datetime

# List of mood emojis

emojis = ["😀", "😅", "😎", "🤔", "😴", "😡", "😇", "🥳", "😢", "🤯", "😬", "😱"]

def generate_mood():
    # Randomly pick 2 or 3 emojis
    count = random.choice([2, 3])
    mood_combo = random.sample(emojis, count)
    return "".join(mood_combo)

def main():
    today = datetime.date.today()
    mood = generate_mood()
    print(f"🌟 Your Emoji Mood for {today} is: {mood}")

    # Save to a file for tracking  
    with open("emoji_mood_log.txt", "a", encoding="utf-8") as f:  
        f.write(f"{today}: {mood}\n")  


if __name__ == "__main__":
    main()