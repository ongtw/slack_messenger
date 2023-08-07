import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Constants
SLACK_CHANNEL_ENGR = "#engineering"
BOT_USER_ID = "U055UHNFC90"  # the bot
# NB: uploaded chart into PeekingDuck storage bucket to make it publicly accessible online
CHART_IMG_URL = "https://storage.googleapis.com/peekingduck/data/big_chart_1200x675.jpg"
# Load env vars
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
USER_ID = os.getenv("USER_ID")

client = WebClient(token=SLACK_BOT_TOKEN)
auth_test = client.auth_test()
bot_user_id = auth_test["user_id"]
print(f"App bot user id={bot_user_id}")


def list_all_uploaded_files(bot_user_id: str):
    """To list all files uploaded by given bot user id

    Args:
        bot_user_id (str): the bot user id
    """
    files = client.files_list(user=bot_user_id)
    # print(type(files))
    # print(dir(files))
    files_list = files.get("files")
    print(f"--- {bot_user_id} files ---")
    print(files_list)
    print("--- end ---")


def delete_all_uploaded_files(bot_user_id: str):
    """To delete all files uploaded by given bot user id

    Args:
        bot_user_id (str): the bot user id
    """
    files = client.files_list(user=bot_user_id)
    files_list = files.get("files")
    # to delete files uploaded
    for file in files_list:
        # print(type(file))
        # print(dir(file))
        file_id = file["id"]
        print(f"deleting file_id={file_id}")
        client.files_delete(file=file_id)


def send_msg():
    try:
        # Format msg block
        msg_block = [
            # text + image combo
            {
                "type": "image",
                "title": {"type": "plain_text", "text": "The Chart"},
                "image_url": CHART_IMG_URL,
                "alt_text": "the dog",
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Post Slack message with a _1200x675 image_ (auto format)",
                },
            },
        ]

        # Send msg to individual user
        msg_resp = client.chat_postMessage(channel=USER_ID, blocks=msg_block)

        # Send msg to group
        # msg_resp = client.chat_postMessage(channel=SLACK_CHANNEL_ENGR, blocks=msg_block)

        print(dir(msg_resp))
        print(msg_resp)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Error: {e.response['error']}")


if __name__ == "__main__":
    send_msg()
