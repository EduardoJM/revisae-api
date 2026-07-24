from uuid import uuid4

from domain.value_objects.email import Email
from domain.value_objects.password import HashedPassword
from domain.value_objects.hex_color import HexColor
from domain.entities.user import User
from domain.entities.subject import Subject
from domain.entities.notification import Notification
from domain.entities.revision_cycle import RevisionCycle
from domain.events.user import UserRegistered
from domain.events.subject import SubjectCreated

# --- User

def test_user_register_emits_event():
    email = 'example@example.com.br'
    full_name = 'Example'
    user = User.register(
        user_id=uuid4(),
        email=Email(email),
        hashed_password=HashedPassword('hashed'),
        full_name=full_name
    )
    events = user.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], UserRegistered)
    assert events[0].email == email
    assert events[0].full_name == full_name

def test_collect_user_events_clears_list():
    user = User.register(uuid4(), Email('example@email.com.br'), HashedPassword(''), "Example")
    user.collect_events()
    assert user.collect_events() == []

# --- Subject

def test_create_subject_emits_event():
    user_id = uuid4()
    name = 'My Subject'
    color = HexColor('#fff')
    subject = Subject.create(
        subject_id=uuid4(),
        user_id=user_id,
        name=name,
        color=color,
    )
    events = subject.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], SubjectCreated)
    assert events[0].user_id == user_id
    assert events[0].subject_name == name

def test_collect_subject_events_clears_list():
    subject = Subject.create(subject_id=uuid4(), user_id=uuid4(), name='subject', color=HexColor('#fff'))
    subject.collect_events()
    assert subject.collect_events() == []

def test_subject_belongs_to_wrong():
    user_id = uuid4()
    name = 'My Subject'
    color = HexColor('#fff')
    subject = Subject.create(
        subject_id=uuid4(),
        user_id=user_id,
        name=name,
        color=color,
    )
    
    assert subject.belongs_to(uuid4()) == False

def test_subject_belongs_to_correct():
    user_id = uuid4()
    name = 'My Subject'
    color = HexColor('#fff')
    subject = Subject.create(
        subject_id=uuid4(),
        user_id=user_id,
        name=name,
        color=color,
    )
    
    assert subject.belongs_to(user_id) == True

def test_subject_update_partial_name():
    user_id = uuid4()
    name = 'My Subject'
    color = HexColor('#fff')
    subject = Subject.create(
        subject_id=uuid4(),
        user_id=user_id,
        name=name,
        color=color,
    )
    new_name = 'New Name'

    subject.update(name=new_name)
    
    assert subject.name == new_name
    assert subject.color == color

def test_subject_update_partial_color():
    user_id = uuid4()
    name = 'My Subject'
    color = HexColor('#fff')
    subject = Subject.create(
        subject_id=uuid4(),
        user_id=user_id,
        name=name,
        color=color,
    )
    new_color = HexColor('#000')

    subject.update(color=new_color)
    
    assert subject.name == name
    assert subject.color == new_color

def test_subject_update_name_and_color():
    user_id = uuid4()
    name = 'My Subject'
    color = HexColor('#fff')
    subject = Subject.create(
        subject_id=uuid4(),
        user_id=user_id,
        name=name,
        color=color,
    )
    new_name = 'New Name'
    new_color = HexColor('#000')

    subject.update(name=new_name, color=new_color)
    
    assert subject.name == new_name
    assert subject.color == new_color

# --- Notification

def test_notification_belongs_to_wrong():
    user_id = uuid4()
    title = 'Notification Title'
    description = 'Notification Description'
    notification = Notification(
        notification_id=uuid4(),
        user_id=user_id,
        title=title,
        description=description,
        is_readed=False
    )
    
    assert notification.belongs_to(uuid4()) == False

def test_notification_belongs_to_correct():
    user_id = uuid4()
    title = 'Notification Title'
    description = 'Notification Description'
    notification = Notification(
        notification_id=uuid4(),
        user_id=user_id,
        title=title,
        description=description,
        is_readed=False
    )
    
    assert notification.belongs_to(user_id) == True

def test_notification_mark_as_readed():
    user_id = uuid4()
    title = 'Notification Title'
    description = 'Notification Description'
    notification = Notification(
        notification_id=uuid4(),
        user_id=user_id,
        title=title,
        description=description,
        is_readed=False
    )

    notification.mark_as_readed()
    
    assert notification.is_readed == True

# --- Revision Cycle

def test_revision_cycle_belongs_to_wrong():
    user_id = uuid4()
    rev_cycle = RevisionCycle(
        revision_cycle_id=uuid4(),
        user_id=user_id,
        name='My Name',
        days=[1, 5, 10]
    )

    assert rev_cycle.belongs_to(uuid4()) == False

def test_revision_cycle_belongs_to_correct():
    user_id = uuid4()
    rev_cycle = RevisionCycle(
        revision_cycle_id=uuid4(),
        user_id=user_id,
        name='My Name',
        days=[1, 5, 10]
    )

    assert rev_cycle.belongs_to(user_id) == True

def test_revision_cycle_update_partial_name():
    user_id = uuid4()
    rev_cycle = RevisionCycle(
        revision_cycle_id=uuid4(),
        user_id=user_id,
        name='My Name',
        days=[1, 5, 10]
    )
    new_name = 'New Name Here'

    rev_cycle.update(name=new_name)

    assert rev_cycle.name == new_name

def test_revision_cycle_update_partial_days():
    user_id = uuid4()
    rev_cycle = RevisionCycle(
        revision_cycle_id=uuid4(),
        user_id=user_id,
        name='My Name',
        days=[1, 5, 10]
    )
    new_days = [10, 20, 30]

    rev_cycle.update(days=new_days)

    assert rev_cycle.days == new_days

def test_revision_cycle_update_name_and_days():
    user_id = uuid4()
    rev_cycle = RevisionCycle(
        revision_cycle_id=uuid4(),
        user_id=user_id,
        name='My Name',
        days=[1, 5, 10]
    )
    new_name = 'New Name Here'
    new_days = [10, 20, 30]

    rev_cycle.update(name=new_name, days=new_days)

    assert rev_cycle.name == new_name
    assert rev_cycle.days == new_days
