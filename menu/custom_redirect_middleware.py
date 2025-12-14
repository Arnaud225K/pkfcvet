from urllib.parse import urlparse, urlunparse

from django import http
from django.conf import settings
from django.contrib.redirects.models import Redirect
from django.contrib.sites.shortcuts import get_current_site

class CustomRedirectFallbackMiddleware:

    response_gone_class = http.HttpResponseGone
    response_redirect_class = http.HttpResponsePermanentRedirect

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code != 404:
            return response

        full_path = request.get_full_path()
        
        parsed_url = urlparse(full_path)
        path_without_query = parsed_url.path
        query_string = parsed_url.query

        current_site = get_current_site(request)

        r = None
        try:
            r = Redirect.objects.get(site=current_site, old_path=path_without_query)
        except Redirect.DoesNotExist:
            pass

        if r is None and settings.APPEND_SLASH and not request.path.endswith('/'):
            try:
                r = Redirect.objects.get(
                    site=current_site,
                    old_path=path_without_query + '/',
                )
            except Redirect.DoesNotExist:
                pass

        if r is not None:
            if r.new_path == '':
                return self.response_gone_class()

            new_path_parsed = urlparse(r.new_path)
            
            redirect_url = urlunparse((
                new_path_parsed.scheme,
                new_path_parsed.netloc,
                new_path_parsed.path,
                new_path_parsed.params,
                query_string,
                new_path_parsed.fragment
            ))
            
            return self.response_redirect_class(redirect_url)

        return response