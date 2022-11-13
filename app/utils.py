from django.core.paginator import Paginator, Page
from django.http import HttpRequest


def paginate(objects_list, request: HttpRequest, default_per_page=3) -> Page:
    page = request.GET.get('p') or 1
    per_page = request.GET.get('per_page') or default_per_page
    p = Paginator(objects_list, per_page)
    return p.get_page(page)
