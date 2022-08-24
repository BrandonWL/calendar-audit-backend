from __future__ import annotations

import json
from typing import TYPE_CHECKING

import jwt
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views import View

from calendar_audit.api import get_credentials, get_events

from .models import Event

if TYPE_CHECKING:
    from typing import Any

    from django.http import HttpRequest

# TODO: verify id_token at protected endpoints
class AuditView(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        JsonResponse([])


class AuthView(View):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        data = json.loads(request.body)

        credentials = get_credentials(data["code"])
        decoded = jwt.decode(
            credentials.id_token,
            algorithms=["RS256"],
            options={"verify_signature": False},
        )
        sub = decoded["sub"]
        user, _ = User.objects.get_or_create(username=sub)
        events = get_events(credentials)

        for event in events:
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
            Event.objects.update_or_create(
                id=event["id"],
                defaults={
                    "start": start,
                    "end": end,
                    "user": user,
                    "summary": event["summary"],
                },
            )
        return JsonResponse({"id_token": credentials.id_token})
