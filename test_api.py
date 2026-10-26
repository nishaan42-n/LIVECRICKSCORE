"""Test configured Cricbuzz endpoints. Run: python test_api.py"""
from utils.api_client import (
    fetch_live_matches, fetch_upcoming_matches, fetch_recent_matches,
)


def check(label, fetch):
    result = fetch()
    print(f"\n--- {label} ---")
    print("Success:", result.get("ok"))
    print("HTTP status:", result.get("status"))
    if result.get("ok"):
        print("Response preview:", str(result.get("data"))[:1000])
    else:
        print("Error:", result.get("error"))


if __name__ == "__main__":
    check("Upcoming Matches", fetch_upcoming_matches)
    check("Live Matches", fetch_live_matches)
    check("Recent Matches", fetch_recent_matches)
