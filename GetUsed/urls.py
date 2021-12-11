from django.urls import path, include
from .import views
app_name = 'GetUsed'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('result/', views.ResultView.as_view(), name='result'),
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
]
