from django.urls import path
from . import views

urlpatterns = [
    path("base/", views.base, name="base"),
    path("", views.home, name="HBase"),
    path("reg/", views.register_view, name="Register"),
    path("login/", views.login_view, name="log"),
]