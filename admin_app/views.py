from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponseRedirect
from workout_app import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import CreateUserForm
from django.db import IntegrityError
from django.contrib import messages
from django.core.paginator import Paginator


class UserList(View):
    # List of users. Also, creating and filtering users.
    template_name = "users.html"
    create_user_form_class = CreateUserForm
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        # Select all users
        User = get_user_model()
        users = User.objects.all()
        # Add users to the paginatro
        paginator = Paginator(users, self.paginate_by)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # Create an empty form for creating users
        create_user_form = self.create_user_form_class()

        return render(request, self.template_name, {"page_obj": page_obj, "create_user_form": create_user_form})

    def post(self, request, *args, **kwargs):
        # Create user if a the according form has been submitted
        self.__create_user(request)
        # Copy the string that has been submitted in the search field
        # If it was empty the default value is an empty string, which will
        # yield all users
        seach_user = request.POST.get('search_user', "")
        # Instanciate an empty form to send back to the template
        create_user_form = self.create_user_form_class()
        # Select all users
        User = get_user_model()
        users = User.objects.all()
        # Create an empty list to hold filtered users
        user_list = []
        # Filter the users, according to the search_user value (The search-field on the page)
        for user in users:
            if seach_user in user.username:
                user_list.append(user)
        # Put the filtered results in the paginator
        paginator = Paginator(user_list, self.paginate_by)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj, "create_user_form": create_user_form})

    def __create_user(self, request):
        # Create a user if the create_user_form in home.html has been submitted
        create_user_form = self.create_user_form_class(request.POST)
        if create_user_form.is_valid():
            try:
                user_name = create_user_form.cleaned_data['username']
                password = create_user_form.cleaned_data['password1']
                User.objects.create_user(username=user_name,
                                         password=password)
            except IntegrityError:
                # This error will incur if the username already exists
                messages.add_message(
                    request, messages.ERROR, "The username already exists!")
        return


class WorkoutList(View):
    # List workouts by user.id
    template_name = "admin_workout_list.html"

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = User.objects.get(id=user_id)
        workout_list = models.Workout.objects.filter(
            user_id=user_id).order_by('id')
        return render(request, self.template_name, {"workout_list": workout_list, "user": user})


class WorkoutExerciseList(View):
    # List workout_exercises by workout.id
    template_name = "admin_workout_exercise_list.html"

    def get(self, request, *args, **kwargs):
        workout_id = kwargs.get("workout_id")
        user_id = kwargs.get("user_id")
        user = User.objects.get(id=user_id)

        workout_exercise_list = models.WorkoutExercise.objects.filter(
            workout_id=workout_id).order_by('id')
        return render(request, self.template_name, {"workout_exercise_list": workout_exercise_list, "user": user})


class ExerciseSetList(View):
    # List exercise_sets by workout_exercise.id
    template_name = "admin_exercise_set_list.html"

    def get(self, request, *args, **kwargs):
        workout_exercise_id = kwargs.get("workout_exercise_id")
        workout_exercise = models.WorkoutExercise.objects.get(
            id=workout_exercise_id)
        exercise = workout_exercise.exercise
        exercise_set_list = models.ExerciseSet.objects.filter(
            workout_exercise_id=workout_exercise_id)
        return render(request, self.template_name, {"exercise_set_list": exercise_set_list, "exercise": exercise})


class DeleteUser(View):
    # Delete user
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = User.objects.get(id=user_id)
        user.delete()
        return HttpResponseRedirect(reverse('admin-users'))
