import email
from django import forms

class EmailPostForm(forms.Form):
    # form details
    name = forms.CharField(max_length=25) # html equivalent of <input type="text"></input>
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

