from database.db import SessionLocal, CalendarEvent
import uuid
import datetime

def create_event(title: str, date: str):
    db = SessionLocal()
    event = CalendarEvent(
        id=str(uuid.uuid4()),
        title=title,
        date=date,
        created_at=datetime.datetime.utcnow()
    )
    db.add(event)
    db.commit()
    db.close()
    return f"Event '{title}' scheduled on {date}."

def get_events():
    db = SessionLocal()
    events = db.query(CalendarEvent).all()
    db.close()
    return [f"{e.title} on {e.date}" for e in events]