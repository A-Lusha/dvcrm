from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import LeadViewSet, NoteViewSet

router = DefaultRouter()
router.register('leads', LeadViewSet, basename='leads')
router.register('notes', NoteViewSet, basename='notes')

urlpatterns = [
    # path('leads/delete_lead/<int:lead_id>/', delete_lead, name='delete_lead'),
    path('', include(router.urls)),
]