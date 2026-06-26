from dishka import Scope

from domain.events.user import UserRegistered
from domain.repositories.user_port import UserPort

from .base import register_consumer, ConsumerBase

@register_consumer(UserRegistered)
class UserRegisteredConsumer(ConsumerBase):
    async def execute(self):
        async with self.container(scope=Scope.REQUEST) as req_container:
            users = await req_container.get(UserPort)

            user_id = self.body['payload']['user_id']
            user = await users.find_by_id(user_id)

            user_name = user.full_name
            user_email = user.email

            print(f'Send e-mail to {user_name} with email {user_email}.')
