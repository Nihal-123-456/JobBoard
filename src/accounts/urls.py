from django.urls import path
from .views import register_view, login_view, logout_view, notifications_list, mark_notification_read, delete_notification

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("notifications/", notifications_list, name="notifications"),
    path("notifications/<int:pk>/read/", mark_notification_read, name="notification-read"),
    path("notifications/<int:pk>/delete/", delete_notification, name="notification-delete"),
]
