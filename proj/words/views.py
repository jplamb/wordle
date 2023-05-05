from django.shortcuts import render
from rest_framework import viewsets
from .models import Word
from .serializers import WordItemSerializer

class WordItemViewset(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordItemSerializer

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

def index(request):
    return render(request, 'words/index.html')