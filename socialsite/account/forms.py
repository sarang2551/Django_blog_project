from django import forms

# the form autheticates users against the database
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) # the widget is used to render the password input for HTML
