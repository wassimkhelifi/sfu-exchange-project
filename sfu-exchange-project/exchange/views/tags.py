from django.core.paginator import Paginator 
from django.db.models import Q
from django.shortcuts import render

from ..models import Tag

# Creating the tags view
def TagsView(request):
    if request.method == "GET":
        query_params = request.GET.get("q")

        if query_params:
            tags = Tag.objects.filter(
                Q(name__icontains=query_params)
            )

        else:
            tags = Tag.objects.all()

        paginator = Paginator(tags, 12)

        page = request.GET.get('page')
        paginated_tags = paginator.get_page(page)

        return render(request, 'exchange/tags.html', {
            'tags_list': paginated_tags,
        })
