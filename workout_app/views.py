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

# View for adding a new Workout 
class AddWorkout(View):
    # Reference to the form class for the model class Workout
    workout_form_class = WorkoutForm
    # Referenece to the form class for the model class ExerciseSet
    exercise_set_form_class = ExerciseSetForm
    # Referenece to the template for this view
    template_name = "add_workout.html"
    # Process a GET-Request
    def get(self, request, *args, **kwargs):
        # Instanciate the forms. 
        # The prefix is mandatory whhen using several forms in the same view.
        # When initializing a form, using the data in the POST-request object, prefix
        # helps setting the forms apart, as you can see in the post method below.
        workout_form = self.workout_form_class(prefix="workout")
        exercise_set_form = self.exercise_set_form_class(prefix="exercise_set")
        # Render the dedicated template
        return render(request, self.template_name, {"workout_form": workout_form, "exercise_set_form": exercise_set_form})
    # Process a POST-Request
    def post(self, request, *args, **kwargs):
        # Instanciate the forms.
        workout_form = self.workout_form_class(request.POST, prefix="workout")
        exercise_set_form = self.exercise_set_form_class(request.POST, prefix="exercise_set")        
        # If both forms are valid
        if workout_form.is_valid() and exercise_set_form.is_valid():
            # Assign the form to the current user. 
            # The instance property of the forms is a reference to the model class 
            # that is being used and allows us to access its properties and methods
            workout_form.instance.user = request.user
            # Cimmit the model object to the database
            workout_form.save()
            # Assign the workout_id of the newly created Workout to the ExerciseSet.workout_id field
            exercise_set_form.instance.workout_id = workout_form.instance.id   
            # Commit the model object to the database
            exercise_set_form.save()  
            # Redirect the user to the home page       
            return HttpResponseRedirect(f"edit_workout/{workout_form.instance.id}")
            #return HttpResponseRedirect(f"edit_workout/{workout_form.instance.id}")
        # If the form was not valid, render the template. The workout_from will contain the validation 
        # messages for the user, which had been generated upon calling the is_valid() method
        return render(request, self.template_name, {"workout_form": workout_form})


class EditWorkout(View):
    # Reference to the form class for the model class Workout
    workout_form_class = WorkoutForm
    # Referenece to the form class for the model class ExerciseSet
    exercise_set_form_class = ExerciseSetForm
    # Referenece to the template for this view
    template_name = "edit_workout.html"
    # Process a GET-Request
    def get(self, request, id, *args, **kwargs):
        # Instanciate the forms. 
        # The prefix is mandatory whhen using several forms in the same view.
        # When initializing a form, using the data in the POST-request object, prefix
        # helps setting the forms apart, as you can see in the post method below.
        workout = Workout.objects.get(id=id)        
        workout_form = self.workout_form_class(instance=workout, prefix="workout")

        exercise_set_forms = []
        exercise_sets = ExerciseSet.objects.filter(workout_id=id)
        for exercise_set in exercise_sets:
            exercise_set_form = self.exercise_set_form_class(instance=exercise_set, prefix="exercise_set")
            exercise_set_forms.append(exercise_set_form)
        
        # Render the dedicated template
        return render(request, self.template_name, {"workout_form": workout_form, "exercise_set_forms": exercise_set_forms})
    # Process a POST-Request
    def post(self, request, *args, **kwargs):
        # Instanciate the forms.
        workout_form = self.workout_form_class(request.POST, prefix="workout")
        # Create a Form-Set that can hold several forms at a time
        ExersiceSetForms = formset_factory(ExerciseForm)
        # Use the Form-Set to extract the set of forms from the POST-request
        exercise_set_forms = ExersiceSetForms(request.POST)
        
        # exercise_set_form = self.exercise_set_form_class(request.POST, prefix="exercise_set")

        # If both forms are valid
        if workout_form.is_valid() and exercise_set_forms.is_valid():
            print("FORMS VALID")
            # Assign the form to the current user. 
            # The instance property of the forms is a reference to the model class 
            # that is being used and allows us to access its properties and methods
            workout_form.instance.user = request.user
            # Cimmit the model object to the database
            workout_form.save()
            # Assign the workout_id of the newly created Workout to the ExerciseSet.workout_id field
            for exercise_set_form in exercise_set_forms:
                exercise_set_form.instance.workout_id = workout_form.instance.id   
                # Commit the model object to the database
                exercise_set_form.save()  
            # Redirect the user to the home page       
            return HttpResponseRedirect("/")
        # If the form was not valid, render the template. The workout_from will contain the validation 
        # messages for the user, which had been generated upon calling the is_valid() method
        return render(request, self.template_name, {"workout_form": workout_form})

    

# List of Exercises
class ExerciseList(generic.ListView):
    model = Exercise
    queryset = Exercise.objects.all()
    template_name = "exercise_list.html"
    paginate_by = 6


# View for adding new exercises
class AddExercise(View):
    # Reference to the form
    exercise_form_class = ExerciseForm
    # Reference to the template
    template_name = "add_exercise.html"
    # Process a GET-Request
    def get(self, request, *args, **kwargs):
        # Instanciate the form
        exercise_form = self.exercise_form_class()
        # Render the specified template
        return render(request, self.template_name, {"exercise_form": exercise_form})
    # Process a POST-Request
    def post(self, request, *args, **kwargs):
        # Instanciate the form
        exercise_form = self.exercise_form_class(request.POST)
        # If the form is valid
        if exercise_form.is_valid():
            # Assign the form to the current user. 
            # The instance property of the forms is a reference to the model class 
            # that is being used and allows us to access its properties and methods
            exercise_form.instance.user = request.user
            # Commit the model object to the database
            exercise_form.save()                   
            # Redirect the user to the home page       
            return HttpResponseRedirect("exercise_list")
        # If the form was not valid, render the template. The workout_from will contain the validation 
        # messages for the user, which had been generated upon calling the is_valid() method
        return render(request, self.template_name, {"exercise_form": exercise_form})
