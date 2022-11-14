from random import choice, randint
from django.core.management import BaseCommand

import app.models


def fill_db(ratio):
    users = [
        app.models.User(username=f"username {i}", password=f"password {i}")
        for i in range(ratio)
    ]
    profiles = [
        app.models.Profile(user=users[i])
        for i in range(ratio)
    ]
    app.models.Profile.objects.bulk_create(profiles)

    tags = [
        app.models.Tag(
            name=f'Tag {i}'
        )
        for i in range(ratio)
    ]

    app.models.Tag.objects.bulk_create(tags)

    questions = [
        app.models.Question(
            title=f'Question {i}',
            text=f'Text {i}',
            author=choice(profiles),
            tags=list(set(choice(tags) for k in range(randint(1, 10)))),
            votes=randint(5, 50),
            comments=randint(5, 50)
        )
        for i in range(ratio * 10)
    ]

    app.models.Question.objects.bulk_create(questions)

    answers = [0] * ratio * 100
    for i in range(ratio * 100):
        question = choice(questions)
        answers[i] = app.models.Answer(
            text=f'Text {i}',
            is_correct=False,
            question=question,
            author=question.author,
        )

    app.models.Answer.objects.bulk_create(answers)

    reactions_question = [
        app.models.ReactionsQuestion(
            author=choice(profiles),
            positive=bool(randint(0, 3)),
            question=choice(questions)
        )
        for i in range(ratio * 50)
    ]

    app.models.ReactionsQuestion.objects.bulk_create(reactions_question)

    reactions_answer = [
        app.models.ReactionsAnswers(
            author=choice(profiles),
            positive=bool(randint(0, 3)),
            question=choice(answers)
        )
        for i in range(ratio * 150)
    ]

    app.models.ReactionsAnswers.objects.bulk_create(reactions_answer)


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('ratio', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio'][0]
        fill_db(ratio)
