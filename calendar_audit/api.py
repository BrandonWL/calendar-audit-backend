from __future__ import print_function

import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import environ
import jwt
from django.utils.dateparse import parse_datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import request

if TYPE_CHECKING:
    from googleapiclient.discovery import Resource

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
env = environ.Env()
env.read_env(str(ROOT_DIR / ".env.local"))

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

CUR_DIR = Path(__file__).resolve(strict=True).parent
CLIENT_ID = env("CLIENT_ID")
CLIENT_SECRET = env("CLIENT_SECRET")
REDIRECT_URI = env("REDIRECT_URI")


def get_credentials(code: str) -> tuple[Credentials, str]:

    # get refresh token/access token from access code
    url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "".join(SCOPES),
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    headers = {"content-type": "application/x-www-form-urlencoded"}

    response = request("POST", url, data=data, headers=headers)
    data = response.json()

    return (
        Credentials(
            None,
            refresh_token=data["refresh_token"],
            token_uri="https://accounts.google.com/o/oauth2/token",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scopes=SCOPES,
        ),
        data["id_token"],  # have to return tuple. class Credentials bug
    )


def duration(end: datetime, start: datetime):
    timediff = end - start
    timediff_in_s = timediff.total_seconds()
    return timediff_in_s / 3600


def get_events(credentials: Credentials) -> None:

    service: Resource = build("calendar", "v3", credentials=credentials)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    response = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=user.last_updated,
            maxResults=1000,
            singleEvents=True,
            orderBy="updated",
        )
        .execute()
    )

    events = response.get("items", [])

    if not events:
        return

    filtered_events = []
    for event in events:
        # Is less than 8 hours long.
        start = (
            event["start"]["dateTime"]
            if "dateTime" in event["start"]
            else event["start"]["date"]
        )
        end = (
            event["end"]["dateTime"]
            if "dateTime" in event["end"]
            else event["end"]["date"]
        )
        start_date, end_date = parse_datetime(start), parse_datetime(end)
        total_time = duration(end_date, start_date)

        # TODO: filter based on:
        # You RSVP’d "Yes" to attend.
        # filter attendees[].additionalGuests > 0
        if total_time <= 8:
            filtered_events += [event]

    return filtered_events
