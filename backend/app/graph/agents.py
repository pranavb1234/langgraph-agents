import requests

RAPID_KEY = "31ff30136dmsh45a242a9ed5bfc1p120493jsna730f50f325f"


def get_destination_id(city: str):
    """
    Looks up destination_id for a city using Booking.com API.
    """
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"

    params = {"query": city}

    headers = {
        "x-rapidapi-key": RAPID_KEY,
        "x-rapidapi-host": "booking-com15.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if "data" not in data or len(data["data"]) == 0:
            return None

        return data["data"][0]["dest_id"]

    except Exception as e:
        print("Error fetching destination ID:", e)
        return None

# def coordinator_agent(state):
#     msg = state.user_message.lower()

#     wants_flight = any(k in msg for k in ["flight", "flights", "fly", "air", "plane"])
#     wants_hotel = any(k in msg for k in ["hotel", "hotels", "stay", "room", "accommodation"])

#     if wants_flight and wants_hotel:
#         state.active_task = "flight_and_hotel"
#     elif wants_flight:
#         state.active_task = "flight"
#     elif wants_hotel:
#         state.active_task = "hotel"
#     else:
#         state.active_task = "unknown"

#     return state

# def coordinator_agent(state):
#     msg = state.user_message.lower()
#     print("COORDINATOR RECEIVED:", msg)      # DEBUG

#     wants_flight = any(k in msg for k in ["flight", "flights", "fly", "air", "plane"])
#     wants_hotel = any(k in msg for k in ["hotel", "hotels", "stay", "room", "accommodation"])
    
#     print("DETECTED wants_hotel:", wants_hotel)   # DEBUG

#     if wants_flight and wants_hotel:
#         state.active_task = "flight_and_hotel"
#     elif wants_flight:
#         state.active_task = "flight"
#     elif wants_hotel:
#         state.active_task = "hotel"
#     else:
#         state.active_task = "unknown"

#     print("ROUTING TO:", state.active_task)   # DEBUG
    
#     return state

def coordinator_agent(state):
    msg = state.user_message.lower()

    print("COORDINATOR RECEIVED:", msg)

    wants_flight = any(k in msg for k in ["flight", "flights", "fly", "air", "plane"])
    wants_hotel = any(k in msg for k in ["hotel", "hotels", "stay", "room", "accommodation"])

    print("DETECTED wants_hotel:", wants_hotel)

    # --- ROUTING LOGIC ---
    if wants_flight and wants_hotel:
        state.active_task = "flight_and_hotel"
    elif wants_flight:
        state.active_task = "flight"
    elif wants_hotel:
        state.active_task = "hotel"
    else:
        state.active_task = "unknown"

    print("ROUTING TO:", state.active_task)
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
    dest_id = state.trip.destination_id  # MUST exist
    if not dest_id:
        state.reply = "Destination ID missing. Please specify a city."
        return state

    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"

    params = {
        "dest_id": dest_id,
        "search_type": "CITY",
        "adults": "1",
        "children_age": "0,17",
        "room_qty": "1",
        "page_number": "1",
        "units": "metric",
        "temperature_unit": "c",
        "languagecode": "en-us",
        "currency_code": "INR",
        "location": "US"
    }

    headers = {
        "x-rapidapi-key": RAPID_KEY,
        "x-rapidapi-host": "booking-com15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Parse hotel results
    hotels = data.get("data", [])
    if not hotels:
        state.reply = "No hotels found."
        return state

    state.hotels = [
        {
            "name": h.get("hotel_name"),
            "rating": h.get("review_score"),
            "price": h.get("min_total_price"),
            "location": h.get("address"),
        }
        for h in hotels[:3]
    ]

    state.reply = f"Found {len(state.hotels)} hotels."
    print("🔥 HOTEL AGENT CALLED")
    print("CITY =", state.trip.destination)
    print("CHECKIN =", state.trip.depart_date)
    print("CHECKOUT =", state.trip.return_date)
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

