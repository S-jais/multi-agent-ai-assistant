from database.db import SessionLocal, Task
import uuid
import datetime

def create_task(title: str):
    db = SessionLocal()
    task = Task(
        id=str(uuid.uuid4()),
        title=title,
        status="pending",
        created_at=datetime.datetime.utcnow()
    )
    db.add(task)
    db.commit()
    db.close()
    return f"Task '{title}' created successfully."

def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()
    return [f"{t.title} ({t.status})" for t in tasks]

def complete_task(title: str):
    db = SessionLocal()
    task = db.query(Task).filter(Task.title == title).first()
    if task:
        task.status = "completed"
        db.commit()
        db.close()
        return f"Task '{title}' marked as completed."
    db.close()
    return "Task not found."