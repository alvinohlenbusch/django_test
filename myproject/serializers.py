from api.models import Note, Account
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Account
        fields = ('id', 'title', 'accountNumber', 'created_by')
        lookup_field = 'pk'
        
class NoteSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, read_only=True)
    
    class Meta:
        model = Note
        fields = ('id', 'title', 'body', 'accounts')
        lookup_field = 'pk'