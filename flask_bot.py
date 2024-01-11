
# SLACK_BOT_TOKEN = "xoxb-6461880745393-6451877706532-HesNri8X9d2lXQoH8lGjQVVW"
# SLACK_BOT_TOKEN = "xoxb-6461880745393-6473508055424-zX0vFV8kNZ5GyPJUfhLHg31K"
# OPENAI_API_KEY  = "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"

import os
import openai
from flask import Flask, request, jsonify
import requests

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOEKN")
OPENAI_API_KEY = os.environ.get("OPEN_API_KEY")
CHAT_BOT_END_POINT = os.environ.get("CHAT_BOT_END_POINT")


app = Flask(__name__)

conversation_history = {}

@app.route("/")
def hello_world():
    return "Hi world!!"

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    print(data)

    if 'challenge' in data:
        return data['challenge']

    event_type = data["event"]["type"]

    if event_type == "app_mention":
        thread_ts = data["event"]["event_ts"]
        user_message = str(data["event"]["text"]).split(">")[1]

        # Retrieve conversation history for the thread
        history = conversation_history.get(thread_ts, [])

        response_text = requests.get(f"{CHAT_BOT_END_POINT}/{user_message}").text
        print(response_text)

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Here you go:\n{response_text}"
                }
            }
        ]

        # Reply to the thread
        response = {"channel": data["event"]["channel"], "thread_ts": thread_ts, "blocks": blocks}
        send_slack_message(response)

    return jsonify({"status": "success"}), 200

def send_slack_message2(response):
    # Implement the logic to send a message back to Slack
    # Use the Slack API or the Slack SDK for Python
    # Replace this with your actual Slack messaging code
    # ...

    # For example:
    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    payload = {"channel": response["channel"], "thread_ts": response.get("thread_ts", ""), "text": response["text"]}
    print(payload)
    response = requests.post(slack_url, headers=headers, json=payload)
    print(response.body)

def send_slack_message(response):
    # Replace this with your actual Slack messaging code
    # ...

    # For example:
    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    payload = {"channel": response["channel"], "thread_ts": response.get("thread_ts", ""), "text": response["text"]}
    
    print(payload)
    response = requests.post(slack_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("Message sent successfully!")
        print(response.text)  # Print the response content
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.text)  # Print the error response content

if __name__ == "__main__":
    app.run()  # Replace with your desired port
