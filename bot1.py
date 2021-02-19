import slack
import os
from pathlib import Path
from dotenv import load_dotenv
# Import Flask
from flask import Flask
# Handles events from Slack
from slackeventsapi import SlackEventAdapter
# Open weather map
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

# Load the Token from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# Configure your flask application
app = Flask(__name__)

# Configure SlackEventAdapter to handle events
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

# Using WebClient in slack, there are other clients built-in as well !!
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

# connect the bot to the channel in Slack Channel
print("sending hello world message...")
client.chat_postMessage(channel='#bot-dev', text='Message from bot (on startup)')

# Get Bot ID
BOT_ID = client.api_call("auth.test")['user_id']
print("bot is running as user_id:", BOT_ID)

# Connect to Open weather map API
owm = OWM(os.environ["OPEN_WEATHER_MAP"])
mgr = owm.weather_manager()

@app.route('/')
def hello():
    return 'up'



# handling Message Events
@slack_event_adapter.on('message')
def message(payload):
    print("bot read message:", payload)
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text2 = event.get('text')
        

    if BOT_ID != user_id:
        # "weather toronto" -> Gets weather for toronto
        # "weather toronto,canada" -> Same as above
        # "weather toronto,usa" -> Gets weather for toronto (in USA)
        # "weather toronto,ohio,usa" -> Same as above
        text2split = text2.split(" ")
        if text2split[0] == "weather":
            place = " ".join(text2split[1:])
            print("getting weather for place:", place)
            try:
                print("got weather data...") 
                observation = mgr.weather_at_place(place)
                weather = observation.weather
                temp = weather.temperature("celsius") # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
                client.chat_postMessage(channel=channel_id, text=str(temp))
            except: 
                print("failed to get weather data!")
                client.chat_postMessage(channel=channel_id, text="Could not find weather for location: {}".format(place))
                client.chat_postMessage(channel=channel_id, text="Usage: weather <city>,<region>,<country> (no spaces, region and country are optional)")
        else:
            print("bot echoing message from:", user_id)
            client.chat_postMessage(channel=channel_id, text=text2)

# Run the webserver micro-service
if __name__ == "__main__":
    app.run(debug=True)