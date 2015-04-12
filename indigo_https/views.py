import json
import requests
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings
from requests.auth import HTTPDigestAuth


try:
    with open('path_aliases.json') as json_data:
        _path_aliases = json.load(json_data)
except:
    _path_aliases = {}


class IndigoView(View):

    def get_alias(self, path):
        if path.startswith('/'):
            path = path[1:]
        if path.endswith('/'):
            path = path[:-1]
        alias = _path_aliases.get(path, None)
        return alias

    def build_url(self, request):
        full_path = request.get_full_path()
        path_alias = self.get_alias(request.path)
        if path_alias is not None:
            full_path = full_path.replace(request.path, path_alias, 1)
        url = 'http://%s%s' % (settings.INTERNAL_INDIGO_HOST, full_path)
        return url

    def get(self, request, **kwargs):
        url = self.build_url(request)
        user_name = settings.INDIGO_USERNAME
        password = settings.INDIGO_PASSWORD

        response = requests.get(url, auth=HTTPDigestAuth(user_name, password))
        return HttpResponse(response.content)

    def post(self, request, **kwargs):
        return self.put(request, **kwargs);

    def put(self, request, **kwargs):
        url = self.build_url(request)
        user_name = settings.INDIGO_USERNAME
        password = settings.INDIGO_PASSWORD

        response = requests.put(url, request.POST, auth=HTTPDigestAuth(user_name, password))
        return HttpResponse(response.content)
