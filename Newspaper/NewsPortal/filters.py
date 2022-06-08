from django_filters import *
from .models import *
from django.forms import *

class DateInput(DateInput):
    input_type = 'date'

class PostFilter(FilterSet):
    postCategory = ModelMultipleChoiceFilter(
        field_name='postCategory',
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
            'author__authorUser': ['exact'],
        }
