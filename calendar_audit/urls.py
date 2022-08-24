from django.urls import path

from .views import AuditView, AuthView, InsightsView

urlpatterns = [
    path("calendar-audit/", AuditView.as_view()),
    path("auth/", AuthView.as_view()),
    path("insights/", InsightsView.as_view()),
]
