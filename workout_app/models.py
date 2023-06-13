from django.db import models
from django.contrib.auth.models import User

# EXERCISE_TYPE is used in class Exercise
EXERCISE_TYPE = ((0, "Strength"), (1, "Cardio"))
# EXERCISE_GOAL is used in class Exercise
EXERCISE_GOAL = ((0, "Repetitions"), (2, "Distance"))

# A class for a Workout session
# A Wrokout is comprised of several sets.
# Each set is for one particular type of exercise
class Workout(models.Model):    
    # Relation to the user
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_workout")
    # Name of the session
    name = models.CharField(max_length=200, blank=False)
    # Date on which the workout took place
    date = models.DateTimeField(auto_now_add=True)
    # Meta for ordering the objects in a descending order
    class Meta:
        ordering = ['-date']
    # Strinbg representation of the object
    def __str__(self):
        return self.name

# A class for the type of exercise, such as push-ups, pull-ups, jogging, etc.
# The WorkoutSet class is related to this class. A WorkoutSet is for a particular
# type of exercise. For instance, the user wants to do a set of push-ups. 
class Exercise(models.Model): 
    # Relation to the user
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_exercise", default=1)   
    # Name of the exercise
    name = models.CharField(max_length=200, blank=False)
    # Type of exercise. There are only two types: Strength and Cardio which are
    # defined in a tupple at the top of this script file
    type = models.IntegerField(choices=EXERCISE_TYPE, default=0)
    # The goal field will only be used in conjunction with Exercises of type Cardio.
    # If the Exercise if of type Strength then this field will be left blank.
    # There are basicly two types of goal: distance and repetitions.
    goal = models.IntegerField(choices=EXERCISE_GOAL, default=0)
    # Strinbg representation of the object
    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    # The relationshop to the owner object of type Workout
    workout= models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="workout_workout_exercise")
    # The relationship to an Exercise object
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT, related_name="exercise_workout_exercise")
    # Status of wether or not you're done with the exercise within the given workout
    done = models.BooleanField(default=False)
    # String representation of the object
    def __str__(self):
        return f"{self.workout.name} : {self.exercise.name}"


# A class for a set. It belongs to (related to) an object of type Workout.
# Each set must also be related to a particular exercise, such as pull-ups or jogging, etc.
class ExerciseSet(models.Model):
    # The relationshop to the owner object of type Workout
    # workout= models.ForeignKey(
    #     Workout, on_delete=models.CASCADE, related_name="workout_exercise_set")
    # The relationship to an Exercise object
    # exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT, related_name="exercise_set")
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name="workout_exercise_exercise_set", default=0)
    # Number of repetitioons in this set
    reps = models.IntegerField(blank=True, null=True, default="0")
    # The weight that was used, if weight lifting is involved
    weight = models.IntegerField(blank=True, null=True, default="0")
    # The time it took to complete the set, if it is a cardio exercise
    time = models.CharField(blank=True, null=True, default="00:00:00:0")
    # The distance covered in the ammount of time specified in the time field
    distance = models.FloatField(blank=True, null=True, default="0")
    def __str__(self):
        return f"{self.workout_exercise.__str__()}"
