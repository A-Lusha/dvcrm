from rest_framework import serializers

from account.serializers import UserSerializer, BranchSerializer

from .models import Lead, Note

class LeadSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    branch = BranchSerializer(read_only=True)
    status = serializers.ChoiceField(choices=Lead.STATUS_CHOICES, default=Lead.NEW)
    status_display = serializers.SerializerMethodField()
    class Meta:
        model = Lead
        read_only_fields = (
            'created_by',
            'created_at',
            'modified_at',
        )
        fields = (
            'id',

            'company_name',
            'street',
            'city',
            'zipcode',
            'state',
            'website',
            'estimated_value',

            'contact_first_name',
            'contact_last_name',
            'contact_email',
            'contact_phone',
            'contact_ext',
            
            'status',
            'status_display',
            'branch',
            'assigned_to',
            'created_at',
            'modified_at',
            'archived'
        )
    
    def get_status_display(self, obj):
        return obj.get_status_display()

class NoteSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Note
        read_only_fields = (
            'created_by',
            'created_at',
            'modified_at',
        )
        fields = '__all__'
