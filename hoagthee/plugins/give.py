import re

from rtmbot.core import Job, Plugin

from hoagthee.api import HoagTheeClient


VALUE_TEXT = ':hoagie:'
re_user = re.compile(r'\<@(\w+)\>')


class GiveHoagiePlugin(Plugin):
    def __init__(self, *args, **kwargs):
        super(GiveHoagiePlugin, self).__init__(*args, **kwargs)
        self.hoag_api = HoagTheeClient(
            host=self.plugin_config['redis'].get('host', 'localhost'),
            port=self.plugin_config['redis'].get('port', 6379),
        )

    def register_jobs(self):
        refresh_users_job = RefreshUsersJob(self.hoag_api, self.refresh_users_delay)
        self.jobs.append(refresh_users_job)

    def process_message(self, data):
        text = data.get('text')
        if not text:
            return

        msg_value = self.count_rewards(text)
        if msg_value > 0:
            sender = data['user']
            channel = data['channel']
            recipients = self.extract_users(text)
            if recipients:
                self.distribute_rewards(sender, recipients, msg_value)
                self.send_reward_messages(sender, recipients, msg_value)
            else:
                print('no recipients listed for {} {}'.format(sender, msg_value, VALUE_TEXT))
            print('all done...')

    def distribute_rewards(self, sender, recipients, reward):
        for recipient in recipients:
            self.hoag_api.give(sender, recipient, reward)

    def send_reward_messages(self, sender, recipients, reward):
        sender_name = self.hoag_api.get_user_name(sender)
        msg = '@{} sent you {} x {}'.format(sender_name, reward, VALUE_TEXT)
        for recipient in recipients:
            self.outputs.append([recipient, msg])

    def extract_users(self, text):
        return re_user.findall(text)

    def count_rewards(self, text):
        return text.count(VALUE_TEXT)

    @property
    def refresh_users_delay(self):
        return int(self.plugin_config.get('refresh_users_delay', 60 * 60))


class RefreshUsersJob(Job):
    def __init__(self, hoag_api, *args, **kwargs):
        super(RefreshUsersJob, self).__init__(*args, **kwargs)
        self.hoag_api = hoag_api

    def run(self, slack_client):
        print('Refreshing users...')
        all_users = []
        cursor = None
        while True:
            response = slack_client.api_call('users.list', cursor=cursor)
            users = response['members']
            all_users += users

            cursor = response.get('cursor')
            if not cursor:
                break

        self.hoag_api.update_user_profiles(all_users)
        print('Refreshed {} users'.format(len(all_users)))
