from fastapi import FastAPI
from pydantic import BaseModel
from agents.orchestrator import router_node
from agents.task_agent import create_task, get_tasks, complete_task
from agents.calendar_agent import create_event, get_events
from agents.notes_agent import create_note, get_notes

app = FastAPI()

class UserInput(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "AI Agent is running 🚀"}

@app.post("/chat")
def chat(input: UserInput):
    user_msg = input.message.lower()

    # TASKS
    if "add task" in user_msg:
        title = user_msg.replace("add task", "").strip()
        return {"response": create_task(title)}

    elif "show tasks" in user_msg:
        return {"response": get_tasks()}

    elif "complete task" in user_msg:
        title = user_msg.replace("complete task", "").strip()
        return {"response": complete_task(title)}

    # CALENDAR
    elif "schedule" in user_msg:
        parts = user_msg.replace("schedule", "").strip().split(" on ")
        if len(parts) == 2:
            return {"response": create_event(parts[0], parts[1])}
        return {"response": "Invalid format. Use: schedule meeting on 2026-04-10"}

    elif "show events" in user_msg:
        return {"response": get_events()}

    # NOTES
    elif "note" in user_msg:
        content = user_msg.replace("note", "").strip()
        return {"response": create_note(content)}

    elif "show notes" in user_msg:
        return {"response": get_notes()}

    return {"response": "Sorry, I didn't understand that."}