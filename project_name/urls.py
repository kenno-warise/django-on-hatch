from django.urls import path
from . import views


urlpatterns = [
        path('', views.AppPageView.as_view(), name='index')
]

