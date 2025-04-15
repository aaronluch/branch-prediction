# Aaron Luciano
# CS 3220
# Branch Prediction Simulation
# 4/13/2025

# too many circular dependencies, so we move the predictions here, then theyre called in branch_pred.py
from typing import Tuple

def simulate_zero_bit_predictor(trace_data: list) -> Tuple[int, int]:
    correct_preds, incorrect_preds = 0, 0

    for address, outcome in trace_data:
        if outcome == 0:
            correct_preds += 1
        else:
            incorrect_preds += 1
    
    return correct_preds, incorrect_preds

def simulate_one_bit_predictor(trace_data: list, num_entries: int) -> Tuple[int, int]:
    predictor = [0] * num_entries  # initialize the predictor with 0s (not taken)
    correct_preds, incorrect_preds = 0, 0

    for address, outcome in trace_data:
        index = address % num_entries
        prediction = predictor[index] # stored result from last prediction
        if prediction == outcome:
            correct_preds += 1
        else:
            incorrect_preds += 1
        predictor[index] = outcome  # update the predictor with the actual outcome

    return correct_preds, incorrect_preds

def simulate_two_bit_predictor(trace_data: list, num_entries: int) -> Tuple[int, int]:
    # start with saturating counters (0 = strongly not taken | 1 = weakly not taken | 2 = weakly taken | 3 = strongly taken)
    predictor = [1] * num_entries  # initialize the predictor with weakly not taken
    correct_preds, incorrect_preds = 0, 0

    for address, outcome in trace_data:
        index = address % num_entries

        # predict taken if counter >= 2, not taken otherwise
        if predictor[index] >= 2:
            prediction = 1
        else:
            prediction = 0
        if prediction == outcome:
            correct_preds += 1
        else:
            incorrect_preds += 1
        
        # update the counter with saturating behavior
        if outcome == 1:
            predictor[index] = min(predictor[index] + 1, 3) # increment counter, saturate at 3
        else:
            predictor[index] = max(predictor[index] - 1, 0) # current branch is not taken, decrement counter, saturate at 0
        
    return correct_preds, incorrect_preds

def simulate_three_bit_predictor(trace_data: list, num_entries: int) -> Tuple[int, int]:
    # (0 = strongly not taken | 1 = weakly not taken | 2 = weakly taken | 3 = strongly taken)
    # counters are initialized to strongly taken (3) for a 3 bit saturating counter (range 0-7)
    predictor = [3] * num_entries  # initialize the predictor with strongly taken
    correct_preds, incorrect_preds = 0, 0

    for address, outcome in trace_data:
        index = address % num_entries

        # predict taken if counter >= 4, not taken otherwise
        if predictor[index] >= 4:
            prediction = 1
        else:
            prediction = 0
        if prediction == outcome:
            correct_preds += 1
        else:
            incorrect_preds += 1
        
        # update the counter with saturating behavior
        if outcome == 1:
            predictor[index] = min(predictor[index] + 1, 7)
        else:
            predictor[index] = max(predictor[index] - 1, 0)

    return correct_preds, incorrect_preds