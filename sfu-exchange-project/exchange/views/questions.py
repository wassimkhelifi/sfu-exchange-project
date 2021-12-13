from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.db.models import Q

from ..models import Question, QuestionVotes
from .questions_detail import QuestionsDetailView
from ..helpers import vote_helper

# Creating the questions view
def QuestionsView(request):
    questions_list = Question.objects.all()
    return render(request, 'exchange/questions.html', {
        'questions_list': questions_list,
    })

def QuestionUpvote(request, question_id, slug):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized, please login to vote', status=401)  
    processQuestionVoteAction(request, True)
    slug = 'FROM_QUESTION_VOTE_TO_RENDERING_Q_DETAIL_VIEW'
    return QuestionsDetailView(request, question_id, slug)

def QuestionDownvote(request, question_id, slug):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized, please login to vote', status=401)  
    processQuestionVoteAction(request, False)
    slug = 'FROM_QUESTION_VOTE_TO_RENDERING_Q_DETAIL_VIEW'

    return QuestionsDetailView(request, question_id, slug)

def processQuestionVoteAction(requestFromVote, isUpvoteClicked):
    question = get_object_or_404(Question, id=requestFromVote.POST.get('question_id'))

    # If user has already voted
    if question.voted.filter(id=requestFromVote.user.id).exists():
        currentUserVote = QuestionVotes.objects.get(Q(question_id=question) & Q(user_id=requestFromVote.user))
        existingVoteIsUpvoteByUser = currentUserVote.is_upvote

        if existingVoteIsUpvoteByUser == True:
            vote_helper.processNewVoteActionOnUpvotedPost(question, isUpvoteClicked, currentUserVote, requestFromVote.user)
        else:
            vote_helper.processNewVoteActionOnDownvotedPost(question, isUpvoteClicked, currentUserVote, requestFromVote.user)
    # otherwise user has not voted yet:
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