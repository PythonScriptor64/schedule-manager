import sqlmodel
import sqlite3
import uuid
import time
import os

_engine = sqlmodel.create_engine("sqlite:///main.db")

def int_time(): return int(time.time())
def str_uuid4(): return str(uuid.uuid4())

class User(sqlmodel.SQLModel, table=True):
    uid: int = sqlmodel.Field(primary_key=True) # required
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

# generic db operations
def backupdb():
    os.makedirs("db_backups", exist_ok=True)
    # write this later
    
def cleanup():
    __import__("time").sleep(7)

# schedule management
def save_user_schedule(schedule: dict[int, str | None], user_id: int):
    print(f"Schedule: {schedule}\n\nUser ID: {user_id}")
    # write this later

def fetch_user_schedule(user_id: int):
    return {1: 'ap-world-history', 2: 'h-pre-calculus', 3: 'ap-biology', 4: 'h-english-9', 5: 'adv-pe-1', 6: 'spanish-1'}
    # write this later
    # return {}

# event management
pass

# rule management
def get_greatest_rule_number():
    pass



sqlmodel.SQLModel.metadata.create_all(_engine)