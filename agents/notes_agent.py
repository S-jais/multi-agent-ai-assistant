from database.db import SessionLocal, Note
import uuid
import datetime

def create_note(content: str):
    db = SessionLocal()
    note = Note(
        id=str(uuid.uuid4()),
        content=content,
        created_at=datetime.datetime.utcnow()
    )
    db.add(note)
    db.commit()
    db.close()
    return "Note saved successfully."

def get_notes():
    db = SessionLocal()
    notes = db.query(Note).all()
    db.close()
    return [n.content for n in notes]