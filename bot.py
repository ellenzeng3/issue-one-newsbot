import slack
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from slack_bolt import App
from flask import Flask
from slackeventsapi import SlackEventAdapter

URL_REGEX = re.compile(r'https?://\S+')
channel_test = "#test-slack-api"
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# run on default port (500)
app = Flask(__name__)

# send events to http://localhost/slack/events
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app) 
client = slack.WebClient(token=os.environ['SLACK_TOKEN']) 

@slack_event_adapter.on('app_mention')
def handle_mention(payload):
    event   = payload.get('event', {})
    user    = event.get('user')
    channel = event.get('channel')
    text    = event.get('text', '')

    # strip off the mention prefix
    _, _, message = text.partition('>')
    message = message.strip()

    # find the first URL
    urls = URL_REGEX.findall(message)
    if not urls:
        client.chat_postEphemeral(
            channel=channel_test,
            user=user,
            text="No URL found."
        )
        return

    url = urls[0]

    client.chat_postEphemeral(
            channel=channel_test,
            user=user,
            text=f"You sent me this url: “{url}”"
        )

# run the web server if running directly
if __name__ == "__main__":
    app.run(debug=True)