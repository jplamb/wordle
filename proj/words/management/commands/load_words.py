import os
import pathlib

from django.core.management.base import BaseCommand

from proj.words.models import Word


class Command(BaseCommand):
    help = 'Create a random application token'
    path = pathlib.Path().absolute()

    def handle(self, *args, **kwargs):
        common_words = self.get_common_words()
        familiar_words = self.get_familiar_words(common_words)
        test_mode = False
        self.create_words(familiar_words, test_mode)

    def create_words(self, familiar_words, test_mode):
        for word, familiarity in familiar_words.items():
            if test_mode:
                print(f"Creating word: {word} - {familiarity}")
            else:
                Word.objects.create(word=word, familiarity=familiarity)

    def get_common_words(self):
        filename = os.path.join(self.path, "proj/words/management/data/common_words.txt")
        words = {}
        with open(filename, 'r') as f:
            for line in f:
                word, freq = line.strip().split(',')
                words[word] = float(freq)
        return words

    def get_familiar_words(self, common_words):
        filename = os.path.join(self.path, "proj/words/management/data/word_freq_measure.txt")
        word_freq = {}
        with open(filename, 'r') as f:
            for line in f:
                word, freq = line.strip().split(',')
                # Poor man's sigmoid function
                freq = float(freq)
                if freq < 3:
                    adj_score = 0.001
                else:
                    adj_score = 0.25
                word_freq[word] = adj_score

        for word in common_words:
            if word not in word_freq:
                word_freq[word] = 0.25

        return word_freq

