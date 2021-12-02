from django.urls import path
from .import base_views
app_name = 'GetUsed'
urlpatterns = [
    path('', base_views.IndexView.as_view(), name="index"),
    path('result/', base_views.ResultView.as_view(), name='result'),
]
