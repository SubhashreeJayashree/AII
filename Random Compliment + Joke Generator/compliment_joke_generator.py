import random

# List of compliments

compliments = [
"You have a great sense of humor!",
"You are really kind-hearted!",
"Your creativity is inspiring!",
"You make people smile effortlessly!",
"You have a wonderful perspective on life!"
]

# List of jokes

jokes = [
"Why did the scarecrow win an award? Because he was outstanding in his field!",
"Why don’t skeletons fight each other? They don’t have the guts.",
"Why did the tomato turn red? Because it saw the salad dressing!",
"I would tell you a joke about construction, but I’m still working on it.",
"Why don’t scientists trust atoms? Because they make up everything!"
]

def generate_daily_message():
    compliment = random.choice(compliments)
    joke = random.choice(jokes)
    return compliment, joke

def main():
    compliment, joke = generate_daily_message()
    print("🌟 Your Daily Compliment + Joke 🌟\n")
    print(f"Compliment: {compliment}")
    print(f"Joke: {joke}")

    # Save to file for tracking
    with open("compliment_joke_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{compliment} | {joke}\n")


if __name__ == "__main__":
    main()
