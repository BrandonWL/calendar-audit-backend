from django.urls import path

from .views import AuditView

urlpatterns = [
    path("calendar-audit/", AuditView.as_view()),
]
