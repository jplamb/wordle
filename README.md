WordleBot is designed to assist you in making the best guess for NYTimes' game, Wordle. It uses information theory to identify words eliminating the greatest number of possible answers.

From a gamesmanship perspective, WordleBot makes a few assumptions:
1. Solving the puzzle in three guesses is ideal. Solving it in less than three guesses is usually luck
2. While the set of possible answers (and allowable guesses) is available in Wordle's html, based on user research, it's really not in the spirit of the game.
3. While solving the puzzle in a single guess is lucky, it still feels good. WordleBot will suggest a guess that has not been a prior answer on the off chance you get a "word in one"

The word list is downloaded from the Brown nltk corpus. It is then combined with SUBTLEX-US corpus. The latter provides a score for how familiar a word is likely to be. Familiarity is useful in providing a rough approximation for how likely a word is to be the answer as unusual words are less likely to be the solution. WordleBot uses a sigmoid function to separate likely answers from not likely.

Using this word list, two frequency maps are created. The first tracks how often each letter appears in the combined word set. The second tracks the positional frequency of each letter in the word set.

Given these frequency maps, WordleBot uses information theory to identify the word that eliminates the greatest number of possible answers. Depending on the number of guesses, it will combine the information gained with the familiarity of the word. 

WordleBot was originally a simple cron job. I've since added a rudimentary web UI using Django + React.
