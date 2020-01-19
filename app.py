import os
import slack
from message_builder import Statistics

def configure_message(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new onboarding tutorial.
    message_builder = Statistics(channel)

    # Get the onboarding message payload
    message = message_builder.get_message_payload()

    # Post the onboarding message in Slack
    response = web_client.chat_postMessage(**message)


    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    message_builder.timestamp = response["ts"]



@slack.RTMClient.run_on(event="message")
def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")
    ts = data.get("ts")

    if text and text.lower() == "start":
        new_web_client.chat_delete(channel=channel_id, ts=ts)
        return configure_message(web_client, user_id, channel_id)

if __name__ == "__main__":
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    auth_token = os.environ["AUTH_TOKEN"]
    new_web_client = slack.WebClient(token=auth_token)
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()
