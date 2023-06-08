from . import views
from django.urls import path

urlpatterns = [
    path('', views.WorkoutList.as_view(), name='home'),
    path('add_workout', views.AddWorkout.as_view(), name="add_workout"),
    path('exercise_list', views.ExerciseList.as_view(), name="exercise_list"),
    path('add_exercise', views.AddExercise.as_view(), name="add_exercise"),
]