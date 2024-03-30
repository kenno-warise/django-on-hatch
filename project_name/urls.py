from django.urls import path  # type: ignore

from . import views


app_name = '{{ project_name }}'

urlpatterns = [
    path('', views.AppPageView.as_view(), name='index')
    # path('example/', views.Example.as_view(), name='example')
]
