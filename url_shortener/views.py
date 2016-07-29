from django.shortcuts import redirect, render
from django.http import HttpResponse

from url_shortener.models import RedirectCode


def index(request):
    return HttpResponse('hello there')


def redirect_from_code(request, code):
    # TODO: Let's use server-side caching for this to save the DB call.
    redirect_code = RedirectCode.objects.filter(code=code).first()
    if not redirect_code:
        return HttpResponse('NOT FOUND, DOOD.', status=404)
    return redirect(redirect_code.url)
