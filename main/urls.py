from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("base/", views.base, name="base"),
    path("", views.home, name="HBase"),
    path("reg/", views.register_view, name="Register"),
    path("login/", views.login_view, name="log"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", LogoutView.as_view(next_page="HBase"), name="logout"),
    path("search-users/", views.search_users, name="search_users"),
    path("search/", views.search_page, name="search"),
]