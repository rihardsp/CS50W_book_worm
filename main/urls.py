from django.urls import path
from . import views
from .views import ChangePasswordView

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("library", views.library_view, name="library"),
    path("comparer", views.comparer_view, name="comparer"),
    path("about_us", views.about_us_view, name="about_us"),
    path("contact_us", views.contact_us_view, name="contact_us"),
    path("settings", views.settings_view, name="settings"),
    path('password-change', ChangePasswordView.as_view(), name='password_change'),

    
    #API Paths
    path("book/<str:book_key>/<str:book_id>", views.book_view, name="settings"),
    path("library-toggle", views.book_toogle, name="book_toogle"),
    path("save_post", views.save_post, name="book_toogle"),
]