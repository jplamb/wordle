### tldr
WordleBot is designed to assist you in making the best guess for NYTimes' game, Wordle. It uses information theory to identify words eliminating the greatest number of possible answers.

From a gamesmanship perspective, WordleBot makes a few assumptions:
1. Solving the puzzle in three guesses is ideal. Solving it in less than three guesses is usually luck
2. While the set of possible answers (and allowable guesses) is available in Wordle's html, based on user research, it's really not in the spirit of the game.
3. While solving the puzzle in a single guess is lucky, it still feels good. WordleBot will suggest a guess that has not been a prior answer on the off chance you get a "word in one"

The word list is downloaded from the Brown nltk corpus. It is then combined with SUBTLEX-US corpus. The latter provides a score for how familiar a word is likely to be. Familiarity is useful in providing a rough approximation for how likely a word is to be the answer as unusual words are less likely to be the solution. WordleBot uses a sigmoid function to separate likely answers from not likely.

Using this word list, two frequency maps are created. The first tracks how often each letter appears in the combined word set. The second tracks the positional frequency of each letter in the word set.

Given these frequency maps, WordleBot uses information theory to identify the word that eliminates the greatest number of possible answers. Depending on the number of guesses, it will combine the information gained with the familiarity of the word. 

WordleBot was originally a simple cron job. I've since added a rudimentary web UI using Django + React.

---
### Intro


Fads come and go. Sometimes you're the one who sticks with it even after the hype has faded. Well, for my family, friends, and I Wordle is the fad we haven't let go of.

It's a simple game, you have six guesses to determine the secret, five-letter word. There's only one puzzle each day and it's the same for everyone.

There are countless articles about "winning" at Wordle or "Here's the best word to start with". Occasionally someone suggests the best starting **pair of guesses**. But I don't think that's all that interesting.

### Measuring Success


Here's the thing. If you solve Wordle on your first guess, that's mostly luck. We all know it. It's like a hole in one. You were aiming for the hole and it just happened to bounce in. It's an accomplishment but not one of skill.

If you solve it in two guesses, that's still mostly luck. There are just too many possibilities to skillfully solve the puzzle in two guesses (most of the time).

Solve it on the third guess, now that's the sweet spot. That requires strategic guessing. 

Solving it on the fourth guess is typically not challenging. 

I don't play on hard mode because I think it robs the game of the extra strategy. Strategy here requires taking the knowledge you have and guessing a word that will eliminate as many candidate words as possible. There's just not enough room to really employ that kind of strategy on hard mode.

### What are we doing here?


Ok, let's recap. Solving Wordle in a single guess is lucky but fun. Solving in two guesses is still primarily luck. Solving it in three is the pinnacle of skill. And four guesses is unimpressive.

As you may have figured out, I made a WordleBot that strives to solve the puzzle in three guesses. And it's pretty good at doing so. 

I'm certainly not the first person to build a Wordle-solving bot but they use information that's kinda sorta cheating. When you load up Wordle in your browser, the full set of possible answers for any game of Wordle is hidden in the page's code. There's a separate, longer list of words that comprise the words that are acceptable guesses. Is using those lists of words cheating? I dunno, but I'm striving to create a bot that has access to the same amount of information as normal, human players.

This WordleBot uses a random set of frequently used English words. I pair that with a rough measure of how common each word is based on often it is used. Meaning this WordleBot has an extensive vocabulary with a rough sense of which words are more common than others. Hopefully, that sounds vaguely like how you and I approach this problem. 

### The theory


Now for the technical. WordleBot's strategy is based on Information Theory. Information theory is a subject area that deals with how much stuff can you pack in a particular space. Imagine a friend of yours that never stops talking. They likely inefficiently pack information into their words. information / words = low signal. Poetry is the opposite. It typically uses few words and packs a ton of meaning into them. That's a high signal. You can also think of this in terms of packing your car for vacation. Someone in your family is likely the designated car packer because they can cram the most amount of stuff into the trunk. That's high signal. 

Let's apply this to Wordle. If your first guess is "storm" and your second guess is "stork", you're unlikely to solve the puzzle in three guesses. Unless of course you had four greens from "storm".

A good first and second guess are ones eliminating the greatest number of possible remaining answers. That is information gain. The more possible answers eliminated by a guess, the higher the information gain. One more technical topic. Entropy. Entropy measures the amount of chaos in a system. In this case, the unpredictableness of the Wordle solution is high entropy. When you narrow down the answer to a smaller and smaller pool of possible answers, the entropy is lowered relative to when you started because the final answer is becoming more predictable. We want to use words that reduce the entropy of the answer set by guessing words that provide high information gain. 

### The Nuts and Bolts


As I said up top, WordleBot has access to a large set of English words. For that set of words, we go through each one and analyze its letters. How many times does the letter "f" appear in the word list? And, how many times does"f" appear as the third letter in a word? WordleBot does this calculation for every word and each letter slot (from 1-5). The end result is a frequency map of how often a letter appears in the remaining answer set and how frequently a letter appears in each position of a word in the answer set. 

Now WordleBot takes each word and computes the information gain for it. It uses the formula for information entropy. Let's take an example: arise. 


1. How likely is it for "a" to be in the set of remaining answers?
2. How likely is it for "a" to be the first letter in the set of remaining answers?
3. Repeat for "r", "i", "s", and "e"

That gives us 10 entropy numbers. WordleBot combines these measures together to create a ranking of how much information would be gained by guessing that word.

WordleBot recommends the top 10 words based on information gain.

Upon guessing that word and learning more information, WordleBot uses that feedback to determine what words in the answer set are still eligible to be the solution.

After the first two guesses, WordleBot can usually narrow it down to a small subset of answers. This is where word familiarity plays a role. Typically, the solution to Wordle is a well known word. So WordleBot takes the information gained by each remaining possible solution and combines it with a rough measure of "is this word well known". This is a simple trick to recommend words that are more likely to be the answer because they're a more familiar word.
