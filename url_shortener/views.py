import logging

from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from url_shortener.models import RedirectCode


@require_http_methods(['GET', 'POST'])
def index(request):
    context = {}

    # As this app doesn't use JavaScript for the sake of simplicity, the GET and POST functionality are
    # used for the same endpoint to simulate a single-page application.
    # This is just to keep the page's URL clean; a separate POST endpoint rendering index.html would have
    # a different path, and to redirect with a success message would require a path or query params.
    if request.method == 'POST':
        # Create a RedirectCode object and populate the context to display a success (or error) message.
        url = request.POST.get('url')
        redirect_code_obj = RedirectCode(url=url, code=RedirectCode.generate_code())
        try:
            # TODO: If this url already exists in DB, fetch code.
            # TODO: Needs DB index on url.
            # Validate that the user-provided URL is in valid format.
            redirect_code_obj.full_clean()
            redirect_code_obj.save()
            context['original_url'] = url
            context['new_url'] = request.build_absolute_uri() + redirect_code_obj.code
        except ValidationError as e:
            url_errors = e.message_dict.get('url')
            if url_errors:
                context['error'] = url_errors[0]
            else:
                # There should be no other validation errors, so log it and show user a generic error message.
                logging.info(e.message_dict)
                context['error'] = 'An error has occurred. Contact firerml@gmail.com to report this bug!'

    return render(request, 'index.html', context=context)


@require_http_methods(['GET'])
def redirect_from_code(request, code):
    # TODO: Let's use server-side caching for this to save the DB call.
    redirect_code = RedirectCode.objects.filter(code=code).first()
    if not redirect_code:
        return HttpResponse('NOT FOUND, DOOD.', status=404)
    return redirect(redirect_code.url)
