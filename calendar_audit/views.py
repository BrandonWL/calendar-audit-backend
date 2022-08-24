from __future__ import annotations

import json
from datetime import datetime
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

# TODO: impl channels. Unable to do push notifications "Note that the Google Calendar API will be able to send notifications to this HTTPS address only if there is a valid SSL certificate installed on your web server."
class AuditView(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        events = Event.objects.filter(user=request.user).values()
        return JsonResponse({"events": list(events)})


class AuthView(View):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        data = json.loads(request.body)

        credentials, id_token = get_credentials(data["code"])

        decoded = jwt.decode(
            id_token,
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

            # TODO: impl some sort event invalidation for new/updated events
            Event.objects.update_or_create(
                id=event["id"],
                defaults={
                    "start": start,
                    "end": end,
                    "user": user,
                    "summary": event["summary"],
                },
            )
        return JsonResponse({"id_token": id_token})


class InsightsView(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        currentMonth = datetime.now().month
        total_times = [
            {
                "month": month,
                "total_time": Event.total_time_by_month(month, request.user),
            }
            for month in range(currentMonth - 2, currentMonth + 1)
        ]
        month_with_most_meetings = Event.month_with_most_meetings(request.user)
        busiest_week = Event.busiest_week(request.user)
        return JsonResponse(
            {
                "totalTimePastThreeMonths": total_times,
                "month_with_most_meetings": month_with_most_meetings,
                "busiestWeek": busiest_week,
            }
        )
