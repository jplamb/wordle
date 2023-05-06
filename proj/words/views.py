import heapq
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Word
from .serializers import WordItemSerializer, SuggestedWordsSerializer
from .utils import get_and_update_prior_answers, suggest_guesses


class WordItemViewset(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordItemSerializer


class SuggestWordsView(APIView):
    def post(self, request, *args, **kwargs):
        guesses = request.data.get('guesses', [])
        feedback = request.data.get('feedback', [])
        if len(guesses) != len(feedback):
            return Response({"error": "Data provided is invalid."}, status=status.HTTP_400_BAD_REQUEST)

        get_and_update_prior_answers()

        suggestions = suggest_guesses([(guess, feedback) for guess, feedback in zip(guesses, feedback)])
        if len(suggestions) == 0:
            return Response([], status=status.HTTP_200_OK)
        ranked_guesses = [
            self._attach_rank_data(word, score, info_gain)
            for word, score, info_gain in suggestions
        ]

        serializer = SuggestedWordsSerializer(ranked_guesses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def _attach_rank_data(word, score, info_gain):
        word.score = score
        word.info_gain = info_gain
        return word

def index(request):
    return render(request, 'words/index.html')