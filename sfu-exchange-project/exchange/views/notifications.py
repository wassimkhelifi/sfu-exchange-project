from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator

from ..helpers import notification_helper
from ..models import Notification

def NotificationsView(request, page=""):
    query_param = request.GET.get("q")
    query_param = "" if not query_param else query_param

    search_vector = SearchVector('notification_title', 'notification_text', 'created_at')
    search_query = SearchQuery(query_param)

    notifications = notification_helper.get_notifications(request.user).annotate(
        search=search_vector, 
        rank=SearchRank(search_vector, search_query),
    )

    if query_param:
        notifications = notifications.filter(search=query_param).order_by("-rank")

    paginator = Paginator(notifications, 10)

    page = request.GET.get("page")
    notification_list = paginator.get_page(page)

    return render(request, 'exchange/notifications.html', {
        "notifications": notification_list,
    })