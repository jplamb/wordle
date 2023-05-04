import nltk

# Download the Brown Corpus
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')

# Load the corpus into a list
from nltk.corpus import brown
words = brown.words()

# Count the frequency of each word
word_freq = {}
for word in words:
    pos_tag = nltk.pos_tag([word])[0][1]
    # if word.lower() == "delve":
    #     print(f"{word} - {pos_tag}")

    if word.isalpha() and len(word) == 5 and pos_tag not in ('NNS', 'NNP', 'NNPS', 'VBN', 'VBD'):
        word = word.lower()

        # if word == 'cried':
        #     print(f"{word} - {pos_tag}")
        word_freq[word] = word_freq.get(word, 0) + 1

# Sort the words by frequency in descending order
sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
total_words = len(words)
# Save the 100 most common words to a text file
with open('common_words.txt', 'w') as f:
    for word, freq in sorted_words:
        f.write(f"{word},{freq/total_words * 100.}\n")
