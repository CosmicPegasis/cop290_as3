def calc_score(to_score, reference, note_length):
    score = 0
    for i in range(len(to_score)):
        to_score[i][2] /= note_length
    for i in range(min(len(to_score), len(reference))):
        if to_score[i][1] == reference[i][1] and to_score[i][0] == reference[i][0]:
            score += 50
            if to_score[i][2] <= (reference[i][2] + 200) or to_score[i][2] >= (
                reference[i][2] - 200
            ):
                score += 25

    return score
