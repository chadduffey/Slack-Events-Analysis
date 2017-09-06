from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import json
import os
import pprint

# Our app's Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
CLIENT = SlackClient(SLACK_BOT_TOKEN)

total_size = 0

# Example responder to greetings
# @slack_events_adapter.on("message")
# def handle_message(event_data):
#     message = event_data["event"]
#     # If the incoming message contains "hi", then respond with a "Hello" message
#     if message.get("subtype") is None and "hi" in message.get('text'):
#         channel = message["channel"]
#         message = "Hello <@%s>! :tada:" % message["user"]
#         CLIENT.api_call("chat.postMessage", channel=channel, text=message)
#
#
# # Example reaction emoji echo
# @slack_events_adapter.on("reaction_added")
# def reaction_added(event_data):
#     event = event_data["event"]
#     emoji = event["reaction"]
#     channel = event["item"]["channel"]
#     text = ":%s:" % emoji
#     CLIENT.api_call("chat.postMessage", channel=channel, text=text)

def display_total(size):
    print "-------------------------------------------"
    print size, " bytes sent from slack events so far"
    print "(", size / 1024 / 1024, " MB so far)"
    print "-------------------------------------------"

# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def channel_created(event_data):
    global total_size
    json_obj = json.dumps(event_data)
    json_size = len(json_obj)
    total_size = total_size + json_size
    print "The size of this object is: ", len(json_obj)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(event_data)
    display_total(total_size)


    #event = event_data["event"]
    #emoji = event["reaction"]
    #channel = event["item"]["channel"]
    #text = ":%s:" % emoji
    #CLIENT.api_call("chat.postMessage", channel=channel, text=event_data)

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)
