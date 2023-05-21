import telebot
import openai

# Set up the Telegram bot token and OpenAI API key
telegram_token = '6007137718:AAFd5FB-JZs0S1p2eL30F5O1JwLvxY_Znrw'
openai_api_key = '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'


# Initialize the Telegram bot
bot = telebot.TeleBot(telegram_token)

# Initialize the OpenAI API client
openai.api_key = openai_api_key

# Define a function to generate a response using OpenAI
    
def generate_response(message):
    # Define the OpenAI chat completion parameters
    model = 'gpt-3.5-turbo'
    max_tokens = 3097
    temperature = 0.7
    
    # Generate a response from OpenAI
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
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
# Define the Telegram bot message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Get the user's message
    user_message = message.text
    
    # Check if the user wants to stop running
    if user_message.lower() == 'stop running':
        # Stop the bot
        bot.stop_polling()
    else:
        # Generate a response using OpenAI
        bot_response = generate_response(user_message)
        
        # Send the response back to the user
        bot.send_message(message.chat.id, bot_response)

# Start the Telegram bot
while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"An error occurred while running the Telegram bot: {e}")
        # You can handle the error or log it as needed
        # Here, we simply print the error message
