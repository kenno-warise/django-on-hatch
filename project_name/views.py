from django.shortcuts import render  # type: ignore
from django.views.generic.base import View  # type: ignore


class AppPageView(View):
    def get(self, request):
        try:
            return render(request, "{{ project_name }}/base_index.html")
        except Exception as inst:
            return render(request, "{{ project_name }}/index.html")
