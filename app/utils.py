from django.core.paginator import Paginator, Page
from django.http import HttpRequest

from app.models import Likeable, User

DEFAULT_PER_PAGE = 3


def paginate(objects_list, request: HttpRequest, default_per_page=DEFAULT_PER_PAGE) -> Page:
    page = request.GET.get('p') or 1
    per_page = request.GET.get('per_page') or default_per_page
    p = Paginator(objects_list, per_page)
    return p.get_page(page)


def add_reactions_to_likeables(likeables: list[Likeable], user: User):
    for likeable in likeables:
        if likeable.has_liked_by(user):
            likeable.liked = True
        elif likeable.has_disliked_by(user):
            likeable.disliked = True
    return likeables
