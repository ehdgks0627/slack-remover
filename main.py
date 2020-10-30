import requests

from slack import Slack
import time

token = 'xoxc-317679371207-471504404707-914799581936-acaab721a3d39d68a7da6198c3871c22c82121dd9f7bd4c5f25efd25e21280d0'
auth = 'eUHzX4zYdc0W1u2374yUh0FFmsG7qQwOZDBXHT07h2cutsPTCWTOQJjN6GSEgp8161TR1LHpFz7GI4lzCZeX3WGKk6eWHihspcH0q%2BHi6oQlBDMnMY%2FbQhm4ORgmww5ZuA9shOj95sRTMjCgm8wLS25H6OLVtbYeexlsRcL5REjbibMzLfPdTn8%3D'
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
