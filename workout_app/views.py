from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.models import User

# List of Workouts
class WorkoutList(generic.ListView):
    model = Workout
    queryset = Workout.objects.all()
    template_name = "index.html"
    paginate_by = 6


class AddWorkout(View):
    workout_form_class = WorkoutForm
    exercise_set_form_class = ExerciseSetForm
    template_name = "add_workout.html"

    def get(self, request, *args, **kwargs):
        workout_form = self.workout_form_class(prefix="workout")
        exercise_set_form = self.exercise_set_form_class(prefix="exercise_set")
        return render(request, self.template_name, {"workout_form": workout_form, "exercise_set_form": exercise_set_form})

    def post(self, request, *args, **kwargs):
        workout_form = self.workout_form_class(request.POST, prefix="workout")
        exercise_set_form = self.exercise_set_form_class(request.POST, prefix="exercise_set")
        if workout_form.is_valid() and exercise_set_form.is_valid():
            # <process form cleaned data>
            workout_form.instance.user = request.user
            workout_form.save()
            exercise_set_form.instance.workout_id = workout_form.instance.id   
            exercise_set_form.save()         
            return HttpResponseRedirect("/")

        return render(request, self.template_name, {"workout_form": workout_form})