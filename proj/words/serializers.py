from rest_framework import serializers
from .models import Word

class WordItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'word', 'was_answer']

class SuggestedWordsSerializer(serializers.ModelSerializer):
    score = serializers.ReadOnlyField()
    info_gain = serializers.ReadOnlyField()
    class Meta:
        model = Word
        fields = ['id', 'word', 'score', 'info_gain']

    def to_representation(self, instance):
        # Set the custom field data on the serializer
        self.fields['score']._readable = True
        self.fields['score']._value = instance.score
        self.fields['info_gain']._readable = True
        self.fields['info_gain']._value = instance.info_gain

        return super().to_representation(instance)
