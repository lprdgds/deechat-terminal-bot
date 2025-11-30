# chatbot_dee.py
"""
Simple terminal chatbot using the OpenAI API.

Features:
- System persona (your bot's "vibe")
- Continuous conversation loop
- Conversation log saved to a .txt file
"""

from datetime import datetime
from openai import OpenAI
import os

client = OpenAI()

LOG_DIR = "logs"

def ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def get_log_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(LOG_DIR, f"dee_chat_{timestamp}.txt")

def log_message(log_file, speaker, text):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{speaker.upper()}: {text}\n\n")

def run_chat():
    ensure_log_dir()
    log_file = get_log_filename()

    system_message = (
        "You are an encouraging but direct AI coach helping Dee learn coding, "
        "AI, trading, and personal development using Bloom's taxonomy. "
        "You explain things simply and give concrete next steps."
    )

    messages = [
        {"role": "system", "content": system_message}
    ]

    print("✨ Dee's Chatbot is live! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit", "bye"}:
            print("Bot: Talk soon, Dee 💜")
            break

        messages.append({"role": "user", "content": user_input})
        log_message(log_file, "you", user_input)

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
            )

            bot_reply = response.choices[0].message.content.strip()
            print(f"Bot: {bot_reply}\n")

            messages.append({"role": "assistant", "content": bot_reply})
            log_message(log_file, "bot", bot_reply)

        except Exception as e:
            print("Bot: Oops, something went wrong:", e)
            log_message(log_file, "error", str(e))


if __name__ == "__main__":
    run_chat()
