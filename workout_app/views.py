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


class Workout(View):
    form_class = WorkoutForm

    template_name = "add_workout.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect("/")

        return render(request, self.template_name, {"form": form})