from SmartDjango import Packing, ErrorDict
from django.views import View


class ErrorView(View):
    @staticmethod
    @Packing.http_pack
    def get(request):
        return ErrorDict.all()


class VersionView(View):
    @staticmethod
    @Packing.http_pack
    def get(request):
        from VideoHandler.handler import Handler
        return dict(
            version=Handler.LATEST_VERSION,
            dv=Handler.DETAILED_DATE,
        )
