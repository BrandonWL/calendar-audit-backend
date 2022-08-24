from django.urls import path

from .views import AuditView, AuthView

urlpatterns = [
    path("calendar-audit/", AuditView.as_view()),
    path("auth/", AuthView.as_view()),
]
