
SLACK_BOT_TOKEN = "xoxb-6461880745393-6451877706532-HesNri8X9d2lXQoH8lGjQVVW"
SLACK_APP_TOKEN = "xapp-1-A06D9R7KM0C-6442774736534-1a606c1af028fe3f5d7a6363bdcb30f31b85f23966b29f2101e7b249690f2ca1"
OPENAI_API_KEY  = "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"

import os
import openai
from flask import Flask, request, jsonify


app = Flask(__name__)

conversation_history = {}

@app.route("/")
def hello_world():
    return "Hi world!!"

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    if 'challenge' in data:
        return data['challenge']

    event_type = data["event"]["type"]

    if event_type == "app_mention":
        thread_ts = data["event"]["thread_ts"]
        user_message = str(data["event"]["text"]).split(">")[1]

        # Retrieve conversation history for the thread
        history = conversation_history.get(thread_ts, [])

        # Create prompt for ChatGPT
        prompt = " ".join([f"In thread {thread_ts}, user said: {message}." for message in history])
        prompt += f" Generate a response: {user_message}"

        # Let the user know that the bot is working on the request
        response = {"channel": data["event"]["channel"], "text": f"Hello from your bot! :robot_face:\nThanks for your request, I'm on it!"}
        send_slack_message(response)

        # Check ChatGPT
        openai.api_key = OPENAI_API_KEY
        response_text = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5
        ).choices[0].text.strip()

        # Update conversation history with the new message
        conversation_history[thread_ts] = history + [user_message]

        # Reply to the thread
        response = {"channel": data["event"]["channel"], "thread_ts": thread_ts, "text": f"Here you go:\n{response_text}"}
        send_slack_message(response)

    return jsonify({"status": "success"}), 200

def send_slack_message(response):
    # Implement the logic to send a message back to Slack
    # Use the Slack API or the Slack SDK for Python
    # Replace this with your actual Slack messaging code
    # ...

    # For example:
    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    payload = {"channel": response["channel"], "thread_ts": response.get("thread_ts", ""), "text": response["text"]}
    requests.post(slack_url, headers=headers, json=payload)

if __name__ == "__main__":
    app.run()  # Replace with your desired port
