from __future__ import print_function

import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import environ
import jwt
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


def get_credentials(code: str) -> Credentials:

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

    return Credentials(
        None,
        refresh_token=data["refresh_token"],
        id_token=data["id_token"],
        token_uri="https://accounts.google.com/o/oauth2/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=SCOPES,
    )

    # # creds = None
    # # # The file token.json stores the user's access and refresh tokens, and is
    # # # created automatically when the authorization flow completes for the first
    # # # time.
    # # if os.path.exists("token2.json"):
    # #     creds = Credentials.from_authorized_user_file("token2.json", SCOPES)

    # creds = get_credentials(code)

    # with open("token2.json", "w") as token:
    #     token.write(creds.to_json())


def get_events(credentials: Credentials) -> None:

    service: Resource = build("calendar", "v3", credentials=credentials)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    response = (
        service.events()
        .list(
            calendarId="primary",
            timeMax=now,
            maxResults=100,
            singleEvents=True,
            orderBy="updated",
        )
        .execute()
    )

    events = response.get("items", [])

    if not events:
        return

    return events


if __name__ == "__main__":
    code = "4/0AdQt8qiAZMzMctbWYepH-d-EpuucRkwWwSKi1Etz4tH_RbacEkjtonSxniUB1GYVu07xfQ"
    get_events(code)


# # 1
# {
#     "kind": "calendar#event",
#     "etag": '"3322415240808000"',
#     "id": "0omql2q5s2nml19b93nq5u7r0j",
#     "status": "confirmed",
#     "htmlLink": "https://www.google.com/calendar/event?eid=MG9tcWwycTVzMm5tbDE5YjkzbnE1dTdyMGogYXRvbWljZGVmaW5pdGlvbkBt",
#     "created": "2022-08-22T22:33:40.000Z",
#     "updated": "2022-08-22T22:33:40.404Z",
#     "summary": "1",
#     "creator": {"email": "atomicdefinition@gmail.com", "self": True},
#     "organizer": {"email": "atomicdefinition@gmail.com", "self": True},
#     "start": {"dateTime": "2022-08-23T06:15:00-07:00", "timeZone": "America/New_York"},
#     "end": {"dateTime": "2022-08-23T08:00:00-07:00", "timeZone": "America/New_York"},
#     "iCalUID": "0omql2q5s2nml19b93nq5u7r0j@google.com",
#     "sequence": 0,
#     "reminders": {"useDefault": True},
#     "eventType": "default",
# }

# # 2
# {
#     "kind": "calendar#event",
#     "etag": '"3322600259102000"',
#     "id": "0omql2q5s2nml19b93nq5u7r0j",
#     "status": "confirmed",
#     "htmlLink": "https://www.google.com/calendar/event?eid=MG9tcWwycTVzMm5tbDE5YjkzbnE1dTdyMGogYXRvbWljZGVmaW5pdGlvbkBt",
#     "created": "2022-08-22T22:33:40.000Z",
#     "updated": "2022-08-24T00:15:29.551Z",
#     "summary": "1",
#     "creator": {"email": "atomicdefinition@gmail.com", "self": True},
#     "organizer": {"email": "atomicdefinition@gmail.com", "self": True},
#     "start": {"dateTime": "2022-08-23T06:30:00-07:00", "timeZone": "America/New_York"},
#     "end": {"dateTime": "2022-08-23T08:15:00-07:00", "timeZone": "America/New_York"},
#     "iCalUID": "0omql2q5s2nml19b93nq5u7r0j@google.com",
#     "sequence": 1,
#     "reminders": {"useDefault": True},
#     "eventType": "default",
# }

# # 3
# {
#     "kind": "calendar#event",
#     "etag": '"3322600360571000"',
#     "id": "0omql2q5s2nml19b93nq5u7r0j",
#     "status": "confirmed",
#     "htmlLink": "https://www.google.com/calendar/event?eid=MG9tcWwycTVzMm5tbDE5YjkzbnE1dTdyMGogYXRvbWljZGVmaW5pdGlvbkBt",
#     "created": "2022-08-22T22:33:40.000Z",
#     "updated": "2022-08-24T00:16:20.361Z",
#     "summary": "1",
#     "creator": {"email": "atomicdefinition@gmail.com", "self": True},
#     "organizer": {"email": "atomicdefinition@gmail.com", "self": True},
#     "start": {"date": "2022-08-23"},
#     "end": {"date": "2022-08-24"},
#     "iCalUID": "0omql2q5s2nml19b93nq5u7r0j@google.com",
#     "sequence": 2,
#     "reminders": {"useDefault": False},
#     "eventType": "default",
# }
