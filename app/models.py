import django.contrib.auth.models

from django.db import models
import app.managers


class User(django.contrib.auth.models.User):
    avatar = models.ImageField(default='img/default_avatar.jpg')
    objects = app.managers.UserModelManager()

    def __str__(self):
        return self.username


class Likeable(models.Model):
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')

    def like(self, user: User):
        self.dislikes.remove(user)
        self.likes.add(user)

    def dislike(self, user: User):
        self.likes.remove(user)
        self.dislikes.add(user)

    @property
    def rating(self) -> int:
        return self.likes.count() - self.dislikes.count()


class Tag(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    objects = app.managers.TagModelManager()

    def __str__(self):
        return self.name


class Question(Likeable):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    datetime = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = app.managers.QuestionModelManager()

    def __str__(self):
        return self.title[:15]


class Answer(Likeable):
    text = models.TextField(1000)
    datetime = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    objects = app.managers.AnswerModelManager()

    def __str__(self):
        return self.title[:15]
