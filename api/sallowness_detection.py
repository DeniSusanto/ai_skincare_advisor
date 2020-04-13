def get_sallowness_score(real_age, predicted_age):
    if predicted_age <= real_age:
        return 0
    else:
        diff = predicted_age - real_age
        if diff <= 5:
            score = diff/5
        else:
            score = 1 + ((diff - 5)/5)
        return score
        