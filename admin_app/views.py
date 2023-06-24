from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from workout_app import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import CreateUserForm
from django.db import IntegrityError
from django.contrib import messages


# Create your views here.
class UserList(View):
    template_name = "home.html"
    create_user_form_class = CreateUserForm

    def get(self, request, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()
        create_user_form = self.create_user_form_class()

        return render(request, self.template_name, {"users": users, "create_user_form": create_user_form})

    def post(self, request, *args, **kwargs):
        self.__create_user(request)
        seach_user = request.POST.get('search_user', "")
        create_user_form = self.create_user_form_class()
        User = get_user_model()
        users = User.objects.all()
        user_list = []
        for user in users:
            if seach_user in user.username:
                user_list.append(user)

        return render(request, self.template_name, {"users": user_list, "create_user_form": create_user_form})

    def __create_user(self, request):
        create_user_form = self.create_user_form_class(request.POST)        
        if create_user_form.is_valid():
            try:
                user_name = create_user_form.cleaned_data['username']
                password = create_user_form.cleaned_data['password1']
                User.objects.create_user(username=user_name,
                                 password=password)
            except IntegrityError:
                messages.add_message(
                request, messages.ERROR, "The username already exists!")
        return


class WorkoutList(View):    
# List workouts by user.id
    template_name = "admin_workout_list.html"

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = User.objects.get(id=user_id)
        workout_list = models.Workout.objects.filter(user_id=user_id).order_by('id')
        return render(request, self.template_name, {"workout_list": workout_list, "user": user})


class WorkoutExerciseList(View):
# List workout_exercises by workout.id
    template_name = "admin_workout_exercise_list.html"

    def get(self, request, *args, **kwargs):
        workout_id = kwargs.get("workout_id")
        user_id = kwargs.get("user_id")
        user = User.objects.get(id=user_id)

        workout_exercise_list = models.WorkoutExercise.objects.filter(workout_id=workout_id).order_by('id')
        return render(request, self.template_name, {"workout_exercise_list": workout_exercise_list, "user": user})


class ExerciseSetList(View):
# List exercise_sets by workout_exercise.id
    template_name = "admin_exercise_set_list.html"

    def get(self, request, *args, **kwargs):        
        workout_exercise_id = kwargs.get("workout_exercise_id")
        workout_exercise = models.WorkoutExercise.objects.get(id=workout_exercise_id)
        exercise = workout_exercise.exercise
        exercise_set_list = models.ExerciseSet.objects.filter(workout_exercise_id=workout_exercise_id)
        return render(request, self.template_name, {"exercise_set_list": exercise_set_list, "exercise": exercise})
