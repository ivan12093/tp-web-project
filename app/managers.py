from django.db.models import Manager, Count


class TagModelManager(Manager):
    def get_popular_tags(self):
        return self.values('name')\
            .annotate(count_questions=Count('question'))\
            .order_by('-count_questions')


class UserModelManager(Manager):
    def get_best_members(self):
        return self.values('username')\
            .annotate(count_answers=Count('answer'))\
            .order_by('-count_answers')


class QuestionModelManager(Manager):
    def get_newest_questions(self):
        return self.all().order_by('-datetime').reverse()

    def get_hottest_questions(self):
        return self\
            .annotate(activity=Count('answer') + Count('likes') + Count('dislikes'))\
            .order_by('-activity')

    def get_questions_by_tag(self, tag):
        return self.all().filter(tags__name=tag).order_by('-datetime').reverse()

    def get_question_by_id(self, question_id):
        return self.all().filter(id=question_id)


class AnswerModelManager(Manager):
    pass
