from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.template.defaultfilters import register

from ..models import AnswerVotes, Question, Answer, User, QuestionVotes
from ..forms import AnswerForm

# Custom template filter for lookup, thank you: https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
@register.filter(name='dict_key')
def get_item(dictionary, key):
    return dictionary.get(key)

def QuestionsDetailView(request, question_id, slug):
    try:
        current_question = Question.objects.get(pk=question_id)
        answerForm = AnswerForm()
    except Question.DoesNotExist:
        raise Http404('Question does not exist!')
    
    if slug == 'FROM_QUESTION_VOTE_TO_RENDERING_Q_DETAIL_VIEW':
        print('we need this skip from QuestionsUpvote and QuestionsDownvote fn')
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized, please login to vote', status=401)
        answerSubmission = AnswerForm(request.POST)
        if answerSubmission.is_valid():
            current_user = User.objects.get(username=request.user)
            Answer.objects.create(
                answer_text = answerSubmission.cleaned_data['answer_text'],
                anonymous = answerSubmission.cleaned_data['anonymous'],
                user_id = current_user,
                question_id = current_question
            )

    answers = Answer.objects.filter(question_id=question_id)
    if not answers:
        answers = None
    else:
        answers = anonymizeAnswers(answers)
        mappedVotedAnswers = mapVotedAnswers(answers, request.user.id)

    isQuestionedUpvoted = QuestionVotes.objects.filter(question_id=question_id).filter(user_id=request.user.id)
    if not isQuestionedUpvoted:
        questionVoteState = None
    else:
        questionVoteState = isQuestionUpvoted(question_id, request.user.id)

    current_question = anonymizeQuestion(current_question)
    return render(request, 'exchange/questions_detail.html', {
        'question': current_question,
        'answers': answers,
        'answerForm': answerForm,
        'questionVoteState': questionVoteState,
        'mappedVotedAnswers': mappedVotedAnswers,
    })

# Not sure if this works since can't test as adding comments is disabled with Wassim's changes
# Basically trying to create a new property called is_upvote in the answer and sending it back to the HTML
# so we can check to see if it is upvoted or downvoted and highlight the button accordingly
def mapVotedAnswers(answers, user_id):
    votedAnswersInQuestionByCurrentUser = {}
    for answer in answers:
        votedAnswerInQueryObject = AnswerVotes.objects.filter(answer_id=answer).filter(user_id=user_id)
        for answerVotesObj in votedAnswerInQueryObject:
            votedAnswersInQuestionByCurrentUser[answerVotesObj.answer_id] = answerVotesObj.is_upvote

    return votedAnswersInQuestionByCurrentUser

def isQuestionUpvoted(question_id, user_id):
    voted = QuestionVotes.objects.get(question_id=question_id, user_id=user_id)
    if voted.is_upvote:
        return 'UPVOTED'

    return 'DOWNVOTED'

def AnswerUpvote(request, answer_id):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized, please login to vote', status=401)  
    args = processAnswerVoteAction(request, True)

    return HttpResponseRedirect(reverse('Questions_Detail', kwargs=args))

def AnswerDownvote(request, answer_id):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized, please login to vote', status=401)
    args = processAnswerVoteAction(request, False)

    return HttpResponseRedirect(reverse('Questions_Detail', kwargs=args))

def processAnswerVoteAction(requestFromVote, isUpvoteClicked):
    answer = get_object_or_404(Answer, id=requestFromVote.POST.get('answer_id'))
    # If user has already voted
    if answer.voted.filter(id=requestFromVote.user.id).exists():
        currentUserVote = AnswerVotes.objects.get(Q(answer_id=answer) & Q(user_id=requestFromVote.user))
        existingVoteIsUpvote = currentUserVote.is_upvote

        if existingVoteIsUpvote == True:
            if isUpvoteClicked:
                answer.votes = answer.votes - 1
                answer.voted.remove(requestFromVote.user)
                answer.save()
                answer.refresh_from_db()
                currentUserVote.delete()
            else: 
                # Because we already have a existing upvote, we need to -1 to negate existing upvote and -1 for the downvotw
                answer.votes = answer.votes - 2
                answer.save()
                currentUserVote.is_upvote = False
                currentUserVote.save()
        else:
            if isUpvoteClicked:
                answer.votes = answer.votes + 2
                answer.save()
                currentUserVote.is_upvote = True
                currentUserVote.save()
            else:
                answer.votes = answer.votes + 1
                answer.voted.remove(requestFromVote.user)
                answer.save()
                answer.refresh_from_db()
                currentUserVote.delete()
    else:
        if isUpvoteClicked:
            answer.votes = answer.votes + 1
            answer.voted.add(requestFromVote.user)
            answer.save()
            newVote = AnswerVotes(answer_id=answer, user_id=requestFromVote.user, is_upvote=True)
            newVote.save()
        else:
            answer.votes = answer.votes - 1
            answer.voted.add(requestFromVote.user)
            answer.save()
            newVote = AnswerVotes(answer_id=answer, user_id=requestFromVote.user, is_upvote=False)
            newVote.save()
    
    args = {}
    args['question_id'] = answer.question_id.id
    args['slug'] = answer.question_id.slug

    return args

def anonymizeUser(user):
    user = User.objects.get(id=user.id)
    user.username = 'anonymous'
    user.first_name = 'anonymous'
    user.last_name = 'anonymous'
    user.email = 'anonymous@sfu.ca'

    return user

def anonymizeAnswers(answers):
    for answer in answers:
        if (answer.anonymous == True):
            anon_user = anonymizeUser(answer.user_id)
            answer.user_id = anon_user

    return answers

def anonymizeQuestion(question):
    if (question.anonymous == True):
        anon_user = anonymizeUser(question.user_id)
        question.user_id = anon_user

    return question
