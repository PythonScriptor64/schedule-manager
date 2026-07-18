import sqlmodel
import sqlite3
import os

_engine = sqlmodel.create_engine("sqlite:///main.db")

class User(sqlmodel.SQLModel, table=True):
    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    period1: str
    period2: str
    period3: str
    period4: str
    period5: str
    period6: str

def backupdb():
    os.mkdir("db_backups")
    # write this later
    
def save_user_schedule(schedule: dict[int, str | None], user_id: int):
    print(f"Schedule: {schedule}\n\nUser ID: {user_id}")
    # write this later

def fetch_user_schedule(user_id: int):
    return {1: 'ap-world-history', 2: 'h-pre-calculus', 3: 'ap-biology', 4: 'h-english-9', 5: 'adv-pe-1', 6: 'spanish-1'}
    # write this later
    # return {}

def cleanup():
    __import__("time").sleep(7)

sqlmodel.SQLModel.metadata.create_all(_engine)