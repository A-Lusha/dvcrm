from rest_framework import serializers

from account.serializers import UserSerializer, BranchSerializer

from .models import Lead, Note

class LeadSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    branch = BranchSerializer(read_only=True)
    status = serializers.ChoiceField(choices=Lead.STATUS_CHOICES)
    
    class Meta:
        model = Lead
        read_only_fields = (
            'created_by',
            'created_at',
            'modified_at',
        )
        fields = (
            'id',
            'business_name',
            'contact_person',
            'contact_email',
            'contact_phone',
            'contact_ext',
            'website',
            'estimated_value',
            'status',
            'branch',
            'assigned_to',
            'created_at',
            'modified_at',
        )

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
