from django.forms import *
from django.core.exceptions import ValidationError
from .models import *
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm


class UserForm(ModelForm):
    authorUser = CharField(
        label='Name'
    )
    class Meta:
        model = Author
        fields = [
            'authorUser',
            'age'
        ]

class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class PostForm(ModelForm):
    text = CharField()
    postCategory = ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label='Categories',
        )
    
    class Meta:
        model = Post
        fields =  [
            'title',
            'text',
            'author',
            'postCategory'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title") 
        text = cleaned_data.get("text")
        return cleaned_data