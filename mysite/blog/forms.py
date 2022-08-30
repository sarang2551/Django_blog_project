import email
from .models import Comment
from django import forms

class EmailPostForm(forms.Form):
    # form details
    name = forms.CharField(max_length=25) # html equivalent of <input type="text"></input>
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    # Django introscepts the model and builds the form dynamically (just add this stuff in the Meta class)
    class Meta:
        model = Comment
        fields = ('name','email','body')


