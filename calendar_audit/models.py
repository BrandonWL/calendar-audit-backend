from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Max, Sum
from django.db.models.functions import ExtractMonth, ExtractWeek, TruncMonth

# Create your models here.
# POSSIBLY USE DATACLASS instead of saving to db!!!!!!
# the model will hold calendar info and have methods !!!!!!!!!!
# like get last 3
# get total hours spent in meeting fom past month... etc


class Event(models.Model):
    id = models.CharField(primary_key=True, max_length=254, unique=True, db_index=True)
    summary = models.CharField(max_length=256)
    start = models.DateTimeField()
    end = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_time_hours(self) -> float:
        timediff = self.end - self.start
        timediff_in_s = timediff.total_seconds()
        return timediff_in_s / 3600

    # 1
    @classmethod
    def total_time_by_month(cls, month: int, user: User) -> float:
        events = cls.objects.filter(
            start__month=month, start__year=datetime.now().year, user=user
        )
        return sum(event.total_time for event in events)

    # 2
    @classmethod
    def month_with_most_meetings(cls, user: User) -> int:
        event_counts = (
            Event.objects.filter(user=user, start__year=datetime.now().year)
            .annotate(month=ExtractMonth("start"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by()
            # .first()
        )

        most_month = event_counts.order_by("-count").values("month", "count").first()
        return most_month["month"]

    # 3
    @classmethod
    def busiest_week(cls, user: User) -> tuple[int, float]:
        event_counts = (
            Event.objects.filter(user=user, start__year=datetime.now().year)
            .annotate(week=ExtractWeek("start"))
            .values("week")
            .annotate(count=Count("id"))
            .order_by()
            # .first()
        )
        print(event_counts.values("week", "count"))
        most_week = event_counts.order_by("-count").values("week", "count").first()
        print(most_week)
        return most_week["week"]


class Atendee(models.Model):
    id = models.CharField(primary_key=True, max_length=254, unique=True, db_index=True)
    email = models.CharField(max_length=256)
    displayName = models.DateTimeField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
