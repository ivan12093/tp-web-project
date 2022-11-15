from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

from app.models import Question, Tag, User
from app.utils import paginate


def question_list(page, context=None):
    if context is None:
        context = {}
    popular_tags = Tag.objects.get_popular_tags()
    best_members = User.objects.get_best_members()
    context['page_obj'] = page
    context['popular_tags'] = popular_tags
    context['best_members'] = best_members
    return context


@require_GET
def index(request: HttpRequest) -> HttpResponse:
    questions = Question.objects.get_newest_questions()
    page = paginate(questions, request)
    return render(request, 'index.html',
                  context=question_list(page))


@require_GET
def hot(request: HttpRequest) -> HttpResponse:
    questions = Question.objects.get_hottest_questions()
    page = paginate(questions, request)
    return render(request, 'hot.html',
                  context=question_list(page))


@require_GET
def tag(request: HttpRequest, name: str) -> HttpResponse:
    questions = Question.objects.get_questions_by_tag(name)
    page = paginate(questions, request)
    context = {'tag': {'name': name}}
    return render(request, 'tag.html',
                  context=question_list(page, context=context))


@require_GET
def question(request: HttpRequest, question_id: int) -> HttpResponse:
    # Добавить 404, если такого вопроса нет
    question_item = Question.objects.get_question_by_id(question_id)[0]
    context = {'question': question_item}
    return render(request, 'question.html', context=context)


@require_GET
def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'login.html')


@require_GET
def signup(request: HttpRequest) -> HttpResponse:
    return render(request, 'signup.html')


@require_GET
def ask(request: HttpRequest) -> HttpResponse:
    return render(request, 'ask.html')


@require_GET
def settings(request: HttpRequest) -> HttpResponse:
    return render(request, 'settings.html')
