import django.contrib.auth.models

from django.db import models
import app.managers


class User(django.contrib.auth.models.AbstractUser):
    avatar = models.ImageField(default='img/default_avatar.jpg', upload_to='img/%Y/%m/%d/')
    objects = app.managers.UserModelManager()

    def __str__(self):
        return self.username


class Likeable(models.Model):
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')
    rating = models.IntegerField(default=0)

    def has_liked_by(self, user):
        return self.likes.contains(user)

    def has_disliked_by(self, user: User):
        return self.dislikes.contains(user)

    def unlike(self, user: User, commit=True):
        if self.has_liked_by(user):
            self.rating -= 1
            self.save()
        self.likes.remove(user)

    def undislike(self, user: User, commit=True):
        if self.has_disliked_by(user):
            self.rating += 1
            self.save()
        self.dislikes.remove(user)

    def like(self, user: User):
        self.undislike(user)
        if not self.likes.contains(user):
            self.likes.add(user)
            self.rating += 1
            self.save()

    def dislike(self, user: User):
        self.unlike(user)
        if not self.dislikes.contains(user):
            self.dislikes.add(user)
            self.rating -= 1
            self.save()


class Tag(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    objects = app.managers.TagModelManager()

    def __str__(self):
        return self.name


class Question(Likeable):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    datetime = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = app.managers.QuestionModelManager()

    def __str__(self):
        return self.title[:15]


class Answer(Likeable):
    text = models.TextField(1000)
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    objects = app.managers.AnswerModelManager()

    def set_correctness(self, is_correct: bool):
        self.is_correct = is_correct
        self.save()

    def __str__(self):
        return self.title[:15]
