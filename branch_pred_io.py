# Aaron Luciano
# CS 3220
# Branch Prediction IO Functions / Loading and Parsing Trace Files
# 4/12/2025

import os
from predictor_utils import *

# Loading and parsing trace files

# Prompt user to select a specific trace file
def select_trace_file() -> str:
    trace_dir = os.path.join(os.getcwd(), 'traces')
    trace_files = [f for f in os.listdir(trace_dir) if f.endswith('.out')]
    trace_files.sort()

    # available trace files
    print("Select a trace file:")
    for index, file in enumerate(trace_files, start=1):
        print(f"{index}. {file}")
    
    while True:
        try:
            choice = int(input(">>> Enter your choice (1-" + str(len(trace_files)) + "): "))
            if 1 <= choice <= len(trace_files):
                return os.path.join(trace_dir, trace_files[choice-1])
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(trace_files)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Load the trace file and parse it
def load_trace_file(file_path: str) -> list:
    trace_data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 2:
                    continue # skip invalid lines
                addr_str, outcome_str = parts
                try:
                    address = int(addr_str, 16) # convert hex address to int
                    outcome = int(outcome_str) # outcome to int
                    if outcome not in (0,1):
                        continue # skip invalid outcomes
                    trace_data.append((address, outcome))
                except ValueError:
                    continue
    except FileNotFoundError:
        print(f"Error reading file {file_path}. Please check the file format.")
        return None
    return trace_data

# Prompt user to select the number of predictor bits
def select_predictor_bits() -> int:
    valid_bits = {0, 1, 2, 3}
    while True:
        try:
            bits = int(input(">>> Enter the number of predictor bits (0-3): "))
            if bits in valid_bits:
                return bits
            else:
                print("Invalid choice. Please enter a number between 0 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Prompt user to select the size of the branch prediction buffer (can be an arbitrary size)
def select_branch_prediction_buffer_size() -> int:
    while True:
        try:
            size = int(input(">>> Enter the size of the branch prediction buffer (in bits): "))
            if size > 0:
                return size
            else:
                print("Buffer must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Just to break up the input prompts for readability
def print_div():
    print("-" * 80)

# Running tests based on user selection

def run_branch_prediction(trace_data: list, predictor_bits: int, buffer_size: int):
    total_branches = len(trace_data)

    if predictor_bits == 0:
        correct, incorrect = simulate_zero_bit_predictor(trace_data)
        num_entries = None
    else:
        # calculate number of entries in the buffer based on the number of bits
        num_entries = buffer_size // predictor_bits
        if predictor_bits == 1:
            correct, incorrect = simulate_one_bit_predictor(trace_data, num_entries)
        elif predictor_bits == 2:
            correct, incorrect = simulate_two_bit_predictor(trace_data, num_entries)
        elif predictor_bits == 3:
            correct, incorrect = simulate_three_bit_predictor(trace_data, num_entries)

    correct_percent = (correct / total_branches) * 100 if total_branches > 0 else 0
    incorrect_percent = (incorrect / total_branches) * 100 if total_branches > 0 else 0

    print("\n--- Branch Prediction Results ---")
    print(f"Total branches processed: {total_branches}")
    if predictor_bits > 0:
        print(f"BHT entries: {num_entries} (Buffer size: {buffer_size} bits, {predictor_bits} bits per counter)")
    print(f"Correct predictions: {correct} ({correct_percent:.2f}%)")
    print(f"Incorrect predictions: {incorrect} ({incorrect_percent:.2f}%)")
    print("---------------------------------")

    return correct, incorrect


# run individual test
def run_individual():
    # Load in the trace file
    trace_file = select_trace_file()
    print(f"Selected trace file: {trace_file}")

    # Load the trace data
    trace_data = load_trace_file(trace_file)
    print(f"Loaded {len(trace_data)} branch instructions from the trace file.")
    print_div()

    # Select the predictor bits
    predictor_bits = select_predictor_bits()
    print(f"Selected predictor bits: {predictor_bits}")
    print_div()

    # Select the size of the branch prediction buffer
    buffer_size = select_branch_prediction_buffer_size()
    print(f"Selected branch prediction buffer size: {buffer_size} bits")
    print_div()

    # Run the branch prediction simulation
    run_branch_prediction(trace_data, predictor_bits, buffer_size)

# run for all predictor bits in a specified trace file
def run_all():
    trace_file = select_trace_file()
    print(f"Selected trace file: {trace_file}")

    # Load the trace data
    trace_data = load_trace_file(trace_file)
    print(f"Loaded {len(trace_data)} branch instructions from the trace file.")
    print_div()

    # Select the size of the branch prediction buffer
    buffer_size = select_branch_prediction_buffer_size()
    print(f"Selected branch prediction buffer size: {buffer_size} bits")
    print_div()

    # Run the branch prediction simulation for all predictor bits
    for predictor_bits in range(4):
        print(f"\n\nRunning simulation with {predictor_bits} predictor bits...")
        run_branch_prediction(trace_data, predictor_bits, buffer_size)

# Clear terminal screen for better readability
def clear_terminal():
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # Unix/Linux/Mac
    else:
        os.system('clear')