from . import views
from django.urls import path

urlpatterns = [
    path("home/", views.UserList.as_view(), name="admin-home"),
    path("admin_workout_list/<int:user_id>", views.WorkoutList.as_view(), name="admin_workout_list"),
]