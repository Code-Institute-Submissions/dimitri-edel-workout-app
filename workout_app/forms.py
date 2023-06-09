from django.forms import ModelForm, TextInput, IntegerField, HiddenInput, modelformset_factory
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
    # id of the ExerciseSet as a hidden field
    id = IntegerField(widget = HiddenInput)   

    class Meta:
        model = ExerciseSet
        fields = ["id", "exercise", "reps","weight", "time","distance"]

    
    def __init__(self, *args, **kwargs):
        super(ExerciseSetForm, self).__init__(*args, **kwargs)
        # Set the empty label in the selector
        self.fields['exercise'].empty_label = "( --- Select Exercise --- )"

class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "type", "goal"]     



ExersiceSetForms = modelformset_factory(model=ExerciseSet, form=ExerciseSetForm, fields=["id", "exercise", "reps","weight", "time","distance"], extra=0)