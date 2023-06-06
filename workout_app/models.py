from django.db import models
from django.contrib.auth.models import User

# Create your models here.
EXERCISE_TYPE = ((0, "Strength"), (1, "Cardio"))


class Workout(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_workout")
    name = models.CharField(max_length=200, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=200, blank=False)
    type = models.IntegerField(choices=EXERCISE_TYPE, default=0)
    goal = models.CharField(max_length=8, blank=False)

    def __str__(self):
        return self.name


class ExerciseSet(models.Model):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="workout_set")
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT, related_name="exercise_set")
    reps = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    time = models.IntegerField(null=True)
    distance = models.FloatField(null=True)
