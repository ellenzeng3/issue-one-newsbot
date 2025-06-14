import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from slack_bolt import App
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# run on default port (500)
app = Flask(__name__)

# send events to http://localhost/slack/events
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app) 

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
# client.chat_postMessage(channel='#test-slack-api', text="Hello World!")

# run the web server if running directly
if __name__ == "__main__":
    app.run(debug=True)