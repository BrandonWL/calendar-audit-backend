from __future__ import print_function

import datetime
from pathlib import Path

import environ
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import request

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
env = environ.Env()
env.read_env(str(ROOT_DIR / ".env.local"))

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

CUR_DIR = Path(__file__).resolve(strict=True).parent


def get_credentials(code: str) -> Credentials:

    # get refresh token/access token from access code
    url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": env("CLIENT_ID"),
        "client_secret": env("CLIENT_SECRET"),
        "scope": "".join(SCOPES),
        "redirect_uri": env("REDIRECT_URI"),
    }
    headers = {"content-type": "application/x-www-form-urlencoded"}

    response = request("POST", url, data=data, headers=headers)
    data = response.json()

    return Credentials(
        None,
        refresh_token=data["refresh_token"],
        token_uri="https://accounts.google.com/o/oauth2/token",
        client_id=env("CLIENT_ID"),
        client_secret=env("CLIENT_SECRET"),
        scopes=SCOPES,
    )


def get_calendars(code: str) -> None:
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    creds = get_credentials(code)

    with open("token2.json", "w") as token:
        token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print("An error occurred: %s" % error)


if __name__ == "__main__":
    code = "4/0AdQt8qiAZMzMctbWYepH-d-EpuucRkwWwSKi1Etz4tH_RbacEkjtonSxniUB1GYVu07xfQ"
    get_calendars(code)
