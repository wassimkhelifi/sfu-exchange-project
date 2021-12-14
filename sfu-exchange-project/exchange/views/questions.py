from django.db.models.aggregates import Count
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from ..models import Question, QuestionVotes, User
from ..helpers import vote_helper, notification_helper


# Creating the questions view
def QuestionsView(request):
    f = request.GET.get('filter','').strip("'")
    tag = request.GET.get('tag','').strip("'")
    query_params = request.GET.get('q', '').strip("'")
    # Hella jank but it was the fastest way of doing this 
        
    if query_params:
        # Search these fields
        search_vector = SearchVector('title', 'question_text', 'tags__name', 'user_id__username', 'user_id__email')
        
        # Make the search inclusive OR for each term in the query
        search_query = SearchQuery("")
        for param in query_params.split():
            search_query = search_query | SearchQuery(param)

        # Perform the search
        questions_list = Question.objects.annotate(
            search=search_vector, 
            rank=SearchRank(search_vector, search_query)
        )
        
        questions_list = questions_list.filter(search=search_query).order_by("-rank", "-created_at")
    else:
        questions_list = Question.objects

    if f == 'popular':
        questions_list = questions_list.order_by('-votes')
    elif f =='unanswered':
        questions_list = questions_list.annotate(count = Count('answer')).filter(
            Q(count=0)
        )
    else:
        questions_list = questions_list.order_by("-created_at")

    if tag:
        questions_list = questions_list.filter(tags__id = tag)


    paginator = Paginator(questions_list, 10)
    page = request.GET.get("page")
    paginated_questions = paginator.get_page(page)
    notification_list = notification_helper.get_notifications(request.user)
    query_text = query_params if query_params != None else ""

    return render(request, 'exchange/questions.html', {
        'questions_list': paginated_questions,
        'notifications': notification_list,
        'query_text': query_params,
    })

def QuestionUpvote(request, question_id, slug):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized, please login to vote', status=401)  
    args = processQuestionVoteAction(request, True, question_id, slug)

    return HttpResponseRedirect(reverse('Questions_Detail', kwargs=args))

def QuestionDownvote(request, question_id, slug):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized, please login to vote', status=401)  
    args = processQuestionVoteAction(request, False, question_id, slug)

    return HttpResponseRedirect(reverse('Questions_Detail', kwargs=args))

def processQuestionVoteAction(requestFromVote, isUpvoteClicked, question_id, slug):
    question = get_object_or_404(Question, id=requestFromVote.POST.get('question_id'))

    # If user has already voted
    if question.voted.filter(id=requestFromVote.user.id).exists():
        currentUserVote = QuestionVotes.objects.get(Q(question_id=question) & Q(user_id=requestFromVote.user))
        existingVoteIsUpvoteByUser = currentUserVote.is_upvote

        if existingVoteIsUpvoteByUser == True:
            vote_helper.processNewVoteActionOnUpvotedPost(question, isUpvoteClicked, currentUserVote, requestFromVote.user)
        else:
            vote_helper.processNewVoteActionOnDownvotedPost(question, isUpvoteClicked, currentUserVote, requestFromVote.user)
    else:
        if isUpvoteClicked:
            question.votes = question.votes + 1
            question.voted.add(requestFromVote.user)
            question.save()
            newVote = QuestionVotes(question_id=question, user_id=requestFromVote.user, is_upvote=True)
            newVote.save()
        else:
            question.votes = question.votes - 1
            question.voted.add(requestFromVote.user)
            question.save()
            newVote = QuestionVotes(question_id=question, user_id=requestFromVote.user, is_upvote=False)
            newVote.save()

    args = {}
    args['question_id'] = question_id
    args['slug'] = slug

    return args
