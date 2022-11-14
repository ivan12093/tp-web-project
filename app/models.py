import django.contrib.auth.models
from django.db import models
from django.db.models import Sum, F


class TagModelManager(models.Manager):
    def get_popular_tags(self):
        pass


class ProfileModelManager(models.Manager):
    def get_best_members(self):
        pass


class QuestionModelManager(models.Manager):
    def get_newest_questions(self):
        return self.all().order_by('id').reverse()

    def get_hottest_questions(self):
        return self.all().annotate(fieldsum=F('votes') + F('comments')).order_by('fieldsum').reverse()

    def get_questions_by_tag(self, tag):
        return self.all().filter(tags__name=tag).order_by('id').reverse()

    def get_question_by_id(self, question_id):
        return self.all().filter(id=question_id)


class UserModelManager(django.contrib.auth.models.UserManager):
    pass


class User(django.contrib.auth.models.User):
    objects = UserModelManager()


class Profile:
    avatar = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = ProfileModelManager()

    def __str__(self):
        return self.user.name


class Tag(models.Model):
    name = models.CharField(max_length=30)

    objects = TagModelManager()

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=100)
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, null=True)
    votes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    objects = QuestionModelManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField(max_length=1000)
    is_correct = models.BooleanField(default=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.text


class ReactionsQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    positive = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.id


class ReactionsAnswers(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    positive = models.BooleanField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.id
