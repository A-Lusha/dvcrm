from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('backoffice/', include('backoffice.urls')),

    # APIViews
    path('api/v1/', include('lead.urls')),
]
