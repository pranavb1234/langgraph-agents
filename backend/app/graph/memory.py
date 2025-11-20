from app.graph.state import ConversationState

SESSIONS = {}

def load_state(session_id: str):
    if session_id in SESSIONS:
        data = SESSIONS[session_id]
        return ConversationState(**data)
    return ConversationState()

def save_state(session_id: str, state: ConversationState):
    SESSIONS[session_id] = state.dict()
