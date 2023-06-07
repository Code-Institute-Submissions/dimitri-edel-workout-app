from django.forms import ModelForm
from .models import *

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ["name"]
