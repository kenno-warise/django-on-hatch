from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = "{{ app_name }}/index.html"
