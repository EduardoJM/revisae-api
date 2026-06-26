from dishka import Scope

from domain.events.subject import SubjectCreated
from domain.repositories.subject_port import SubjectPort
from domain.repositories.user_port import UserPort

from .base import register_consumer, ConsumerBase

@register_consumer(SubjectCreated)
class UserRegisteredConsumer(ConsumerBase):
    async def execute(self):
        async with self.container(scope=Scope.REQUEST) as req_container:
            subjects = await req_container.get(SubjectPort)
            users = await req_container.get(UserPort)

            subject_id = self.body['payload']['subject_id']
            user_id = self.body['payload']['user_id']
            
            subject = await subjects.find_by_id(subject_id)
            user = await users.find_by_id(user_id)

            user_name = user.full_name
            subject_name = subject.name

            print(f'Send notification to {user_name} to create contents on {subject_name}.')
