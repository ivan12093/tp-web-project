from django.contrib import admin

from app.models import Tag, Question, Answer, User

# Register your models here.

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
