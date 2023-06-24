from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from workout_app import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Create your views here.
class UserList(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()

        return render(request, self.template_name, {"users": users})