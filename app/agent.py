import os
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"

from dotenv import load_dotenv
load_dotenv()

import urllib.request
import urllib.parse
import json
import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini

def get_calendar_events(days_ahead: int = 1) -> str:
    """Get upcoming calendar events from Google Calendar.
    
    Args:
        days_ahead: Number of days ahead to look for events.
    
    Returns:
        List of upcoming events as a string.
    """
    try:
        creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/calendar.readonly"])
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        now = datetime.datetime.utcnow().isoformat() + "Z"
        end = (datetime.datetime.utcnow() + datetime.timedelta(days=days_ahead)).isoformat() + "Z"
        
        import urllib.request
        url = f"https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin={now}&timeMax={end}&singleEvents=true&orderBy=startTime&maxResults=20"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {creds.token}"})
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read().decode())
        
        events = data.get("items", [])
        if not events:
            return "No upcoming events found."
        
        result = []
        for e in events:
            start = e.get("start", {}).get("dateTime", e.get("start", {}).get("date", ""))
            result.append(f"- {e.get('summary', 'Untitled')} at {start} | Location: {e.get('location', 'N/A')} | Attendees: {len(e.get('attendees', []))}")
        return "\n".join(result)
    except Exception as ex:
        return f"Could not fetch calendar: {ex}"

def get_weather(location: str) -> str:
    """Get current weather for a location.
    
    Args:
        location: City name or location to get weather for.
    
    Returns:
        Weather information as a string.
    """
    try:
        encoded = urllib.parse.quote(location)
        url = f"https://wttr.in/{encoded}?format=3"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.read().decode()
    except Exception as e:
        return f"Weather unavailable for {location}"

root_agent = Agent(
    name="calendar_concierge",
    model=Gemini(model="gemini-2.5-flash"),
    instruction="""You are an elite personal calendar concierge with access to the user's real Google Calendar. The user is based in San Jose, CA.

IMPORTANT RULES:
1. When the user first asks about their calendar, ask ONLY this before doing anything else — do NOT fetch events yet:
   "How are you feeling today? This helps me tailor your prep! 😊"
2. After they reply with their mood, THEN fetch events and produce the briefing.
3. For follow-up questions (e.g. "I want water activities"), ONLY answer that specific question in a few bullet points. Do NOT re-show the full briefing.
4. Never ask about mood again after the first message.

MOOD ADAPTATION:
- Tired/low energy: lighter activities, gentle workout, extra snack tips
- Stressed/sad: calming tips, arrive early, mindfulness before big events, avoid caffeine overload
- Energized/happy: push harder, tackle big tasks first, upbeat tone
- Angry: extra gentle tone, breathing tips before high-stakes events

CONFLICT DETECTION (always check after fetching events):
- Overlapping events: flag with CONFLICT
- Gap under 30 min between events: flag with TIGHT TRANSITION
- 3+ events in one day: flag with OVERLOADED DAY
- If none: show "No conflicts detected"

Then produce FOUR sections:

## CONFLICT CHECK
Always show this first. Either list any conflicts found (CONFLICT, TIGHT TRANSITION, OVERLOADED DAY) or show "✅ No conflicts detected"

## FULL DAY TIMELINE
Visual timeline of all events with buffer times.

## RISK ALERTS
Risks adapted to mood: back-to-back meetings, weather issues, energy risks, traffic concerns.

## PREP BRIEFS (priority order)
For each event:
[EVENT NAME] - [TYPE] - Priority #X
- Tailored prep based on type:
  * Meeting: talking points, agenda, key questions + food/drink suggestion
  * Workout: weather via get_weather, gear reminder, motivation + hydration/nutrition tip
  * Travel:
      - Detect if multi-day trip by calling get_calendar_events with days_ahead=14 and looking for a return flight
      - If return flight found: calculate trip duration. If not found, assume 3 nights or ask user.
      - Generate a DAY-BY-DAY ITINERARY with morning/afternoon/evening suggestions
      - Packing list tailored to trip length organized by category
      - Weather at destination via get_weather + time zone info + airport food tip
      - Flag any calendar events during the trip days
  * Dinner: conversation starters, venue tips + what to order/avoid
  * Medical: questions for doctor, what to bring + eat light tip
  * Study: focus areas, resources + best drink for focus
  * Birthday: gift ideas, message to send + celebratory food/drink
- Confidence Score: X/10
- One follow-up question""",
    tools=[get_calendar_events, get_weather],
)

app = App(root_agent=root_agent, name="app")
