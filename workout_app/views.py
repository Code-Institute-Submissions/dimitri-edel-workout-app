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
    paginate_by = 20

# View for adding a new Workout


class AddWorkout(View):
    # Reference to the form class for the model class Workout
    workout_form_class = WorkoutForm
    # Referenece to the form class for the model class ExerciseSet
    workout_exercise_form_class = WorkoutExerciseForm
    # Referenece to the template for this view
    template_name = "add_workout.html"
    # Process a GET-Request

    def get(self, request, *args, **kwargs):
        # Instanciate the forms.
        # The prefix is mandatory whhen using several forms in the same view.
        # When initializing a form, using the data in the POST-request object, prefix
        # helps setting the forms apart, as you can see in the post method below.
        workout_form = self.workout_form_class(prefix="workout")
        workout_exercise_form = self.workout_exercise_form_class(prefix="workout_exercise")
        # Render the dedicated template
        return render(request, self.template_name, {"workout_form": workout_form, "workout_exercise_form": workout_exercise_form})
    # Process a POST-Request

    def post(self, request, *args, **kwargs):
        # Instanciate the forms.
        workout_form = self.workout_form_class(request.POST, prefix="workout")
        workout_exercise_form = self.workout_exercise_form_class(
            request.POST, prefix="workout_exercise")
        
        # If both forms are valid
        if workout_form.is_valid() and workout_exercise_form.is_valid():
            print("is valid !!!!!!!!!!!!!!!!!!!!")
            # Assign the form to the current user.
            # The instance property of the forms is a reference to the model class
            # that is being used and allows us to access its properties and methods
            workout_form.instance.user = request.user
            # Cimmit the model object to the database
            workout_form.save()
            # Assign the workout_id of the newly created Workout to the ExerciseSet.workout_id field
            workout_exercise_form.instance.workout_id = workout_form.instance.id
            # Commit the model object to the database
            workout_exercise_form.save()
            # Redirect the user to the home page
            return HttpResponseRedirect(f"edit_workout/{workout_form.instance.id}")
            # return HttpResponseRedirect(f"edit_workout/{workout_form.instance.id}")
        # If the form was not valid, render the template. The workout_from will contain the validation
        # messages for the user, which had been generated upon calling the is_valid() method
        return render(request, self.template_name, {"workout_form": workout_form})

# class for editing the list of exercises that the workout is comprised of
class EditWorkout(View):
    # Reference to the form class for the model class Workout
    workout_form_class = WorkoutForm
    
    # Referenece to the template for this view
    template_name = "edit_workout.html"
    # Process a GET-Request

    def get(self, request, id, *args, **kwargs):
        # Instanciate the forms.
        # The prefix is mandatory whhen using several forms in the same view.
        # When initializing a form, using the data in the POST-request object, prefix
        # helps setting the forms apart, as you can see in the post method below.
        workout = Workout.objects.get(id=id)
        workout_form = self.workout_form_class(
            instance=workout, prefix="workout")

        # Use the Form-Set to extract the set of forms from the POST-request
        workout_exercise_formset = WorkoutExerciseFormset(queryset=WorkoutExercise.objects.filter(workout_id=id))
        print(workout_exercise_formset.data)
        # workout_exercise_formset = []
        # exercise_sets = ExerciseSet.objects.filter(workout_id=id)
        # for exercise_set in exercise_sets:
        #     exercise_set_form = self.exercise_set_form_class(
        #         instance=exercise_set, prefix="exercise_set")
        #     workout_exercise_formset.append(exercise_set_form)

        # Render the dedicated template
        return render(request, self.template_name, {"workout_form": workout_form, "workout_exercise_formset": workout_exercise_formset})
    # Process a POST-Request
    # @parameter : id = workout_id
    def post(self, request, id, *args, **kwargs):
       
        workout = Workout.objects.get(id=id)
        # Instanciate the forms.
        workout_form = self.workout_form_class(
            request.POST, prefix="workout", instance=workout)
        # Create a Form-Set that can hold several forms at a time

        # Use the Form-Set to extract the set of forms from the POST-request
        workout_exercise_formset = WorkoutExerciseFormset(
            request.POST, request.FILES )

        # exercise_set_form = self.exercise_set_form_class(request.POST, prefix="exercise_set")

        # If both forms are valid
        if workout_form.is_valid() and workout_exercise_formset.is_valid():
            print("Is valid !!!!!!!!!!!!!!!!!!!!")
            return self.__save_forms(request, workout_form, workout_exercise_formset)

        # If the form was not valid, render the template. The workout_from will contain the validation
        # messages for the user, which had been generated upon calling the is_valid() method
        return render(request, self.template_name, {"workout_form": workout_form})

    def __save_forms(self, request, workout_form, workout_exercise_formset):
        # Assign the form to the current user.
        # The instance property of the forms is a reference to the model class
        # that is being used and allows us to access its properties and methods
        workout_form.instance.user = request.user
        # Cimmit the model object to the database
        workout_form.save()
        # Assign the workout_id of the newly created Workout to the ExerciseSet.workout_id field
        for exercise_set_form in workout_exercise_formset:
            exercise_set_form.instance.workout_id = workout_form.instance.id
            # Commit the model object to the database
            exercise_set_form.save()
        # Redirect the user to the home page
        return HttpResponseRedirect("/")


class AddExerciseSet(View):
    # Process a GET-request
    def get(self, request, workout_id, *args, **kwargs):
        exercise = Exercise.objects.get(id=1)
        ExerciseSet.objects.create(workout_id=workout_id, exercise=exercise)
        return HttpResponseRedirect(f"/edit_workout/{workout_id}")

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
