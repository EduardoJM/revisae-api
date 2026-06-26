from domain.events.subject import SubjectCreated

from .base import register_consumer, ConsumerBase

@register_consumer(SubjectCreated)
class UserRegisteredConsumer(ConsumerBase):
    async def execute(self):
        subject_id = self.body['payload']['subject_id']
        user_id = self.body['payload']['user_id']
        subject_name = self.body['payload']['subject_name']

        print(f'Send notification to {user_id} to create contents on {subject_id}/{subject_name}.')
