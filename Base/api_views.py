from django.views import View

from Base.error import Error
from Base.response import response


class ErrorView(View):
    @staticmethod
    def get(request):
        return response(body=Error.get_error_dict())


class VersionView(View):
    @staticmethod
    def get(request):
        from VideoHandler.handler import Handler
        return response(body=dict(
            version=Handler.LATEST_VERSION,
            dv=Handler.DETAILED_DATE,
        ))
