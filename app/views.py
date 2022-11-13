from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

from app.models import QUESTIONS
from app.utils import paginate


@require_GET
def index(request: HttpRequest) -> HttpResponse:
    questions = QUESTIONS['questions']
    context = {'page_obj': paginate(questions, request)}
    return render(request, 'index.html', context=context)


@require_GET
def hot(request: HttpRequest) -> HttpResponse:
    questions = QUESTIONS['questions']
    context = {'page_obj': paginate(questions, request)}
    return render(request, 'hot.html', context=context)


@require_GET
def tag(request: HttpRequest, name: str) -> HttpResponse:
    questions = QUESTIONS['questions']
    context = {'page_obj': paginate(questions, request), 'tag': {'name': name}}
    print(context)
    return render(request, 'tag.html', context=context)


@require_GET
def question(request: HttpRequest, question_id: int) -> HttpResponse:
    for question_item in QUESTIONS['questions']:
        if question_item['id'] == question_id:
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
