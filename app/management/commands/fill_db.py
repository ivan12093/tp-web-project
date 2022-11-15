from random import choice, randint

from django.core.management import BaseCommand
from django.db import IntegrityError
from faker import Faker
from typing import List
from app.models import Question, Tag, Answer, User, Likeable

import app.models


class Command(BaseCommand):
    fake = Faker()

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        self.fill_db(ratio)

    def create_tags(self, amount):
        tags = [
            Tag(
                name=self.fake.word()
            )
            for i in range(amount)
        ]
        Tag.objects.bulk_create(tags)
        return tags

    def create_users(self, amount: int):
        users = []
        i = 0
        while i < amount:
            user = User(username=self.fake.simple_profile()['username'],
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

    def create_answers(self, amount: int, questions: List[Question]):
        answers = []
        for i in range(amount):
            question = choice(questions)
            answer = Answer(
                text=self.fake.text(max_nb_chars=randint(100, 300)),
                related_question=question,
                author=question.author,
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
        question_amount = ratio
        answer_amount = ratio * 100
        tag_amount = ratio
        reaction_amount = ratio * 200

        tags = self.create_tags(tag_amount)
        profiles = self.create_users(user_amount)
        questions = self.create_questions(question_amount, profiles,
                                          tags)
        answers = self.create_answers(answer_amount, questions)
        self.create_reactions(reaction_amount, answers + questions,
                              profiles)
