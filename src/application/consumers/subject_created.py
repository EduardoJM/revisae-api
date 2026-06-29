from uuid import uuid4
from dishka import Scope

from domain.events.subject import SubjectCreated
from domain.entities.notification import Notification
from domain.repositories.notification_port import NotificationPort

from .base import register_consumer, ConsumerBase

@register_consumer(SubjectCreated)
class UserRegisteredConsumer(ConsumerBase):
    async def execute(self):
        subject_id = self.body['payload']['subject_id']
        user_id = self.body['payload']['user_id']
        subject_name = self.body['payload']['subject_name']

        title = f"Populate the subject {subject_name}"
        content = "Create contents to review and begin using the application."
        notification_id = uuid4()
        notification = Notification(
            notification_id=notification_id,
            user_id=user_id,
            title=title,
            description=content,
            is_readed=False,
        )

        async with self.container(scope=Scope.REQUEST) as req_container:
            notifications = await req_container.get(NotificationPort)
            await notifications.save(notification)

        print(f'Send notification to {user_id} to create contents on {subject_id}/{subject_name}.')
