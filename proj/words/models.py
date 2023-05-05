from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=100)
    was_answer = models.BooleanField(default=False)

    class Meta:
        app_label = 'words'
