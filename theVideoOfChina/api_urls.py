from django.urls import path, include

from theVideoOfChina.api_views import LinkView, JumpView

urlpatterns = [
    path('give-me-dl-link', LinkView.as_view()),
    path('jump-dl-link', JumpView.as_view()),
    path('base/', include('Base.api_urls')),
]