from langgraph.graph import StateGraph, END
from app.graph.state import ConversationState
from app.graph.agents import coordinator_agent, flight_agent, hotel_agent, presenter_agent

# def route_from_coordinator(state):
#     if state.active_task == "flight":
#         return "flight"
#     if state.active_task == "hotel":
#         return "hotel"
#     if state.active_task == "flight_and_hotel":
#         return ["flight", "hotel"]
#     return "presenter"

def route_from_coordinator(state):
    print("EDGE ROUTER RECEIVED TASK:", state.active_task)

    if state.active_task == "hotel":
        return "hotel"

    if state.active_task == "flight":
        return "flight"

    if state.active_task == "flight_and_hotel":
        return ["flight", "hotel"]

    return "presenter"


def build_graph():
    builder = StateGraph(ConversationState)

    builder.add_node("coordinator", coordinator_agent)
    builder.add_node("flight", flight_agent)
    builder.add_node("hotel", hotel_agent)
    builder.add_node("presenter", presenter_agent)

    builder.set_entry_point("coordinator")
    builder.add_conditional_edges("coordinator", route_from_coordinator)

    builder.add_edge("flight", "presenter")
    builder.add_edge("hotel", "presenter")
    builder.add_edge("presenter", END)

    return builder.compile()

graph_runner = build_graph()
