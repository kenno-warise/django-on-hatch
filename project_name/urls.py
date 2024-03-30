from django.urls import path  # type: ignore
from . import views


urlpatterns = [
    path('', views.AppPageView.as_view(), name='index')
    # path('example/', views.Example.as_view(), name='example')
]
