from http import client
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
        # TODO: add permissions to this
        queryset = super().get_queryset()
        query_params = self.request.query_params

        # filter by archived field; exclude by default
        archived = query_params.get('archived')
        match archived:
            case 'only':
                queryset = queryset.filter(archived=True)
            case 'include':
                pass
            case _:
                queryset = queryset.exclude(status=False)

        # filter by client status; exclude by default
        client = query_params.get('client')
        match client:
            case 'only':
                queryset = queryset.filter(status=Lead.CLIENT)
            case 'include':
                pass
            case _:
                queryset = queryset.exclude(status=Lead.CLIENT)

        # filter by status
        status = query_params.get('status')
        if status: queryset = queryset.filter(status=status) 

        # filter by branch
        branch = query_params.get('branch')
        if branch: queryset = queryset.filter(branch__id=branch)
        
        # filter by assigned user; self by default
        assigned_to = query_params.get('assigned_to')
        if assigned_to == 'all': 
            pass
        elif assigned_to:
            queryset = queryset.filter(assigned_to=assigned_to)
        else:
            queryset = queryset.filter(assigned_to=self.request.user)

        return queryset

class NotePagination(PageNumberPagination):
    page_size = 8

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all().order_by('-created_at')
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
        # if created_by: queryset = queryset.filter(created_by=created_by) 
        
        return queryset
