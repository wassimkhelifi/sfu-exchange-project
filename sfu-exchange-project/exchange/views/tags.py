from django.shortcuts import render
from django.http import HttpResponse

from ..models import Tag

# Creating the tags view
def TagsView(request):
    tags_list = Tag.objects.all()
    return render(request, 'exchange/tags.html', {
        'tags_list': tags_list,
    })