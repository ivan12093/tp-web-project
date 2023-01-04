from django.core.paginator import Paginator, Page
from django.http import HttpRequest

DEFAULT_PER_PAGE = 3


def paginate(objects_list, request: HttpRequest, default_per_page=DEFAULT_PER_PAGE) -> Page:
    page = request.GET.get('p') or 1
    per_page = request.GET.get('per_page') or default_per_page
    p = Paginator(objects_list, per_page)
    return p.get_page(page)
