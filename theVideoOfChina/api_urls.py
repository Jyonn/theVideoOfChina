from django.urls import path, include

from theVideoOfChina.api_views import get_dl_link

urlpatterns = [
    path('give-me-dl-link', get_dl_link),
    path('base/', include('Base.api_urls')),
]