from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .models import Lead, Note
from .serializers import LeadSerializer, NoteSerializer

class LeadPagination(PageNumberPagination):
    page_size = 8

class LeadViewSet(viewsets.ModelViewSet):
    serializer_class = LeadSerializer
    queryset = Lead.objects.all().order_by('created_at')

    pagination_class = LeadPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('business_name', 'contact_person')
    
    def perform_create(self, serializer):
        # TODO: add permissions to this and perform_update
        user = self.request.user
        serializer.save(created_by=user, assigned_to=user, branch=user.branch)
    
    def get_queryset(self):
        queryset = super().get_queryset()

        # filter by branch
        branch = self.request.query_params.get('branch')
        if branch: queryset = queryset.filter(branch__id=branch)
        
        # filter by assigned user
        assigned_to = self.request.query_params.get('assigned_to')
        if assigned_to == 'all': 
            queryset = queryset.filter()
        elif assigned_to:
            queryset = queryset.filter(assigned_to=assigned_to)
        else:
            queryset = queryset.filter(assigned_to=self.request.user)

        # filter by status
        status = self.request.query_params.get('status')
        if status: queryset = queryset.filter(status=status) 
        
        return queryset

class NotePagination(PageNumberPagination):
    page_size = 8

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all().order_by('created_at')
    pagination_class = NotePagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('body',)
    
    def perform_create(self, serializer):
        # TODO: add permissions to this and perform_update
        user = self.request.user
        serializer.save(created_by=user)

    def get_queryset(self):
        queryset = super().get_queryset()

        # filter for specific lead
        lead = self.request.query_params.get('lead')
        if lead: queryset = queryset.filter(lead=lead)

        # filter assigned user
        created_by = self.request.query_params.get('created_by')
        if created_by: queryset = queryset.filter(created_by=created_by) 
        
        return queryset
