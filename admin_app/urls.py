from . import views
from django.urls import path

urlpatterns = [
    path("home/", views.UserList.as_view(), name="admin-home"),
]