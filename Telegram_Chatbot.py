import telebot
import openai
import tkinter as tk
import threading
from itertools import cycle

# Set up the Telegram bot token and OpenAI API key
telegram_token = '6007137718:AAFd5FB-JZs0S1p2eL30F5O1JwLvxY_Znrw'
openai_api_key = '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'

# Initialize the Telegram bot
bot = telebot.TeleBot(telegram_token)

# Initialize the OpenAI API client
openai.api_key = openai_api_key

# Conversation history list to store the messages
conversation_history = []

# Define a function to generate a response using OpenAI
def generate_response(message):
    # Define the OpenAI chat completion parameters
    model = 'gpt-3.5-turbo'
    max_tokens = 3097
    temperature = 0.7

    # Generate a response from OpenAI
    response = openai.ChatCompletion.create(
        model=model,
        messages=conversation_history + [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )

    # Extract and return the generated response
    return response.choices[0].message.content.strip()

# Define the Telegram bot message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Get the user's message
    user_message = message.text

    # Check if the user wants to stop the program
    if user_message.lower() == 'vicx':
        bot.send_message(message.chat.id, "Program stopped. Goodbye!")
        return

    # Generate a response using OpenAI
    bot_response = generate_response(user_message)

    # Send the response back to the user
    bot.send_message(message.chat.id, bot_response)

    # Add the user and bot messages to the conversation history
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history.append({"role": "assistant", "content": bot_response})

# Create a tkinter window
window = tk.Tk()
window.configure(bg="black")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the center position for the label
label_x = screen_width // 2
label_y = screen_height // 2

# Create a label for displaying "Connected to Telegram"
connected_label = tk.Label(window, text="Connected to Telegram", font=("Arial", 10), fg="red", bg="black")
connected_label.place(x=label_x, y=label_y, anchor="center")

# Function to animate the label text
def animate_label():
    colors = cycle(["red", "white"])  # Cycle between red and white
    for color in colors:
        connected_label.config(fg=color)
        window.update()
        window.after(500)  # Delay between color changes

# Start the label animation in a separate thread
thread = threading.Thread(target=animate_label, daemon=True)
thread.start()

# Function to start the Telegram bot polling
def start_telegram_bot():
    bot.polling(none_stop=True)

# Start the Telegram bot polling in a separate thread
telegram_thread = threading.Thread(target=start_telegram_bot, daemon=True)
telegram_thread.start()

# Run the tkinter main loop
window.mainloop()
