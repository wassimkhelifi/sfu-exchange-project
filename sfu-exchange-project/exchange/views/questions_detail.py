from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.http import Http404

from ..models import Question, Answer, User
from ..forms import AnswerForm
from ..helpers import notification_helper

def QuestionsDetailView(request, question_id, slug, notification_id=''):
    try:
        current_question = Question.objects.get(pk=question_id)
        answerForm = AnswerForm()

    except Question.DoesNotExist:
        raise Http404("Question does not exist!")
    
    if notification_id:
        notification_helper.delete_notification(notification_id)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        answerSubmission = AnswerForm(request.POST)
        if answerSubmission.is_valid():
            current_user = User.objects.get(username=request.user)
            Answer.objects.create(
                answer_text=answerSubmission.cleaned_data["answer_text"],
                anonymous=answerSubmission.cleaned_data["anonymous"],
                user_id=current_user,
                question_id=current_question,
            )
            notification_helper.create_notification(current_question.user_id, 
                {
                    "notification_title" : current_user.username + " answered your question!", 
                    "notification_text" : current_question.title + " has been answered.",
                    "url" : f"/exchange/questions/{current_question.id }/{ current_question.slug }",
                }
            )
            return HttpResponseRedirect(request.path_info)

          
    answers = Answer.objects.filter(question_id=question_id)
    if not answers:
        answers = None
    else:
        answers = anonymizeAnswers(answers)

    current_question = anonymizeQuestion(current_question)
    notification_list = notification_helper.get_notifications(request.user)
    context = {
        "question": current_question,
        "answers": answers,
        "answerForm": answerForm,
        "notifications": notification_list
    }

    return render(request, "exchange/questions_detail.html", context)


def anonymizeUser(user):
    user = User.objects.get(id=user.id)
    user.username = "anonymous"
    user.first_name = "anonymous"
    user.last_name = "anonymous"
    user.email = "anonymous@sfu.ca"

    return user


def anonymizeAnswers(answers):
    for answer in answers:
        if answer.anonymous == True:
            anon_user = anonymizeUser(answer.user_id)
            answer.user_id = anon_user

    return answers


def anonymizeQuestion(question):
    if question.anonymous == True:
        anon_user = anonymizeUser(question.user_id)
        question.user_id = anon_user

    return question
