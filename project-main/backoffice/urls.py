from django.urls import re_path
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class BackofficeView(LoginRequiredMixin, TemplateView):
  template_name='backoffice/index.html'

urlpatterns = [
  re_path(r"^.*$", BackofficeView.as_view(), name='backoffice')
]

