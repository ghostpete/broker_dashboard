from django.urls import path
from . import views


# app_name = 'api'

urlpatterns = [
    path('login/', views.login_with_email_api, name="login_with_email_api"),
    path("register/", views.register_api_view, name="api_register"),
    path("update-profile-api/", views.update_profile_api_view, name="update_profile_api_view"),
    path("change-password-api/", views.change_password_api_view, name="change_password_api_view"),
    path("support-api/", views.support_api, name="support_api"),
    path("clear-user-notification/", views.clear_user_notification, name="clear_user_notification"),
]
