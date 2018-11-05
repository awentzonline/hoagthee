import json

import redis


class HoagTheeClient(object):
    def __init__(self, **redis_kwargs):
        self.redis = redis.StrictRedis(**redis_kwargs)

    def give(self, issuer, recipient, num_rewards):
        self.redis.hincrby('allrewards', recipient, num_rewards)

    def fetch_rewards_for_user(self, user):
        return int(self.redis.hget('rewards', user) or 0)

    def update_user_profiles(self, users):
        if not users:
            return

        values = {
            self.user_profile_key(user['id']): json.dumps(user)
            for user in users
        }
        self.redis.mset(values)

    def user_profile_key(self, user_id):
        return 'user-{}'.format(user_id)

    def fetch_user_profile(self, user_id):
        user_data = self.redis.get(self.user_profile_key(user_id))
        return json.loads(user_data)

    def get_user_name(self, user_id):
        profile = self.fetch_user_profile(user_id)
        return profile['name']
