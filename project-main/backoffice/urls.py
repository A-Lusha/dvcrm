from django.urls import re_path
from django.views.generic.base import TemplateView

urlpatterns = [
  re_path(r"^.*$", TemplateView.as_view(template_name='backoffice/index.html'), name='backoffice')
]

