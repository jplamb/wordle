from rest_framework import serializers
from .models import Word

class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'word', 'was_answer']
