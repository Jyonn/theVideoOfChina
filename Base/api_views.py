from django.views import View

from Base.error import Error
from Base.response import response


class ErrorView(View):
    @staticmethod
    def get(request):
        return response(body=Error.get_error_dict())
