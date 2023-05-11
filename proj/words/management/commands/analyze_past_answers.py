import os
import statistics
import pathlib

from django.core.management.base import BaseCommand

from proj.words.utils import get_previous_answers


class Command(BaseCommand):
    help = 'Create a random application token'
    path = pathlib.Path().absolute()

    def handle(self, *args, **kwargs):
        previous_answers = get_previous_answers(test_mode=False)
        common_words = self.get_common_words()
        familiar_words = self.get_familiar_words(common_words)
        self.analyze_answers(previous_answers, familiar_words)

    def analyze_answers(self, answers, familiar_words):
        print(f"Total words: {len(answers)}")
        skipped_words = 0
        familiarity_scores = []
        for word in answers:
            if word not in familiar_words:
                skipped_words += 1
            else:
                familiarity_scores.append(familiar_words[word])
                print(f"Word: {word} - familiarity: {familiar_words[word]}")

        print(f"Skipped words: {skipped_words}")
        print(f"Median familiarity: {statistics.median(familiarity_scores)}")
        print(f"Mean familiarity: {sum(familiarity_scores) / len(familiarity_scores)}")

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
                word_freq[word] = freq



        return word_freq

