from flask import Flask, render_template, request, jsonify
# from DBChatApp import *
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPEN_API_KEY"]

app = Flask(__name__)

# Set up OpenAI API credentials
# openai.api_key = "YOUR_OPENAI_API_KEY"

# # Predefined messages for the bot
predefined_messages = [
    "Hi, how can I assist you?",
    "What brings you here today?",
    "How can I help you?",
    "Is there anything specific you would like to know?"
]

# Home page
@app.route("/")
def home():
    return render_template("index.html")
    # return "Hello World"

# @app.route("/get_response", methods=["POST"])
# def chatbot():
#     # get the message input from the user
#     user_message = request.form["user_message"]

#     # Combine user message and predefined messages
#     messages = predefined_messages + [user_message]

#     # User the OpenAI API to generate response
#     # prompt = f"User: {user_message}\nChatbot: "
#     chat_history = []

#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt = prompt,
#         messages=[
#             {"role": "system", "content": message} for message in messages
#         ],
#         max_tokens=50,
#         temperature=0.7,
#         n=1,
#         stop=None
#     )

#     # Add the user input and bot response to chat_history
#     bot_response = response.choices[0].message.content.strip()
#     chat_history.append("User: {user_input}\nChatbot {bot_response}")

#     return render_template(
#         "chatbot.html",
#         user_message=user_message,
#         bot_response = bot_response
#     )



# API endpoint for getting bot responses
@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"]

    # Combine user message and predefined messages
    messages = predefined_messages + [user_message]

    print(f"messages={messages}")

    # Generate a response from ChatGPT
    response = openai.Completion.create(
        engine="text-davinci-003",
        messages=[
            {"role": "system", "content": message} for message in messages
        ],
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None
    )

    # Extract and return the generated response
    bot_response = response.choices[0].message.content.strip()

    print(f"bot_response={bot_response}")

    return jsonify({"bot_response": bot_response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)