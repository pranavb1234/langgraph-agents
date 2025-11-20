#!/usr/bin/env python3
"""
Quick tester for booking-com15 RapidAPI endpoints:
1) searchDestination -> get dest_id
2) searchHotels -> get hotels for dest_id

Usage:
  # set env var (recommended)
  export RAPID_API_KEY="your_key_here"
  python test_booking_api.py --city "Paris"

  # OR pass key directly (less secure)
  python test_booking_api.py --city Paris --key your_key_here
"""

import argparse
import os
import sys
import requests
import json
from textwrap import shorten
from datetime import date, timedelta

DEFAULT_HOST = "booking-com15.p.rapidapi.com"

def pretty_print_json(obj, max_chars=2000):
    s = json.dumps(obj, indent=2, ensure_ascii=False)
    print(shorten(s, width=max_chars, placeholder=" ... (truncated)"))

def call_destination_lookup(api_key, city, host=DEFAULT_HOST):
    url = f"https://{host}/api/v1/hotels/searchDestination"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": host,
    }
    params = {"query": city}
    print("\n[DESTINATION] GET", url, "params=", params)
    r = requests.get(url, headers=headers, params=params, timeout=15)
    print("Status:", r.status_code)
    ct = r.headers.get("Content-Type","")
    print("Content-Type:", ct)
    try:
        data = r.json()
    except Exception:
        print("Response is not JSON. Raw body:")
        print(r.text[:4000])
        return None, r
    return data, r

def call_search_hotels(api_key, dest_id, host=DEFAULT_HOST, currency="INR"):
    url = f"https://{host}/api/v1/hotels/searchHotels"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": host,
    }
    arrival = (date.today() + timedelta(days=1)).isoformat()
# use day after tomorrow as check-out
    departure = (date.today() + timedelta(days=3)).isoformat()

    params = {
    "dest_id": str(dest_id),
    "search_type": "CITY",
    "adults": "1",
    "children_age": "0,17",
    "room_qty": "1",
    "page_number": "1",
    "units": "metric",
    "temperature_unit": "c",
    "languagecode": "en-us",
    "currency_code": "INR",
    "location": "US",
    "arrival_date": arrival,
    "departure_date": departure
}
    print("\n[HOTEL SEARCH] GET", url, "params=", params)
    r = requests.get(url, headers=headers, params=params, timeout=100)
    print("Status:", r.status_code)
    ct = r.headers.get("Content-Type","")
    print("Content-Type:", ct)
    try:
        data = r.json()
    except Exception:
        print("Response is not JSON. Raw body:")
        print(r.text[:4000])
        return None, r
    return data, r

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--city", required=True, help="City name to search e.g. Paris")
    p.add_argument("--key", default=None, help="RapidAPI key (optional, env RAPID_API_KEY used if not provided)")
    p.add_argument("--host", default=DEFAULT_HOST, help="RapidAPI host (booking-com15.p.rapidapi.com)")
    p.add_argument("--currency", default="INR", help="Currency code for hotel prices (INR, USD, AED...)")
    args = p.parse_args()

    api_key = args.key or os.environ.get("RAPID_API_KEY") or os.environ.get("RAPID_KEY")
    if not api_key:
        print("ERROR: No RapidAPI key provided. Use --key or set RAPID_API_KEY environment variable.")
        sys.exit(2)

    city = args.city
    host = args.host

    # 1) Destination lookup
    dest_json, dest_resp = call_destination_lookup(api_key, city, host=host)
    if dest_json is None:
        print("Destination lookup failed or returned non-JSON. See above.")
        sys.exit(1)

    # debug: print keys
    print("\nDestination lookup response keys:", list(dest_json.keys())[:10])
    # Look for 'data' key (booking-com15 uses data)
    data_list = dest_json.get("data") or dest_json.get("results") or dest_json.get("items") or None
    if not data_list:
        print("No 'data' (candidate destinations) found in response. Full JSON (truncated):")
        pretty_print_json(dest_json)
        sys.exit(1)

    # show top candidate(s)
    print(f"\nTop {min(5, len(data_list))} destination candidates:")
    for i, entry in enumerate(data_list[:5], start=1):
        # safe access
        print(f"  [{i}] keys: {list(entry.keys())[:8]}")
        # try print common fields if present:
        cname = entry.get("city_name") or entry.get("label") or entry.get("name") or entry.get("caption")
        dest_id = entry.get("dest_id") or entry.get("id") or entry.get("destination_id")
        country = entry.get("country") or entry.get("country_name")
        print(f"      city_name={cname!r} dest_id={dest_id!r} country={country!r}")

    # pick first dest_id
    dest_id = data_list[0].get("dest_id") or data_list[0].get("id") or data_list[0].get("destination_id")
    if not dest_id:
        print("Could not find dest_id in first result. Aborting.")
        pretty_print_json(data_list[0])
        sys.exit(1)

    print("\nUsing dest_id =", dest_id)

    # 2) Hotel search
    hotels_json, hotels_resp = call_search_hotels(api_key, dest_id, host=host, currency=args.currency)
    if hotels_json is None:
        print("Hotel search returned non-JSON. See raw body above.")
        sys.exit(1)

    # show top-level keys
    print("\nHotel search top-level keys:", list(hotels_json.keys())[:20])

    # bookings endpoints often return 'data' list
    # hotels_list = hotels_json.get("data") or hotels_json.get("result") or hotels_json.get("hotels") or None
    # if not hotels_list:
    #     print("No hotels list found in response. Printing truncated JSON for debugging:")
    #     pretty_print_json(hotels_json)
    #     sys.exit(1)
    # ---- FIX: Extract hotels safely ----
    data_field = hotels_json.get("data")

    hotels_list = None

    # Case 1: data is already a list
    if isinstance(data_field, list):
        hotels_list = data_field

    # Case 2: data is a dict (most common in RapidAPI Booking)
    elif isinstance(data_field, dict):
        hotels_list = (
            data_field.get("hotels") or
            data_field.get("result") or
            data_field.get("items") or
            data_field.get("list")
        )

    # Safety check
    if not hotels_list:
        print("\n No hotels list found in API response. RAW JSON:\n")
        pretty_print_json(hotels_json)
        sys.exit(1)

    print("\nDEBUG: FIRST HOTEL RAW JSON:")
    pretty_print_json(hotels_list[0], max_chars=4000)
    print(f"\nFound {len(hotels_list)} hotels (showing top 5):")
    for i, h in enumerate(hotels_list[:5], start=1):
        # extract common fields robustly
        prop = h.get("property", {})

        name = prop.get("name")
        rating = prop.get("reviewScore")

        # Price
        price_info = prop.get("priceBreakdown", {})
        gross = price_info.get("grossPrice", {})
        price = gross.get("value")

        # Address (use accessibilityLabel as fallback)
        address = h.get("accessibilityLabel") or "Address unavailable"

    print("\nDONE. If you see HTTP 401/403/429/500, check API key, subscription, rate limits, or host name.")

if __name__ == "__main__":
    main()
