def coordinator_agent(state):
    msg = state.user_message.lower()

    wants_flight = any(k in msg for k in ["flight", "fly", "air", "plane"])
    wants_hotel = any(k in msg for k in ["hotel", "stay", "room", "accommodation"])

    if wants_flight and wants_hotel:
        state.active_task = "flight_and_hotel"
    elif wants_flight:
        state.active_task = "flight"
    elif wants_hotel:
        state.active_task = "hotel"
    else:
        state.active_task = "unknown"

    return state



def flight_agent(state):
    state.flights = [
        {
            "airline": "IndiGo",
            "price": 45500,
            "depart_time": "2025-01-10 09:00",
            "arrive_time": "2025-01-10 16:20"
        },
        {
            "airline": "Air India",
            "price": 49700,
            "depart_time": "2025-01-10 12:30",
            "arrive_time": "2025-01-10 20:10"
        }
    ]
    return state

def hotel_agent(state):
    state.hotels = [
        {
            "name": "Paris Central Hotel",
            "rating": 4.5,
            "price": 7800,
            "location": "Eiffel Tower"
        },
        {
            "name": "Budget Stay Paris",
            "rating": 4.0,
            "price": 5500,
            "location": "City Center"
        }
    ]
    return state



def presenter_agent(state):
    msg = ""

    if state.flights:
        msg += f"Found {len(state.flights)} flights for your trip.\n"

    if state.hotels:
        msg += f"Found {len(state.hotels)} hotels for your stay.\n"

    if msg == "":
        msg = "I can help you find flights or hotels. Ask me anything!"

    state.reply = msg
    return state

