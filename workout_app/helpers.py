from django.http import HttpResponseRedirect
from django.shortcuts import reverse

# Redirect user to the index page of their group
def redirect_user_to_goup(request):
    user_group = None
    user_group = request.user.groups.all()[0].name
    if user_group == 'admin':
        return HttpResponseRedirect(reverse("admin:index"))
    else:
        return HttpResponseRedirect(reverse("home"))
