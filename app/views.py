from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET

from app.models import Question, Tag, User
from app.utils import paginate


def add_sidebar_info(context=None):
    if context is None:
        context = {}
    popular_tags = Tag.objects.get_popular_tags()
    best_members = User.objects.get_best_members()
    context['popular_tags'] = popular_tags[:50]
    context['best_members'] = best_members[:14]
    return context


@require_GET
def index(request: HttpRequest) -> HttpResponse:
    questions = Question.objects.get_newest_questions()
    page = paginate(questions, request)
    context = {'page_obj': page}
    return render(request, 'index.html',
                  context=add_sidebar_info(context))


@require_GET
def hot(request: HttpRequest) -> HttpResponse:
    questions = Question.objects.get_hottest_questions()
    page = paginate(questions, request)
    context = {'page_obj': page}
    return render(request, 'hot.html',
                  context=add_sidebar_info(context))


@require_GET
def tag(request: HttpRequest, name: str) -> HttpResponse:
    questions = Question.objects.get_questions_by_tag(name)
    page = paginate(questions, request)
    context = {'tag': {'name': name}, 'page_obj': page}
    return render(request, 'tag.html',
                  context=add_sidebar_info(context))


@require_GET
def question(request: HttpRequest, question_id: int) -> HttpResponse:
    try:
        question_item = Question.objects.get_question_by_id(question_id).first()
    except IndexError:
        raise Http404
    question_item.answers = paginate(question_item.answer_set.all(), request)
    context = {'question': question_item, 'page_obj': question_item.answers}
    return render(request, 'question.html', context=add_sidebar_info(context))


def login(request: HttpRequest) -> HttpResponse:
    print(request.POST)
    return render(request, 'login.html', context=add_sidebar_info())


@require_GET
def signup(request: HttpRequest) -> HttpResponse:
    return render(request, 'signup.html', context=add_sidebar_info())


@require_GET
def ask(request: HttpRequest) -> HttpResponse:
    return render(request, 'ask.html', context=add_sidebar_info())


@require_GET
def settings(request: HttpRequest) -> HttpResponse:
    return render(request, 'settings.html', context=add_sidebar_info())
