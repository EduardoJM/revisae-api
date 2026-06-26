from domain.events.user import UserRegistered

from .base import register_consumer, ConsumerBase

@register_consumer(UserRegistered)
class UserRegisteredConsumer(ConsumerBase):
    async def execute(self):
        user_id = self.body['payload']['user_id']
        user_name = self.body['payload']['full_name']
        user_email = self.body['payload']['email']

        print(f'Send e-mail to {user_id}/{user_name} with email {user_email}.')
