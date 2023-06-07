from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import *

# List of Workouts
class WorkoutList(generic.ListView):
    model = Workout
    queryset = Workout.objects.all()
    template_name = "index.html"
    paginate_by = 6
