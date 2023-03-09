from random import choice, randint

from django.core.management import BaseCommand
from django.db import IntegrityError
from faker import Faker
from typing import List
from app.models import Question, Tag, Answer, User, Likeable


class Command(BaseCommand):
    fake = Faker()

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        self.fill_db(ratio)

    def create_tags(self, amount):
        tags = set()
        while len(tags) < amount:
            tag = Tag(name=self.fake.word())
            if tag not in tags:
                tags.add(tag)
        tags = list(tags)
        Tag.objects.bulk_create(tags)
        return tags

    def create_users(self, amount: int):
        users = []
        i = 0
        while i < amount:
            _profile = self.fake.simple_profile()
            user = User.objects.create_user(username=_profile['username'],
                                            email=_profile['mail'],
                                            password=self.fake.password()
                                            )
            try:
                user.save()
                users.append(user)
                i += 1
            except IntegrityError:
                pass

        return users

    def create_questions(self, amount: int, users: List[Question],
                         tags: List[Tag], max_tags_per_question: int = 10):
        questions = []
        for i in range(amount):
            question = Question(
                title=self.fake.sentence(),
                text=self.fake.text(max_nb_chars=999),
                datetime=self.fake.date_time_this_decade(),
                author=choice(users),
            )
            question.save()
            for _ in range(randint(0, max_tags_per_question)):
                question.tags.add(choice(tags))
            questions.append(question)
        return questions

    def create_answers(self, amount: int, questions: List[Question],
                       users: List[User]):
        answers = []
        for i in range(amount):
            question = choice(questions)
            answer = Answer(
                text=self.fake.text(max_nb_chars=randint(100, 300)),
                related_question=question,
                author=choice(users),
                is_correct=not bool(randint(0, 10))
            )
            answer.save()
            answers.append(answer)
        return answers

    def create_reactions(self, count: int, likeables: List[Likeable],
                         users: List[User]):
        for i in range(count):
            likeable = choice(likeables)
            if randint(0, 10) > 3:
                likeable.like(choice(users))
            else:
                likeable.dislike(choice(users))

    def fill_db(self, ratio):
        user_amount = ratio
        question_amount = ratio * 10
        answer_amount = ratio * 100
        tag_amount = ratio
        reaction_amount = ratio * 200

        tags = self.create_tags(tag_amount)
        users = self.create_users(user_amount)
        questions = self.create_questions(question_amount, users,
                                          tags)
        answers = self.create_answers(answer_amount, questions, users)
        self.create_reactions(reaction_amount, answers + questions,
                              users)
