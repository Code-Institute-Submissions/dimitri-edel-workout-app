from django.forms import ModelForm, TextInput, formset_factory
from .models import *

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ["name"]

        labels = {
            'name' : ""
        }
        widgets = {
            'name': TextInput({'placeholder': 'Enter Name of Workout'})
        }


class ExerciseSetForm(ModelForm):    
    class Meta:
        model = ExerciseSet
        fields = ["exercise", "reps","weight", "time","distance"]

    
    def __init__(self, *args, **kwargs):
        super(ExerciseSetForm, self).__init__(*args, **kwargs)
        # Set the empty label in the selector
        self.fields['exercise'].empty_label = "( --- Select Exercise --- )"


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "type", "goal"]     

        