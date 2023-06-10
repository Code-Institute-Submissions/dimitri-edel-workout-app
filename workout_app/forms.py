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
        fields = ["id", "reps","weight", "time","distance"]

    
    # def __init__(self, *args, **kwargs):
    #     super(ExerciseSetForm, self).__init__(*args, **kwargs)
    #     # Set the empty label in the selector
    #     self.fields['exercise'].empty_label = "( --- Select Exercise --- )"


# FormSet to hold multiple forms of type ExerciseSetForm
ExersiceSetFormset = modelformset_factory(model=ExerciseSet, form=ExerciseSetForm, fields=["id", "reps","weight", "time","distance"], extra=0)


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "type", "goal"]     



class WorkoutExerciseForm(ModelForm):
    # id of the WorkoutExercise as a hidden field
    # id = IntegerField(widget = HiddenInput) 

    class Meta:
        model= WorkoutExercise
        fields = ["exercise", "done"]

# FormSet to hold multiple forms of type WorkoutExerciseForm
WorkoutExerciseFormset = modelformset_factory(model=WorkoutExercise, form=WorkoutExerciseForm, fields = ["exercise", "done"], extra=0)