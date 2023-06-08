from . import views
from django.urls import path

urlpatterns = [
    path('', views.WorkoutList.as_view(), name='home'),
    path('add_workout', views.AddWorkout.as_view(), name="add_workout"),
    path('add_exercise', views.AddExercise.as_view(), name="add_exercise"),
]