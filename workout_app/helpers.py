from django.http import HttpResponseRedirect
from django.shortcuts import reverse

# Redirect user to the main page of their group
def redirect_user_to_goup(request):
    user_group = None
    # Grab the name of the first group of the user
    # Users can belong to many groups, yet in this project
    # there is only one group: admin
    user_group = request.user.groups.all()[0].name
    if user_group == 'admin':
        return HttpResponseRedirect(reverse("admin-users"))
    else:
        return HttpResponseRedirect(reverse("home"))
