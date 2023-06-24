from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from workout_app import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Create your views here.
class UserList(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()

        return render(request, self.template_name, {"users": users})


class WorkoutList(View):    
# List workouts by user.id
    template_name = "admin_workout_list.html"
    
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        workout_list = models.Workout.objects.filter(user_id=user_id).order_by('id')
        return render(request, self.template_name, {"workout_list": workout_list})


class WorkoutExerciseList(View):
# List workout_exercises by workout.id
    template_name = "admin_workout_exercise_list.html"

    def get(self, request, *args, **kwargs):
        workout_id = kwargs.get("workout_id")
        workout_exercise_list = models.WorkoutExercise.objects.filter(workout_id=workout_id).order_by('id')
        return render(request, self.template_name, {"workout_exercise_list": workout_exercise_list})


class ExerciseSetList(View):
# List exercise_sets by workout_exercise.id
    def get(self, request, *args, **kwargs):
        workout_exercise_id = kwargs.get("workout_exercise_id")
        exercise_set_list = models.ExerciseSet.objects.filter(workout_exercise_id=workout_exercise_id)
        return render(request, self.template_name, {"exercise_set_list": exercise_set_list})
