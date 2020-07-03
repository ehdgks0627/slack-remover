import requests

from slack import Slack
import time

token = '{TOKEN HERE}'
auth = '{AUTH HERE}'
slack = Slack(token, auth)
channel_list = slack.get_channel_list()
for i in range(len(channel_list)):
    print(f"{i + 1}. {channel_list[i][1]}")
index = int(input("번호 입력 > "))
channel_id = channel_list[index - 1][0]

history_list = slack.get_history_list(channel_id)

for history in history_list:
    ok = slack.delete_chat(channel_id, history[0])
    time.sleep(1)
    print(f"{history_list.index(history) + 1}/{len(history_list)}",history[1], ok)
