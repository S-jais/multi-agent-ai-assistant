import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

class AgentState(TypedDict):
    messages: List[str]
    current_agent: str
    result: str

def router_node(state: AgentState):
    user_msg = state["messages"][-1].lower()
    if any(w in user_msg for w in ["task", "todo", "remind", "do"]):
        return {**state, "current_agent": "task"}
    elif any(w in user_msg for w in ["note", "write", "save", "remember"]):
        return {**state, "current_agent": "notes"}
    elif any(w in user_msg for w in ["calendar", "schedule", "meeting", "event"]):
        return {**state, "current_agent": "calendar"}
    return {**state, "current_agent": "task"}

def task_agent_node(state: AgentState):
    response = llm.invoke(
        f"You are a task manager assistant. Help the user with: {state['messages'][-1]}"
    )
    return {**state, "current_agent": "task", "result": response.content}

def notes_agent_node(state: AgentState):
    response = llm.invoke(
        f"You are a notes assistant. Help the user with: {state['messages'][-1]}"
    )
    return {**state, "current_agent": "notes", "result": response.content}

def calendar_agent_node(state: AgentState):
    response = llm.invoke(
        f"You are a calendar assistant. Help the user with: {state['messages'][-1]}"
    )
    return {**state, "current_agent": "calendar", "result": response.content}

def route_decision(state: AgentState):
    return state["current_agent"]

graph = StateGraph(AgentState)
graph.add_node("router", router_node)
graph.add_node("task", task_agent_node)
graph.add_node("notes", notes_agent_node)
graph.add_node("calendar", calendar_agent_node)
graph.set_entry_point("router")
graph.add_conditional_edges("router", route_decision, {
    "task": "task",
    "notes": "notes",
    "calendar": "calendar"
})
graph.add_edge("task", END)
graph.add_edge("notes", END)
graph.add_edge("calendar", END)

app_graph = graph.compile()