from django.shortcuts import render
from django.core.paginator import Paginator 

from ..models import Tag

# Creating the tags view
def TagsView(request):
    tags = Tag.objects.all()

    paginator = Paginator(tags, 12)

    page = request.GET.get('page')
    paginated_tags = paginator.get_page(page)

    return render(request, 'exchange/tags.html', {
        'tags_list': paginated_tags,
    })
