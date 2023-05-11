
import nltk
import pathlib

from django.core.management.base import BaseCommand

from proj.words.models import Word


class Command(BaseCommand):
    help = 'Create a random application token'
    path = pathlib.Path().absolute()

    def handle(self, *args, **kwargs):
        test_mode = False
        for word in Word.objects.all():
            pos_tag = nltk.pos_tag([word.word])[0][1]

            if pos_tag in ('NNS', 'NNP', 'NNPS', 'VBN', 'VBD'):
                if test_mode:
                    print(f"Found ineligible word: {word.word} - {pos_tag}")
                else:
                    word.delete()





