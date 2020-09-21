import base64
import os
import os.path
import pickle
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CALENDAR_ID = os.getenv("CALENDAR_ID")


def _base64_encode_logo(logo_path: str):
    with open(logo_path, "br") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return encoded


MEET_ICON_BASE64 = _base64_encode_logo("img/meet.png")
STREAM_ICON_BASE64 = _base64_encode_logo("img/stream.png")


def main():
    creds = _get_creds()
    event = _get_event_(creds)

    if event is None:
        return

    name, start_time, hangout_link, stream_uri = _parse_event(event)

    if hangout_link is not None:
        icon = MEET_ICON_BASE64
        href = hangout_link
    elif stream_uri is not None:
        icon = STREAM_ICON_BASE64
        href = stream_uri
    else:
        icon = None
        href = None

    print(f"{start_time} {name}|image={icon} href={href} size=12")


def _parse_event(event: Dict) -> (str, str, Optional[str], Optional[str]):
    name = event["summary"]
    start = event["start"]["dateTime"]
    # TODO get these mtg url from `conferenceData`, and identify `meet` or `stream` from the url
    hangout_link = event.get("hangoutLink")
    conference_data = event.get("conferenceData")
    stream_uri = conference_data["entryPoints"][0]["uri"] if conference_data is not None else None

    # extract HH::mm from ISO8601 time
    import re

    m = re.search(r"\d{4}-\d{2}-\d{2}T(\d{2}:\d{2}):\d{2}\+\d{2}:\d{2}", start)
    start_time = m.groups()[0]

    return name, start_time, hangout_link, stream_uri


def _get_event_(creds):
    service = build("calendar", "v3", credentials=creds)
    now = datetime.now(timezone.utc)

    # python datetime not support `Z` suffix format for UTC, so use `replace`
    events_result = (
        service.events()
        .list(
            calendarId=CALENDAR_ID,
            timeMin=now.isoformat().replace("+00:00", "Z"),
            timeMax=(now + timedelta(hours=24)).isoformat().replace("+00:00", "Z"),
            maxResults=1,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if events is None:
        print("No upcoming events found.")
        return

    return events[0]


def _get_creds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


if __name__ == "__main__":
    main()
