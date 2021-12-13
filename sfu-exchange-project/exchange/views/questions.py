from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

from ..models import Question, QuestionVotes
from .questions_detail import QuestionsDetailView
from ..helpers import vote_helper, notification_helper

# Creating the questions view
def QuestionsView(request):
    questions_list = Question.objects.all()
    # TODO: can this be removed?
    notification_list = notification_helper.get_notifications(request.user)
    return render(request, 'exchange/questions.html', {
        'questions_list': questions_list,
        'notifications': notification_list,
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
