""" Adel Liu 180226

base子路由
"""
from django.urls import path

from Base.api_views import ErrorView, VersionView

urlpatterns = [
    path('errors', ErrorView.as_view()),
    path('version', VersionView.as_view()),
]
