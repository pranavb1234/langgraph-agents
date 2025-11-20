from fastapi import FastAPI
from app.schemas import ChatRequest, ChatResponse
from app.graph.builder import graph_runner
from app.graph.memory import load_state, save_state
from app.graph.state import ConversationState
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    state = load_state(req.session_id)
    state.user_message = req.message

    result = graph_runner.invoke(state)

    # convert dict → ConversationState
    new_state = ConversationState(**result)

    save_state(req.session_id, new_state)

    return ChatResponse(
        reply=new_state.reply,
        flights=new_state.flights,
        hotels=new_state.hotels
    )

@app.get("/")
def home():
    return {"status": "Travel Assistant Backend Running"}
