from django.views.generic.base import TempateView


class HomePageView(TemplateView):
    template_name = "{{ app_name }}/index.html"
