import sqlmodel
import sqlite3
import logging
import uuid
import time
import os

logger = logging.getLogger(__name__)
_engine = sqlmodel.create_engine("sqlite:///main.db")

def int_time(): return int(time.time())
def str_uuid4(): return str(uuid.uuid4())

class User(sqlmodel.SQLModel, table=True):
    user_id: int = sqlmodel.Field(primary_key=True) # required
    period1: str | None = None
    period2: str | None = None
    period3: str | None = None
    period4: str | None = None
    period5: str | None = None
    period6: str | None = None

class EventDate(sqlmodel.SQLModel, table=True):
    event_uuid: str = sqlmodel.Field(primary_key=True, default_factory=str_uuid4)
    span: bool = False
    start_time: int # required
    end_time: int | None = None
    name: str = "Event Title"
    description: str = "No event description provided"
    approved: bool = False
    created_by: int | None = None
    created_at: int = sqlmodel.Field(default_factory=int_time)
    approved_by: int | None = None
    approved_at: int | None = None

class Rule(sqlmodel.SQLModel, table=True):
    rule_uuid: str = sqlmodel.Field(primary_key=True, default_factory=str_uuid4)
    rule_number: int = sqlmodel.Field(unique=True, index=True)
    title: str = "Rule Title"
    description: str = "No rule description provided"
    created_by: int | None = None
    created_at: int = sqlmodel.Field(default_factory=int_time)

class GenericValues(sqlmodel.SQLModel, table=True):
    key: str = sqlmodel.Field(primary_key=True) # required
    value: str | None = None

sqlmodel.SQLModel.metadata.create_all(_engine)


# generic db operations
def backupdb():
    os.makedirs("db_backups", exist_ok=True)
    # write this later
    
def cleanup():
    _engine.dispose()


# schedule management
def serialize_schedule(schedule: dict[int, str | None], user: User):
    for i in range(1,7):
        class_id = schedule.get(i)
        if class_id is not None:
            setattr(
                user,
                f"period{i}",
                class_id
            )

    return user

def deserialize_schedule(user: User):
    if user is None:
        user = User(user_id=0)

    schedule = dict()
    for i in range(1,7):
        schedule[i] = getattr(
            user,
            f"period{i}"
        )
    return schedule

def save_user_schedule(schedule: dict[int, str | None], user_id: int):
    logger.debug(f"Saving user schedule; Schedule: {schedule}\n\nUser ID: {user_id}")
    with sqlmodel.Session(_engine) as session:
        user = session.get(User, user_id)
        if user is None: user = User(user_id=user_id)
        serialize_schedule(schedule=schedule, user=user)
        session.add(user)

        try:
            session.commit()
            return True
        except:
            logger.exception(f"Failed to save schedule to DB; User ID: {user_id}")
            session.rollback()
            return False
        
def fetch_user_schedule(user_id: int):
    logger.debug(f"Trying to fetch schedule for user ID {user_id}")
    with sqlmodel.Session(_engine) as session:
        user = session.get(User, user_id)
        return deserialize_schedule(user)

    # return {1: 'ap-world-history', 2: 'h-pre-calculus', 3: 'ap-biology', 4: 'h-english-9', 5: 'adv-pe-1', 6: 'spanish-1'}


# event management
pass


# rule management
def get_greatest_rule_number():
    pass

