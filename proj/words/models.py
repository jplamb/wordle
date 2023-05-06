from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=100, unique=True)
    was_answer = models.BooleanField(default=False)
    familiarity = models.FloatField(default=0.0)

    class Meta:
        app_label = 'words'

    def __str__(self):
        return self.word

    def __lt__(self, other):
        return self.familiarity < other.familiarity
