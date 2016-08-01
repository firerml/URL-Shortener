from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from url_shortener.models import RedirectCode


@require_http_methods(['GET', 'POST'])
def index(request, return_json=False):
    # As this app, for simplicity, doesn't use JavaScript (outside of the copying functionality),
    # the home page and the shrinking are in the same endpoint to simulate a single-page application.
    # This is just to keep the page's URL clean; a separate POST endpoint rendering index.html would have
    # a different path, and to redirect with a success message would require a path or query params.
    context = {'error': ''}
    status = 200
    if request.method == 'POST':
        # Create a RedirectCode object and populate the context to display a success (or error) message.
        url = request.POST.get('url')
        redirect_code_data = RedirectCode.get_or_create_from_url(url)

        if redirect_code_data['error']:
            # Display what the user last typed in the input box so the user can fix it.
            context['error'] = redirect_code_data['error']
            if return_json:
                return JsonResponse(context, status=400)
            context['input_value'] = url
            return render(request, 'index.html', context=context, status=400)

        # No errors? Populate context for success message.
        redirect_code_obj = redirect_code_data['redirect_code_object']
        context['original_url'] = url
        context['new_url'] = redirect_code_obj.get_short_url()
        context['url_length_difference'] = max(len(context['original_url']) - len(context['new_url']), 0)
        context['redirect_code'] = redirect_code_obj.code
        if redirect_code_data['created']:
            status = 201

    if return_json:
        context.pop('input_value', '')
        return JsonResponse(context, status=status)

    # Wipe the input box on successful input.
    context['input_value'] = ''
    return render(request, 'index.html', context=context, status=status)


@require_http_methods(['GET'])
def redirect_from_code(request, code, return_json=False):
    redirect_code = RedirectCode.objects.filter(code=code).first()
    if not redirect_code:
        if return_json:
            return JsonResponse({'error': 'Code does not exist.'}, status=400)
        else:
            return redirect(index)
    if return_json:
        return JsonResponse({
            'error': '',
            'original_url': redirect_code.url,
            'short_url': redirect_code.get_short_url(),
            'code': redirect_code.code
        }, status=404)
    return redirect(redirect_code.url)


#######
# API #
#######

# All of the logic except the final return format is identical to logic found above, so no need to replicate it.

@require_http_methods(['GET'])
def api_get_redirect_code(request, code):
    return redirect_from_code(request, code, return_json=True)


@require_http_methods(['POST'])
def api_create_redirect_code(request):
    return index(request, return_json=True)
