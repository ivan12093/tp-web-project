from math import ceil

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.http import HttpResponse, HttpRequest, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from app.forms import LoginForm, RegisterForm, UpdateUserForm, CreateQuestionForm, CreateAnswerForm
from app.models import Question, Tag, User, Likeable, Answer
from app.utils import paginate, DEFAULT_PER_PAGE


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


def question(request: HttpRequest, question_id: int) -> HttpResponse:
    question_item = Question.objects.get_question_by_id(question_id)
    if not question_item:
        raise Http404
    if request.method == 'GET':
        answer_form = CreateAnswerForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'login/?continue=question/{question_id}')
        answer_form = CreateAnswerForm(data=request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(request.user, question_item)
            per_page = request.GET.get('per_page') or DEFAULT_PER_PAGE
            count_of_answers = question_item.answer_set.count()
            page_to_jump = ceil(count_of_answers / per_page)
            return redirect(f'{request.path}?p={page_to_jump}&per_page={per_page}#{answer.id}')

    question_item.answers = paginate(question_item.answer_set.all().order_by('id'), request)
    context = {'question': question_item, 'page_obj': question_item.answers, 'form': answer_form}
    return render(request, 'question.html', context=add_sidebar_info(context))


def login(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        user_form = LoginForm()
    if request.method == 'POST':
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request, **user_form.cleaned_data)
            if user is not None and user.is_active:
                auth.login(request, user)
                redirect_path = request.GET.get('continue') or '/'
                return redirect(redirect_path)
            else:
                user_form.add_error(field=None, error='Wrong username or password')
    context = add_sidebar_info()
    context['form'] = user_form
    return render(request, 'login.html', context=context)


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        register_form = RegisterForm()
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            register_form.save()
            user = auth.authenticate(request, **register_form.cleaned_data)
            auth.login(request, user)
            return redirect(reverse('index'))

    context = add_sidebar_info()
    context['form'] = register_form
    return render(request, 'signup.html', context=context)


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    redirect_path = request.GET.get('next') or '/'
    return redirect(redirect_path)


@login_required(login_url='/login', redirect_field_name='continue')
def ask(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        question_form = CreateQuestionForm()
    if request.method == 'POST':
        question_form = CreateQuestionForm(data=request.POST)
        if question_form.is_valid():
            question_item = question_form.save(request.user)
            return redirect(f'question/{question_item.id}')

    context = add_sidebar_info()
    context['form'] = question_form
    return render(request, 'ask.html', context=context)


@login_required(login_url='/login', redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
def settings(request: HttpRequest) -> HttpResponse:
    user_id = request.user.id
    if request.method == 'GET':
        user_data = model_to_dict(request.user)
        user_data.pop('password')
        user_data.pop('avatar')
        update_form = UpdateUserForm(initial=user_data)
    if request.method == 'POST':
        update_form = UpdateUserForm(data=request.POST, files=request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            user = auth.authenticate(request, **update_form.cleaned_data)
            auth.login(request, user)
            return redirect(reverse('settings'))
        else:
            request.user = User.objects.get(id=user_id)

    context = add_sidebar_info()
    context['form'] = update_form
    return render(request, 'settings.html', context=context)


@require_POST
@login_required(login_url='/login', redirect_field_name='continue')
def like(request: HttpRequest):
    object_type = request.POST['object_type']
    item_id = request.POST['id']
    if object_type == 'question':
        item = Question.objects.get_question_by_id(item_id)
    else:
        item = Answer.objects.get_answer_by_id(item_id)
    if not item:
        return JsonResponse({'status': 'not found'})
    if item.has_liked_by(request.user):
        item.unlike(request.user)
    else:
        item.like(request.user)
    return JsonResponse({
        'status': 'ok',
        'rating': item.rating
    })


@require_POST
@login_required(login_url='/login', redirect_field_name='continue')
def dislike(request: HttpRequest):
    object_type = request.POST['object_type']
    item_id = request.POST['id']
    if object_type == 'question':
        item = Question.objects.get_question_by_id(item_id)
    else:
        item = Answer.objects.get_answer_by_id(item_id)
    if not item:
        return JsonResponse({'status': 'not found'})
    if item.has_disliked_by(request.user):
        item.undislike(request.user)
    else:
        item.dislike(request.user)
    return JsonResponse({
        'status': 'ok',
        'rating': item.rating
        })

@require_POST
@login_required(login_url='/login', redirect_field_name='continue')
def correct(request: HttpRequest):
    question_id = request.POST['question_id']
    answer_id = request.POST['answer_id']
    is_correct = request.POST['correct'] == 'true'

    question_item = Question.objects.get_question_by_id(question_id)
    if question_item.author != request.user:
        raise PermissionDenied()

    answer_item = Answer.objects.get_answer_by_id(answer_id)
    answer_item.set_correctness(is_correct)

    return JsonResponse({'status': 'ok', 'correct': is_correct})
