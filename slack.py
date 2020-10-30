import time

import requests


class Slack:

    def __init__(self, token, auth):
        self.token = token
        self.session = requests.session()
        self.session.cookies['d'] = auth
        self.url = 'https://pilabgroup.slack.com/api'
        self.user_id = None

    def get_channel_list(self):
        channels = []
        now = time.time()
        url = self.url + '/client.boot?_x_id=noversion-%.3f&_x_version_ts=noversion&_x_gantry=true' % now
        res = self.session.post(url, {
            'token': self.token,
            'only_self_subteams': '1',
            'flannel_api_ver': '4',
            'include_min_version_bump_check': '1',
            'version_ts': str(int(now)),
            '_x_reason': 'deferred-data',
            '_x_sonic': 'true',
        })
        data = res.json()
        for channel in data['channels']:
            if channel['is_archived']:
                continue
            channels.append((channel['id'], channel['name']))
        for mpim in data['mpims']:
            channels.append((mpim['id'], mpim['purpose']['value']))
        self.user_id = data['self']['id']
        return channels

    def get_history_list(self, channel_id):
        histories = []
        now = time.time()
        url = self.url + '/conversations.history?_x_id=b7dba001-%.3f&slack_route=T9BKZAX63&_x_version_ts=noversion&_x_gantry=true' % now
        req_data = {
            'channel': channel_id,
            'limit': '1000',
            'ignore_replies': 'true',
            'include_pin_count': 'true',
            'inclusive': 'true',
            'no_user_profile': 'true',
            'token': self.token,
            '_x_reason': 'message-pane/requestHistory',
            '_x_mode': 'online',
            '_x_sonic': 'true',
        }
        while True:
            res = self.session.post(url, req_data)
            data = res.json()
            for message in data['messages']:
                if message['type'] != 'message' or 'subtype' in message:
                    continue
                if message['user'] != self.user_id:
                    continue
                histories.append((message['ts'], message['text']))
            req_data['latest'] = data['messages'][-1]['ts']
            if not data['has_more']:
                break
        return histories

    def delete_chat(self, channel_id, ts):
        now = time.time()
        url = self.url + '/chat.delete?_x_id=b7dba001-%.3f&_x_csid=wYx9xOGpTdo&slack_route=T9BKZAX63&_x_version_ts=noversion&_x_gantry=true' % now
        data = {
            'channel': channel_id,
            'ts': ts,
            'token': self.token,
            '_x_reason': 'animateAndDeleteMessageApi',
            '_x_mode': 'online',
            '_x_sonic': 'true',
        }
        while True:
            try:
                res = self.session.post(url, data)
                break
            except:
                time.sleep(1)
                continue
        return res.json()['ok']
