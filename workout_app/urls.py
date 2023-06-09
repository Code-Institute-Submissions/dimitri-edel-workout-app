from . import views
from django.urls import path

urlpatterns = [
    path('', views.WorkoutList.as_view(), name='home'),
    path('add_workout', views.AddWorkout.as_view(), name="add_workout"),    
    path('exercise_list', views.ExerciseList.as_view(), name="exercise_list"),
    path('add_exercise', views.AddExercise.as_view(), name="add_exercise"), 
    path('edit_workout/<int:id>', views.EditWorkout.as_view(), name='edit_workout'),  
    path('add_exercise_set/<int:workout_id>', views.AddExerciseSet.as_view(), name='add_exercise_set'),
    path('add_workout_exercise/<int:workout_id>', views.AddWorkoutExercise.as_view(), name='add_workout_exercise'),
]