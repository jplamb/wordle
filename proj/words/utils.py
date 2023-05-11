import heapq
import math
import logging
import requests

from bs4 import BeautifulSoup

from proj.words.models import Word
from proj.settings.settings_loader import NUM_GUESSES_SUGGESTED, PAST_WORDLE_ANSWERS_URL, IS_TEST_MODE

LOG_LEVEL = logging.DEBUG

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,  # Set the lowest severity level to log
    format="%(asctime)s [%(levelname)s]: %(message)s",  # Set the log format
    datefmt="%Y-%m-%d %H:%M:%S"  # Set the date format
)


def get_previous_answers(test_mode=IS_TEST_MODE):
    # logging.info(f"Collecting past answers")
    if test_mode:
        return []

    response = requests.get(PAST_WORDLE_ANSWERS_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the header element containing the text "all wordle answers"
    header_el = soup.find('h2', string='All Wordle answers')

    # Find the <ul> element at the same level as the header element
    ul_el = header_el.find_next_sibling('ul')

    # Extract the text content of the <ul> element
    ul_content = ul_el.get_text(strip=False)
    words = set()
    for word_text in ul_content.split():
        word_text = word_text.lower()
        if len(word_text) != 5:
            continue
        words.add(word_text)
    return list(words)


def get_and_update_prior_answers():
    words = get_previous_answers()
    for word_text in words:
        try:
            Word.objects.filter(word=word_text).update(was_answer=True)
        except Word.DoesNotExist:
            continue


def prioritize(data):
    # Convert data into a max heap
    prepped_data = [(-score, word) for word, score in data.items()]
    heapq.heapify(prepped_data)
    return prepped_data


def suggest_guesses(feedback):
    all_words = Word.objects.all()
    eligible_words = get_eligible_words(feedback)
    # logging.info(f"There are {len(eligible_words)} eligible words remaining")

    letter_pos_freq, overall_letter_freq = create_frequency_set(eligible_words)

    words_by_entropy = rank_words_information_gain(all_words, letter_pos_freq, overall_letter_freq,
                                                   len(feedback) + 1)
    words_by_overall = rank_words(all_words, words_by_entropy, eligible_words, len(feedback) + 1)
    return get_top_suggestions(words_by_overall, words_by_entropy, eligible_words, len(feedback) + 1)


def get_top_suggestions(words_by_overall, words_by_entropy, eligible_words, guess_num=1):
    if guess_num == 2 and len(eligible_words) == 1:
        return [(eligible_words[0], 0, 0)]

    sorted_words_by_overall = prioritize(words_by_overall)
    sorted_words_by_entropy = prioritize(words_by_entropy)

    if guess_num < 3:
        # Recommend a guess that maximizes the letter-positional frequency score
        # This should be a guess maximizing the information learned from the guess
        suggested_guesses = []
        for i in range(min(NUM_GUESSES_SUGGESTED, len(sorted_words_by_entropy))):
            score, word = heapq.heappop(sorted_words_by_entropy)
            suggested_guesses.append((word, -1 * score, words_by_entropy[word] if word in words_by_entropy else 0))
        return suggested_guesses
    else:
        # On the third guess and beyond, choose the word maximizing commonality with a slight preference for
        # letter-positional frequency
        suggested_guesses = []
        for i in range(min(NUM_GUESSES_SUGGESTED, len(eligible_words))):
            score, word = heapq.heappop(sorted_words_by_overall)
            suggested_guesses.append((word, -1 * score, words_by_entropy[word] if word in words_by_entropy else 0))
        return suggested_guesses


def get_eligible_words(feedback):
    # Feedback is a list of lists. Each sub-list is a tuple of guess to the info gained.
    # The info gained has length 5 where each individual entry is
    # "-" (not in word), "y" (in word), or "g" (correct position)
    letters_not_in_answer = set()
    letters_in_answer = set()
    letters_known_pos = ["*"] * 5
    letters_known_not_pos = [set([]) for _ in range(5)]
    for guess, info in feedback:
        # logging.info(f"Guess: {guess}, Feedback: {info}")
        for i in range(5):
            letter = guess[i]
            learned = info[i]
            if learned == "*" and letter not in letters_in_answer:
                letters_not_in_answer.add(letter)
            elif learned == "*" and letter in letters_in_answer:
                letters_known_not_pos[i].add(letter)
            elif learned == "y":
                letters_in_answer.add(letter)
                letters_known_not_pos[i].add(letter)
            elif learned == "g":
                letters_in_answer.add(letter)
                letters_known_pos[i] = letter

    # logging.debug(f"Letters not in answer: {letters_not_in_answer}")
    # logging.debug(f"Letters in answer: {letters_in_answer}")
    # logging.debug(f"Letters known position: {letters_known_pos}")
    # logging.debug(f"Letters known not in this position: {letters_known_not_pos}")
    eligible_words = []
    word_set = Word.objects.all() if IS_TEST_MODE else Word.objects.filter(was_answer=False)
    for word in word_set:
        word_text = word.word
        # logging.debug(f"Checking {word}: {letters_in_answer.issubset(word)} and {letters_not_in_answer.isdisjoint(word)}")
        if letters_in_answer.issubset(word_text) and letters_not_in_answer.isdisjoint(word_text):
            for i, letter in enumerate(word_text):
                check_letter = letters_known_pos[i]
                if (check_letter != "*" and letter != check_letter):
                    break
                if letter in letters_known_not_pos[i]:
                    break
            else:
                eligible_words.append(word)

    return eligible_words


def create_frequency_set(five_letter_words):
    # create frequency set by position
    # return frequency set

    # logging.info("Determining the frequency of letters in words and positions")
    letter_freq = {}
    position_freq_count = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
    # Count the occurrences of letters
    for word in five_letter_words:
        word_text = word.word
        # iterate over each character in the string with the letter's index
        for pos, letter in enumerate(word_text):
            # How often does the letter appear in each position?
            if letter not in position_freq_count[pos + 1]:
                position_freq_count[pos + 1][letter] = 1
            else:
                position_freq_count[pos + 1][letter] += 1

            # How often does the letter appear overall?
            if letter not in letter_freq:
                letter_freq[letter] = 1
            else:
                letter_freq[letter] += 1

    total = len(five_letter_words)
    position_freq = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
    # Convert frequency to probability
    for pos in range(1, 6):
        for letter in position_freq_count[pos]:
            position_freq[pos][letter] = position_freq_count[pos][letter] / total

    overall_letter_freq = {}
    for letter in letter_freq:
        overall_letter_freq[letter] = letter_freq[letter] / total

    return position_freq, overall_letter_freq


def rank_words_information_gain(word_list, letter_pos_freq, overall_letter_freq, guess_num):
    # rank words by information gain
    # Thanks to https://www.3blue1brown.com/lessons/wordle for jogging my memory on how to do this
    # logging.info("Ranking words by information gain")
    word_entropy = {}
    for word in word_list:
        entropy = 0
        letters_seen = {}
        # logging.debug(f"\nInfo Gain - Word: {word}")
        for i, letter in enumerate(word.word):
            # Take the probability of the letter occurring in the word and multiply it by the information gain of the
            # letter in that particular position
            if letter not in letters_seen and letter in overall_letter_freq:
                prob_of_letter_in_word = (1 - overall_letter_freq[letter])
                info_gained_letter_in_word = -1. * prob_of_letter_in_word * math.log2(prob_of_letter_in_word) if prob_of_letter_in_word > 0 else 0
                # logging.debug(f"Letter in word: {letter} {prob_of_letter_in_word} {info_gained_letter_in_word}")
                letters_seen[letter] = 1
            else:
                info_gained_letter_in_word = 0

            if letter not in letter_pos_freq[i + 1]:
                info_gained_letter_in_pos = 0
            else:
                # Information gained is the -log2(p) where p is the probability of...
                letter_pos_prob = (1 - letter_pos_freq[i + 1][letter])
                info_gained_letter_in_pos = -1. * letter_pos_prob * math.log2(letter_pos_prob) if letter_pos_prob > 0 else 0
                # logging.debug(f"Letter in pos: {letter} {letter_pos_prob} {info_gained_letter_in_pos}")
            if guess_num < 3:
                entropy += 0.6 * info_gained_letter_in_word + 0.4 * info_gained_letter_in_pos
            else:
                entropy += 0.1 * info_gained_letter_in_word + 0.9 * info_gained_letter_in_pos
            # logging.debug(f"Entropy: {entropy}")
        word_entropy[word] = entropy

    return word_entropy


def rank_words(all_words, words_by_entropy, eligible_words, guess_num):
    # rank words by commonality and frequency
    # return dictionary of words sorted by commonality and frequency (most common first)
    # logging.info("Creating an overall ranking by information gained with word familiarity")

    # If we're on the first guess, only use the eligible words for a change at a hole in one
    if guess_num == 1:
        guess_list = eligible_words
    # For guess two, choose the word with best info gained even if it's not a possible answer
    elif guess_num == 2:
        guess_list = list(all_words)
    # Only suggest possible answers
    else:
        guess_list = eligible_words

    ranked_words = {}
    for word in guess_list:
        freq_score = word.familiarity if word.familiarity > 0 else 0.001
        info_gained = words_by_entropy[word] if word in words_by_entropy else 0
        # Given the remaining set of options, compute how likely it is to be the answer by combining the info gained
        # with how common the word is
        # Probability of being the answer based on commonality
        ranked_words[word] = freq_score * info_gained
        # logging.debug(f"Rank words: {word} {freq_score} {info_gained} {ranked_words[word]}")

    return ranked_words
