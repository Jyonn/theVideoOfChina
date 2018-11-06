from django.urls import path, include

from theVideoOfChina.api_views import LinkView

urlpatterns = [
    path('give-me-dl-link', LinkView.as_view()),
    path('base/', include('Base.api_urls')),
]