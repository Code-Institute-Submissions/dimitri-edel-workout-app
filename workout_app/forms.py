from django.forms import ModelForm
from .models import *

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ["name"]


class ExerciseSetForm(ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ["exercise","reps","weight", "time","distance"]
