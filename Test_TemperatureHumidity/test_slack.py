# import os

# #from slackclient import SlackClient
# import slack
# from slack_sdk import WebClient

# # botアカウントのトークンを指定
# API_TOKEN = 'xoxb-4101200651380-4100235025731-aXulc8SvIrHuu6Mm7autcnwg'
# channel_general = 'C042G5R0C5V'
# file_name = '/home/zen/Documents/Geek/Test_TemperatureHumidity/test_temp_humi.csv'

# slack_token = os.getenv(API_TOKEN)
# #client = SlackClient(slack_token)
# client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])


# from slack.errors import SlackApiError

# try:
#   response = client.chat_postMessage(
#             channel=channel_general,
#             text="Hello world!!!!!!")

#   #assert response["ok"]
#   #assert response["message"]["text"] == "Hello world!"
# except:
#   #print(traceback.format_exc())
#   print('error')

# # def channel_list(client):
# #     channels = client.api_call("channels.list")
# #     if channels['ok']:
# #         return channels['channels']
# #     else:
# #         return None

# # def send_message(client, channel_id, message):
# #     client.api_call(
# #         'chat.postMessage',
# #         channel=channel_id,
# #         text=message
# #     )

# # def send_file(client, channel_id, content, title):
# #     client.api_call(
# #         'files.upload',
# #         channels=channel_id,
# #         content=content,
# #         title=title
# #     )

# # if __name__ == '__main__':
# #     channel_list(client)
# #     # send_message(client, channel_general, 'test!!!!!!!!!!!!')
# #     # send_file(client, channel_general, file_name, 'file_data')

import requests

url = "https://slack.com/api/chat.postMessage"
data = {
   "token": "xoxb-4101200651380-4100235025731-aXulc8SvIrHuu6Mm7autcnwg",
   "channel": "C042G5R0C5V",
   "text": "Hello world"
}
requests.post(url, data=data)

url2 = "https://slack.com/api/files.upload"
data2 = {
   "token": "xoxb-4101200651380-4100235025731-aXulc8SvIrHuu6Mm7autcnwg",
   "channels": "C042G5R0C5V",
   "title": "my file",
   "initial_comment": "initial\ncomment"
}
files = {'file': open("/home/zen/Documents/Geek/Test_TemperatureHumidity/temp_humi.png", 'rb')}
requests.post(url2, data=data2, files=files)
