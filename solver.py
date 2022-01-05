import sys
import re
import numpy as np

WORD_LENGTH = 5
ALL_WORDS = [word.strip() for word in open("wordlist.txt", 'r').readlines()]
NUM_WORDS = len(ALL_WORDS)
REVERSE_WORD_INDEX = {w: i for (i, w) in enumerate(ALL_WORDS)}

""" Compute the best guess that maximizes our information gain on the remaining words. """
def BestGuess(remaining_words):
    best_guess, best_guess_score = None, sys.maxsize
    for potential_guess in ALL_WORDS:
        feedback_counts = np.zeros(3 ** WORD_LENGTH)
        for potential_answer in remaining_words:
            feedback_index = FEEDBACK_PAIRS[REVERSE_WORD_INDEX[potential_guess], REVERSE_WORD_INDEX[potential_answer]]
            feedback_counts[feedback_index] += 1
        score = np.max(feedback_counts)
        if score < best_guess_score:
            best_guess, best_guess_score = potential_guess, score
    return best_guess

""" Turns a feedback string of the form [.?*]{5} into an integer [0, 242] """
def EncodeFeedbackString(feedback_string):
    feedback = 0
    for i, c in enumerate(feedback_string):
        if c == "*":
            feedback += 2 * (3**i)
        elif c == "?":
            feedback +=     (3**i)
    return feedback

""" Return only those words from the word list that yield the same feedback string as the one we got. """
def PruneWordlist(guess, feedback_string, word_list):
    return [word for word in word_list if FEEDBACK_PAIRS[REVERSE_WORD_INDEX[guess], REVERSE_WORD_INDEX[word]] == EncodeFeedbackString(feedback_string)]


if __name__ == "__main__":
    print("Welcome to MattR's shitty Wordle engine, programmed for lulz.")
    FEEDBACK_PAIRS = np.load('feedback_pairs.npy')
    word_list = ALL_WORDS.copy()
    guess = "ARISE"
    validator = re.compile("^[\.\?\*]{5}$")

    print("Try first guess: %s" % guess)
    print("Next, report the puzzle engine's feedback in the following format:")
    print("For each letter that was completely wrong, put a dot (.)")
    print("For each letter that was right, but in the wrong spot, put a ?")
    print("For each letter that was right, and in the right spot, put a *")
    print("For instance, if you guessed ARISE and saw that the A was correct, and the S and E were in the wrong spots, your input should be *..??")

    while len(word_list) > 1:
        print("AI chooses %s to maximize information gain." % guess)
        feedback_string = input("Input feedback string: ")
        while not validator.match(feedback_string):
            print("Invalid feedback string, try again.")
            feedback_string = input("Input feedback string: ")

        word_list = PruneWordlist(guess, feedback_string, word_list)
        print("Pruned list of legal words: ")
        print(word_list)
        guess = BestGuess(word_list)
    
    print("You win! The word has been discovered to be %s." % word_list[0])