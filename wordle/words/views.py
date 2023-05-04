from django.shortcuts import render
from rest_framework import viewsets
from .models import Word
from .serializers import TodoItemSerializer

class WordItemViewset(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = TodoItemSerializer

def index(request):
    print('index')
    return render(request, 'words/index.html')