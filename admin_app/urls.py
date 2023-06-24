from . import views
from django.urls import path

urlpatterns = [
    path("home/", views.UserList.as_view(), name="admin-home"),
    path("admin_workout_list/<int:user_id>", views.WorkoutList.as_view(), name="admin_workout_list"),
    path("admin_workout_exercise_list/<int:workout_id>/<int:user_id>", views.WorkoutExerciseList.as_view(), name="admin_workout_exercise_list"),
    path("admin_exercise_set_list/<int:workout_exercise_id>", views.ExerciseSetList.as_view(), name="admin_exercise_set_list"),
    path("admin_delete_user/<int:user_id>", views.DeleteUser.as_view(), name="admin_delete_user"),
]