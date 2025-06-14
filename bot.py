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
user_test = ""
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# run on default port (5000)
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

    client.chat_postEphemeral(
        channel=channel,
        user=user,
        text="Poll failed to load",
        blocks = [
      {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Which category does this belong to?"
        }
    },
    {
        "type": "actions",
        "block_id": "category_poll",
        "elements": [
            {
                "type": "button",
                "action_id": "choose_tech",
                "text": {"type": "plain_text", "text": "Tech Reform"},
                "value": f"{url}|Tech Reform"
            },
            {
                "type": "button",
                "action_id": "choose_election",
                "text": {"type": "plain_text", "text": "Election Protection"},
                "value": f"{url}|Election Protection"
            },
            {
                "type": "button",
                "action_id": "choose_money",
                "text": {"type": "plain_text", "text": "Money in Politics"},
                "value": f"{url}|Constitutional Defense"
            }
        ]
    }
]   
    )

# run the web server if running directly
if __name__ == "__main__":
    app.run(debug=True)