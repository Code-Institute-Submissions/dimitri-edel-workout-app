from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import ProtectedError

# List of Workouts


class WorkoutList(generic.ListView):
    model = Workout      
    template_name = "index.html"
    paginate_by = 20

    # Only retrieve datasets related to the user
    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)

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
        workout_exercise_form = self.workout_exercise_form_class(
            prefix="workout_exercise")
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
    # Reference to the name of the form class for the model class Workout
    workout_form_class = WorkoutForm
    # Reference to the name of the form class for the model class WorkoutExercise
    workout_exercise_form_class = WorkoutExerciseForm

    # Referenece to the template for this view
    template_name = "edit_workout.html"
    # Process a GET-Request

    def get(self, request, id, *args, **kwargs):
        # Instanciate the forms.
        # The prefix is mandatory whhen using several forms in the same view.
        # When initializing a form, using the data in the POST-request object, prefix
        # helps setting the forms apart, as you can see in the post method below.
        workout = Workout.objects.get(id=id)
        # Create form for the workout object
        workout_form = self.workout_form_class(
            instance=workout, prefix="workout")
        # Get the last object from the WorkoutExercise model that is related to this workout
        workout_exercise_list = WorkoutExercise.objects.filter(workout_id=id)
        # Create a form for the last WrokoutExercise object
        workout_exercise_form = self.workout_exercise_form_class(
            instance=workout_exercise_list.last(), prefix="workout_exercise"
        )

        # Use the Form-Set to extract the set of forms from the POST-request
        workout_exercise_formset = WorkoutExerciseFormset(
            queryset=WorkoutExercise.objects.filter(workout_id=id))

        # Render the dedicated template
        return render(
            request, self.template_name, {"workout_form": workout_form,
                                          "workout_exercise_list": workout_exercise_list,
                                          "workout_exercise_form": workout_exercise_form})
    # Process a POST-Request
    # @parameter : id = workout_id

    def post(self, request, id, *args, **kwargs):

        workout = Workout.objects.get(id=id)
        # Instanciate the forms.
        workout_form = self.workout_form_class(
            request.POST, prefix="workout", instance=workout)
        #
        workout_exercise = WorkoutExercise.objects.filter(workout_id=id).last()

        workout_exercise_form = self.workout_exercise_form_class(
            request.POST, prefix="workout_exercise", instance=workout_exercise
        )
        # Use the Form-Set to extract the set of forms from the POST-request
        workout_exercise_formset = WorkoutExerciseFormset(
            request.POST, request.FILES)
        # If both forms are valid
        if workout_form.is_valid() and workout_exercise_form.is_valid():
            print("Is valid !!!!!!!!!!!!!!!!!!!!")
            return self.__save_forms(request, workout_form, workout_exercise_form)

        # If the form was not valid, render the template. The workout_from will contain the validation
        # messages for the user, which had been generated upon calling the is_valid() method
        return render(request, self.template_name, {"workout_form": workout_form})

    def __save_forms(self, request, workout_form, workout_exercise_form):
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
        return HttpResponseRedirect(reverse('edit_workout', kwargs={'id':workout_form.instance  .id}))


class EditExerciseSet(View):
    workout_exercise_form_class = WorkoutExerciseForm
    exercise_set_form_class = ExerciseSetForm
    template_strength_exercise = "edit_workout_exercise_strength.html"
    template_repetitions_exercise = "edit_workout_exercise_repetitions.html"
    template_distance_exercise = "edit_workout_exercise_distance.html"
    EXERCISE_TYPE_STRENGTH = 0
    EXERCISE_TYPE_CARDIO = 1
    EXERCISE_GOAL_REPETITIONS = 0
    EXERCISE_GOAL_DISTANCE = 1

    def get(self, request, workout_exercise_id, *args, **kwargs):
        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)
        workout_exercise_form = self.workout_exercise_form_class(
            instance=workout_exercise, prefix="workout_exercise")
        exercise_set_formset = ExersiceSetFormset(
            queryset=ExerciseSet.objects.filter(workout_exercise_id=workout_exercise_id))

        # Determine the type of exercise
        exercise = Exercise.objects.get(
            id=workout_exercise.exercise_id)

        return self.__render(request, exercise, workout_exercise_form, exercise_set_formset)

    def post(self, request, workout_exercise_id, *args, **kwargs):
        #
        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)

        #
        workout_exercise_form = self.workout_exercise_form_class(
            request.POST, instance=workout_exercise, prefix="workout_exercise")
        #
        exercise_set_formset = ExersiceSetFormset(request.POST, request.FILES)

        exercise = Exercise.objects.get(id=workout_exercise.exercise_id)

        # If forms are valid
        if workout_exercise_form.is_valid() and exercise_set_formset.is_valid():
            self.__save_forms(request, workout_exercise_form,
                              exercise_set_formset)

        return self.__render(request, exercise, workout_exercise_form, exercise_set_formset)

    def __save_forms(self, request, workout_exercise_form, exercise_set_formset):
        workout_exercise_form.instance.user = request.user
        workout_exercise_form.save()

        for form in exercise_set_formset:
            form.instance.exercise_workout_exercise = workout_exercise_form.instance.id
            form.save()
        # return HttpResponseRedirect(f"edit_exercise_set/{workout_exercise_form.instance.id}")
        return HttpResponseRedirect(reverse("edit_exercise_set", kwargs={"workout_exercise_id": workout_exercise_form.instance.id}))

    def __render(self, request, exercise, workout_exercise_form, exercise_set_formset):
        if exercise.type == self.EXERCISE_TYPE_STRENGTH:
            return render(request, self.template_strength_exercise, {"exercise": exercise, "workout_exercise_form": workout_exercise_form, "exercise_set_formset": exercise_set_formset})
        else:
            if exercise.goal == self.EXERCISE_GOAL_REPETITIONS:
                return render(request, self.template_repetitions_exercise, {"exercise": exercise, "workout_exercise_form": workout_exercise_form, "exercise_set_formset": exercise_set_formset})
            else:
                return render(request, self.template_distance_exercise, {"exercise": exercise, "workout_exercise_form": workout_exercise_form, "exercise_set_formset": exercise_set_formset})


