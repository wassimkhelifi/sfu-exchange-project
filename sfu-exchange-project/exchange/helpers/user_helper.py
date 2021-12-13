from ..models import Question, Answer, Comment, Tag




def format_user(user):
    user.name = user.first_name + ' ' + user.last_name

    questions = get_user_questions(user)
    answers   = get_user_answers(user)
    comments  = get_user_comments(user)

    user.questions = len(questions)
    user.answers   = len(answers)
    user.comments  = len(comments)

    user.points = sum(questions.values_list('votes', flat=True)) + \
                  sum(answers.values_list('votes', flat=True)) + \
                  sum(comments.values_list('votes', flat=True))
    return user

def get_user_questions(user) -> Question:
    return Question.objects.filter(user_id=user)

def get_user_answers(user) -> Answer:
    return Answer.objects.filter(user_id=user)

def get_user_comments(user) -> Comment:
    return Comment.objects.filter(user_id=user)

def get_user_top_questions(user) -> Question:
    top_questions = Question.objects.all().filter(user_id=user).order_by('-votes')
    if len(top_questions) > 5: top_questions = top_questions[:4]
    return top_questions

def get_user_top_tags(user) -> Tag:
    return get_user_top_questions(user).values_list('tags', flat=True)
