""" A tiny script to generate the feedback pairs data table for the solver. """
import tqdm
import numpy as np
import solver

# Compute the (integer-coded) feedback value for a guess/answer pair.
def Feedback(guess, answer):
    feedback = 0
    for i, g in enumerate(guess):
        offset = 3**i
        if g == answer[i]:
            feedback += 2 * offset
        elif g in answer:
            feedback += 1 * offset
    return feedback


# A reasonably large computation, quadratic in wordlist size. 
# Compute and store the (integer-coded) feedback value for each word pair in the dictionary.
# This table is just stored as a numpy array of bytes, which compresses nicely.
if __name__ == "__main__":
    print("Running feedback pair table generation.")
    feedback_pairs = np.zeros((solver.NUM_WORDS, solver.NUM_WORDS), dtype=np.uint8)
    for i, w1 in tqdm.tqdm(list(enumerate(solver.ALL_WORDS))):
        for j, w2 in enumerate(solver.ALL_WORDS):
            feedback_pairs[i, j] = Feedback(w1, w2)

    np.save('feedback_pairs.npy', feedback_pairs)    
    print("Done successfully.")

