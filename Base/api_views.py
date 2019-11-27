from SmartDjango import E
from django.views import View


class ErrorView(View):
    @staticmethod
    def get(request):
        return E.all()


class VersionView(View):
    @staticmethod
    def get(request):
        from VideoHandler.handler import Handler
        return dict(
            version=Handler.LATEST_VERSION,
            dv=Handler.DETAILED_DATE,
        )
