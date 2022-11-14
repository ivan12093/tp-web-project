from django.contrib import admin

from app.models import User, Tag, Question, Answer, ReactionsQuestion, ReactionsAnswers, Profile

# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(ReactionsQuestion)
admin.site.register(ReactionsAnswers)
