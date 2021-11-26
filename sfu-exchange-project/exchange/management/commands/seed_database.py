import os
from typing import Any, Optional
from django.core.management import BaseCommand
from exchange.models import *
from django.db import transaction
import random

ROLES = [
    ("Admin", "Full feature controls"),
    ("Moderator", "Moderating comments and answers"),
    ("Faculty", "Creating and moderating Faculty Posts"),
    ("Professor", "Creating and moderating class related Posts"),
    ("Student", "Can create and view Posts and Answers"),
]

FACULTIES = [
    "Applied Sciences",
    "Arts and Social Sciences",
    "Education",
    "Business",
    "Communication, Art and Technology",
    "Environment",
    "Health Sciences",
    "Science",
]

NUM_USERS = 50
NUM_QUESTIONS = 25
MAX_ANSWERS_PER_QUESTION = 5
COMMENTS_PER_ANSWER = 5
TAGS = 15


class Command(BaseCommand):
    help = "Generate Dummy data for the database"

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> Optional[str]:

        self.stdout.write(
            "Wiping old database... Note: Does not reset auto-increment IDs"
        )
        models = [Faculty, Role, User, Notification, Tag, Question, Answer, Comment]
        for model in models:
            if model == User:
                # Don't delete super users
                for user in model.objects.all():
                    if not user.is_superuser:
                        user.delete()
            else:
                model.objects.all().delete()

        self.stdout.write("Creating dummy data...")
        roles = [Role(name=role[0], description=role[1]) for role in ROLES]
        faculties = [Faculty(name=faculty) for faculty in FACULTIES]
        tags = [Tag(name=f"Tag-{tag}") for tag in range(TAGS)]

        # Commit objects to DB
        for r in roles:
            r.save()

        for f in faculties:
            f.save()

        for t in tags:
            t.save()

        f_names = open("./seed_data/names.txt").read().splitlines()
        l_names = open("./seed_data/last_names.txt").read().splitlines()

        self.stdout.write(
            "Creating random users... this may take a couple seconds... All have password: password"
        )
        users = []
        for user in range(NUM_USERS):
            #
            f_name = random.choice(f_names)
            l_name = random.choice(l_names)
            username = f"{f_name[0].lower()}{l_name.lower()}{random.randint(100,999)}"

            user = User.objects.create_user(
                username=username,
                email=f"{username}@sfu.ca",
                first_name=f_name,
                last_name=l_name,
                password="password",  # not unique but this way we can login to everyones account
                img="https://www.deviantart.com/moist-toad/art/Knackles-675515746",  # sorry for memeing
                faculty_id=random.choice(faculties),
            )
            user.save()
            user.roles.add(random.choice(roles))
            users.append(user)

        self.stdout.write("Creating Questions...")
        questions = []
        for _ in range(NUM_QUESTIONS):
            question = Question(
                title="Lorem Ipsum Question",
                question_text="Are sentiments apartments decisively the especially alteration. After nor you leave might share court balls.",
                votes=random.randint(30, 1000),
                anonymous=random.choice([True,False]),
                user_id=random.choice(users),
            )
            question.save()
            for i in range(random.randint(2, 5)):
                question.tags.add(
                    random.choice(tags)
                )  # This may cause overlaps but shouldn't be an issue
            questions.append(question)

        
        self.stdout.write("Creating Answers...")
        answers = []
        for _ in range(COMMENTS_PER_ANSWER):
            answer = Answer(
                answer_text = "Made last it seen went no just when of by. Occasional entreaties comparison me difficulty so themselves.",
                votes=random.randint(30, 1000),
                anonymous=random.choice([True,False]),
                user_id = random.choice(users),
                question_id = random.choice(questions)
            )
            answer.save()
            answers.append(answer)

        self.stdout.write("Creating Comments...")
        for _ in range(COMMENTS_PER_ANSWER):
            comment = Comment(
                comment_text = "His exquisite sincerity education shameless ten earnestly breakfast add.",
                votes=random.randint(10, 500),
                anonymous=random.choice([True,False]),
                user_id = random.choice(users), 
                answer_id = random.choice(answers)
            )
            comment.save() 

        self.stdout.write("Dummy data generation finished")