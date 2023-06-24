from django import forms


class CreateUserForm(forms.Form):
    # Form to create a User
    username = forms.CharField(label="Username:", max_length=100)
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput)