class AddExerciseSet(View):
    # Process a GET-request
    def get(self, request, workout_exercise_id, workout_id,  *args, **kwargs):

        # Create new ExerciseSet object
        ExerciseSet.objects.create(workout_exercise_id=workout_exercise_id)

        # return HttpResponseRedirect(f"/edit_exercise_set/{workout_exercise_id}")
        return HttpResponseRedirect(reverse('edit_exercise_set', kwargs={"workout_exercise_id": workout_exercise_id}))


class DeleteExerciseSet(View):
    def get(self, request, workout_exercise_id, exercise_set_id, *args, **kwargs):
        exercise_set = ExerciseSet.objects.get(id=exercise_set_id)
        exercise_set.delete()
        return HttpResponseRedirect(reverse('edit_exercise_set', kwargs={"workout_exercise_id": workout_exercise_id}))


class AddWorkoutExercise(View):
    def get(self, request, workout_id, *args, **kwargs):
        WorkoutExercise.objects.create(workout_id=workout_id, exercise_id=1)
        # return HttpResponseRedirect(f"/edit_workout/{workout_id}")
        return HttpResponseRedirect(reverse('edit_workout', kwargs={"id": workout_id}))


class DeleteWorkoutExercise(View):
    def get(self, request, workout_exercise_id, workout_id, *args, **kwargs):
        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)
        workout_exercise.delete()
        return HttpResponseRedirect(reverse('edit_workout', kwargs={'id':workout_id}))


class DeleteWorkout(View):
    def get(self, request, workout_id, *args, **kwargs):
        workout = Workout.objects.get(id=workout_id)
        workout.delete()
        return HttpResponseRedirect(reverse('home'))


class EditExerciseList(View):
    # Reference to the form
    exercise_form_class = ExerciseForm
    # Reference to the template
    template_name = "edit_exercise_list.html"
    # Process a GET-Request

    def get(self, request, *args, **kwargs):
        # Instanciate the form
        exercises = Exercise.objects.all()
        edit_exercise = exercises.last()
        exercise_form = self.exercise_form_class(instance=edit_exercise)
        # Render the specified template
        return render(request, self.template_name, {"exercise_form": exercise_form, "exercises":exercises})
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
            return HttpResponseRedirect(reverse("edit_exercise_list"))
        # If the form was not valid, render the template. The workout_from will contain the validation
        # messages for the user, which had been generated upon calling the is_valid() method
        return render(request, self.template_name, {"exercise_form": exercise_form})


class DeleteExercise(View):
    def get(self, request, exercise_id, *args, **kwargs):
        exercise = Exercise.objects.get(id=exercise_id)
        try:
            exercise.delete()
        except ProtectedError:
            messages.add_message(request, messages.ERROR, "This exercise connot be deleted because it is being used in a workout!")
            
        return HttpResponseRedirect(reverse("edit_exercise_list"))


# List of Exercises
class ExerciseList(generic.ListView):
    model = Exercise
    queryset = Exercise.objects.all()
    template_name = "exercise_list.html"
    paginate_by = 6


# View for editing exercises
class EditExercise(View):
    # Reference to the form
    exercise_form_class = ExerciseForm
    # Reference to the template
    template_name = "edit_exercise.html"
    # Process a GET-Request

    def get(self, request, exercise_id, *args, **kwargs):
        # Retrieve dataset
        exercise = Exercise.objects.get(id=exercise_id)
        # Instanciate the form
        exercise_form = self.exercise_form_class(instance=exercise)
        # Render the specified template
        return render(request, self.template_name, {"exercise_form": exercise_form})
    # Process a POST-Request

    def post(self, request,  *args, **kwargs):
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
            return HttpResponseRedirect(reverse("edit_exercise_list"))
        # If the form was not valid, render the template. The workout_from will contain the validation
        # messages for the user, which had been generated upon calling the is_valid() method
        return render(request, self.template_name, {"exercise_form": exercise_form})
