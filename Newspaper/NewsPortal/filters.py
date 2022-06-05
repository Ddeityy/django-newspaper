from django_filters import ModelMultipleChoiceFilter, DateFilter, FilterSet
from .models import Category, Post
from django.forms import DateInput

class DateInput(DateInput):
    input_type = 'date'

class PostFilter(FilterSet):
    post_category = ModelMultipleChoiceFilter(
        field_name='post_category',
        queryset=Category.objects.all(),
        label='Categories',
        conjoined=True
    )
    
    creation_timedate = DateFilter(
        lookup_expr='gt',
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        ),
        label='Older than:'
    )
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__author_user': ['exact'],
        }
