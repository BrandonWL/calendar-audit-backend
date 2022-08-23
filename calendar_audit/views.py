import json
from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.views import View

from calendar_audit.api import get_calendars

if TYPE_CHECKING:
    from typing import Any

    from django.http import HttpRequest


class AuditView(View):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        data = json.loads(request.body)

        get_calendars(data["code"])
        return HttpResponse("Hello, World!")
