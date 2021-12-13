from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import F
from django.http.response import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.urls import reverse

from ..models import Question, QuestionVotes
from .questions_detail import QuestionsDetailView

# Creating the questions view
def QuestionsView(request):
    questions_list = Question.objects.all()
    return render(request, 'exchange/questions.html', {
        'questions_list': questions_list,
    })

def QuestionUpvote(request, question_id, slug):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized, please login to vote', status=401)  
    performVoteActions(request, True)
    slug = 'SKIP'
    return QuestionsDetailView(request, question_id, slug)

def QuestionDownvote(request, question_id, slug):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized, please login to vote', status=401)  
    performVoteActions(request, False)
    slug = 'SKIP'

    return QuestionsDetailView(request, question_id, slug)

def performVoteActions(requestFromVote, isUpvoteClicked):
    question = get_object_or_404(Question, id=requestFromVote.POST.get('question_id'))

    # If user has already voted
    if question.voted.filter(id=requestFromVote.user.id).exists():
        currentUserVote = QuestionVotes.objects.get(Q(question_id=question) & Q(user_id=requestFromVote.user))
        existingVoteIsUpvote = currentUserVote.is_upvote

        if existingVoteIsUpvote == True:
            if isUpvoteClicked:
                question.votes = question.votes - 1
                question.voted.remove(requestFromVote.user)
                question.save()
                question.refresh_from_db()
                currentUserVote.delete()
            else: 
                # Because we already have a existing upvote, we need to -1 to negate existing upvote and -1 for the downvotw
                question.votes = question.votes - 2
                question.save()
                currentUserVote.is_upvote = False
                currentUserVote.save()
        else:
            if isUpvoteClicked:
                question.votes = question.votes + 2
                question.save()
                currentUserVote.is_upvote = True
                currentUserVote.save()
            else:
                question.votes = question.votes + 1
                question.voted.remove(requestFromVote.user)
                question.save()
                question.refresh_from_db()
                currentUserVote.delete()
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

    return