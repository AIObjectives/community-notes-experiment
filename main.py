# Inspired by Vitalik's post and code:
# https://vitalik.ca/general/2023/08/16/communitynotes.html
# https://github.com/ethereum/research/blob/master/community_notes_analysis/basic_algo.py

import random
import time
import sys 

def load_matrix(folder):
    matrix = []
    with open(f"./data/{folder}/participants-votes.csv") as f:
        lines = f.readlines()
    for line in lines[1:]:
        matrix.append([int(x if x != '' else '0') for x in line.strip().split(',')[7:]])
    people = len(matrix)
    notes = len(matrix[0])
    print("Loaded {} people, {} notes".format(people, notes))
    return matrix 

def cost(matrix, intercept, user_friendliness, note_quality, user_alignment, note_alignment):
    people = len(matrix)
    notes = len(matrix[0])
    total = 0
    for i in range(people):
        for j in range(notes):
            expected_value = (
                intercept +
                user_friendliness[i] +
                note_quality[j] +
                user_alignment[i] * note_alignment[j]
            )
            total += (matrix[i][j] - expected_value) ** 2
    # Add regularization params
    total += 0.15 * sum(v**2 for v in ([intercept] * people + user_friendliness + note_quality))
    total += 0.05 * sum(v**2 for v in (user_alignment + note_alignment))
    return total

def naive_descent(matrix, folder):
    people = len(matrix)
    notes = len(matrix[0])
    intercept = [random.randrange(1000) / 1000]
    user_friendliness = [random.randrange(1000) / 1000 for _ in range(people)]
    note_quality = [random.randrange(1000) / 1000 for _ in range(notes)]
    user_alignment = [random.randrange(1000) / 1000 for _ in range(people)]
    note_alignment = [random.randrange(1000) / 1000 for _ in range(notes)]
    score = cost(
        matrix, intercept[0], user_friendliness, note_quality, user_alignment, note_alignment
    )
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
                        matrix, intercept[0], user_friendliness,
                        note_quality, user_alignment, note_alignment
                    )
                    if score < new_score:
                        var[i] -= delta
                    else:
                        improvements += 1
                        score = new_score
                        if improvements % 50 == 0:
                            ellapsed = time.time() - timestart
                            print("Round {}, improvements {}, cost: {}, ellapsed: {}".format(round, improvements, score, ellapsed))
                            with open(f"./data/{folder}/note_alignment.txt", 'w') as f:
                                f.write(','.join([str(x) for x in note_alignment]))
                            with open(f"./data/{folder}/note_quality.txt", 'w') as f:
                                f.write(','.join([str(x) for x in note_quality]))

        # If we can't descend any further, exit
        if score == start_round_score:
            print("Finished descending")
            break
    return note_quality


if __name__ == '__main__':
    folder = sys.argv[1]
    matrix = load_matrix(folder)
    naive_descent(matrix, folder)
