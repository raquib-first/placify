from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("fetch/", views.fetch_notifications, name="fetch"),
    path("read/<int:notif_id>/", views.mark_as_read, name="read"),
]
