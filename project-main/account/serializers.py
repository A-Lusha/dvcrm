from rest_framework import serializers
from .models import Branch, CustomUser as User

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = (
            'id',
            'name',
        )

class UserSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'branch',
            'first_name',
            'last_name',
        )

