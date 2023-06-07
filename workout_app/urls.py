from . import views
from django.urls import path

urlpatterns = [
    path('', views.WorkoutList.as_view(), name='home'),
    path('/add_workout', views.Workout.as_view(), name="add_workout"),
]