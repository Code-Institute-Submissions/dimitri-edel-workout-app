from django.forms import ModelForm, TextInput, ModelChoiceField
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
    exercise = ModelChoiceField(queryset=Exercise.objects.values_list('name', flat=True), empty_label="------ Select Exercise",to_field_name='exercise')
    
    class Meta:
        model = ExerciseSet
        fields = ["exercise", "reps","weight", "time","distance"]


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "type", "goal"]     

        