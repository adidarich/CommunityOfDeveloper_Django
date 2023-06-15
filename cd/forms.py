from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={'rows': 3}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3}),
        }


class SearchForm(forms.Form):
    query = forms.CharField()
