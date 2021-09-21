from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("library", views.library_view, name="library"),
    path("comparer", views.comparer_view, name="comparer"),
    path("about_us", views.about_us_view, name="about_us"),
    path("contact_us", views.contact_us_view, name="contact_us"),
    path("profile", views.profile_view, name="profile"),
    path("settings", views.settings_view, name="settings")
]