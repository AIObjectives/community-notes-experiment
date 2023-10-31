import random
import time
import sys
import numpy as np

FILLING_VALUE = 0  # change to np.nan to ignore predictions for missing values


def load_matrix(folder):
    matrix = np.genfromtxt(f"./data/{folder}/participants-votes.csv", filling_values=FILLING_VALUE,
                           delimiter=',', skip_header=1, dtype=float, invalid_raise=False)[:, 7:]
    people, notes = matrix.shape
    print("Loaded {} people, {} notes".format(people, notes))
    print(matrix)
    return matrix


def cost(matrix, intercept, user_friendliness, note_quality, user_alignment, note_alignment):
    expected_values = (
        intercept +
        user_friendliness[:, np.newaxis] +
        note_quality[np.newaxis, :] +
        np.outer(user_alignment, note_alignment)
    )
    error = matrix - expected_values
    total = np.nansum(error ** 2)
    # Add regularization params
    people, notes = matrix.shape
    total += 0.15 * ((intercept ** 2) * people * notes +
                     np.sum(user_friendliness ** 2) +
                     np.sum(note_quality ** 2) +
                     np.sum(user_alignment ** 2) +
                     np.sum(note_alignment ** 2))
    return total


def naive_descent(matrix, folder):
    people, notes = matrix.shape
    intercept = np.array([random.random()])
    user_friendliness = np.random.random(people)
    note_quality = np.random.random(notes)
    user_alignment = np.random.random(people)
    note_alignment = np.random.random(notes)
    score = cost(matrix, intercept[0], user_friendliness,
                 note_quality, user_alignment, note_alignment)
    improvements = 0
    timestart = time.time()
    for round in range(9**99):
        round_delta = max(0.001, 0.1 / (round+1)**0.5)
        start_round_score = score
        # Try tweaking each value up and down, and see if that reduces the cost.
        # If it does, keep the change.
        for var in (intercept, user_friendliness, note_quality, user_alignment, note_alignment):
            for i in range(len(var)):
                for delta in (round_delta, -round_delta):
                    var[i] += delta
                    new_score = cost(
                        matrix, intercept[0], user_friendliness, note_quality, user_alignment, note_alignment)
                    if score < new_score:
                        var[i] -= delta
                    else:
                        improvements += 1
                        score = new_score
                        if improvements % 50 == 0:
                            elapsed = time.time() - timestart
                            print("Round {}, improvements {}, cost: {}, elapsed: {}".format(
                                round, improvements, score, elapsed))
                            np.savetxt(
                                f"./data/{folder}/note_alignment.txt", note_alignment, delimiter=',')
                            np.savetxt(
                                f"./data/{folder}/note_quality.txt", note_quality, delimiter=',')
        # If we can't descend any further, exit
        if score == start_round_score:
            print("Finished descending")
            break


if __name__ == '__main__':
    folder = sys.argv[1]
    matrix = load_matrix(folder)
    naive_descent(matrix, folder)
