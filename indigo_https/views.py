import requests
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings
from requests.auth import HTTPDigestAuth


class IndigoView(View):

    def build_url(self, requset):
        url = 'http://%s%s' % (settings.INTERNAL_INDIGO_HOST, requset.get_full_path())
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
