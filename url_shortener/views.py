import logging

from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from url_shortener.models import RedirectCode


@require_http_methods(['GET', 'POST'])
def index(request):
    # As this app, for simplicity, doesn't use JavaScript, the home page and the shrinking are
    # in the same endpoint to simulate a single-page application.
    # This is just to keep the page's URL clean; a separate POST endpoint rendering index.html would have
    # a different path, and to redirect with a success message would require a path or query params.
    context = {}
    if request.method == 'POST':
        # Create a RedirectCode object and populate the context to display a success (or error) message.
        url = request.POST.get('url')
        if not url:
            context['error'] = 'URL cannot be blank!'
            return render(request, 'index.html', context=context)

        # See if this URL has been used before.
        redirect_code_obj = RedirectCode.objects.filter(url=url).first()
        # If not, create a new RedirectCode object and validate it, preparing error messages if there are any.
        if not redirect_code_obj:
            redirect_code_obj = RedirectCode(url=url, code=RedirectCode.generate_code())
            try:
                # Validate that the user-provided URL is in valid format.
                redirect_code_obj.full_clean()
                redirect_code_obj.save()
            except ValidationError as e:
                url_errors = e.message_dict.get('url')
                if url_errors:
                    context['error'] = url_errors[0] + ' (Did you forget the http/https?)'
                else:
                    # There should be no other validation errors, so log it and show user a generic error message.
                    logging.info(e.message_dict)
                    context['error'] = 'An error has occurred. Contact firerml@gmail.com to report this bug!'
                return render(request, 'index.html', context=context)

        # No errors? Populate context for success message.
        context['original_url'] = url
        context['new_url'] = request.build_absolute_uri() + redirect_code_obj.code
        context['url_length_difference'] = max(len(context['original_url']) - len(context['new_url']), 0)

    return render(request, 'index.html', context=context)


@require_http_methods(['GET'])
def redirect_from_code(request, code):
    # TODO: HTTP caching.
    redirect_code = RedirectCode.objects.filter(code=code).first()
    if not redirect_code:
        return redirect(index)
    return redirect(redirect_code.url)
