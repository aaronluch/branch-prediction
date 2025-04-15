# Aaron Luciano
# CS 3220
# Branch Prediction Graphing and CSV Generation
# 4/14/2025

from branch_pred_io import run_branch_prediction, load_trace_file
import matplotlib.pyplot as plt
import numpy as np
import os
import csv

# This entire file is mainly just utility functions to generate the CSV files and charts
# So arguably not relevant to the assigned task other than for comparative purposes

# Load all trace files NAMES into a list
def load_all_trace_files() -> list:
    trace_dir = os.path.join(os.getcwd(), 'traces')
    trace_files = [f for f in os.listdir(trace_dir) if f.endswith('.out')]
    trace_files.sort()
    trace_file_paths = [os.path.join(trace_dir, file) for file in trace_files]
    
    return trace_file_paths

# Generate CSV results for all trace files (make an individual CSV for each trace file)
def generate_csv_results():
    print("Current directory:", os.getcwd())
    all_files = load_all_trace_files()
    buffer_sizes = [256, 512, 768, 1024]
    pred_bits = [0, 1, 2, 3]

    for trace_path in all_files:
        trace_data = load_trace_file(trace_path)
        
        base_name = os.path.basename(trace_path)
        csv_filename = os.path.splitext(base_name)[0] + ".csv"
        csv_filename = os.path.join("output", csv_filename)
        
        with open(csv_filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "num_predictor_bits",
                "branch_prediction_buffer",
                "correct_predictions"
            ])
            
            for bits in pred_bits:
                for buffer_size in buffer_sizes:
                    correct_preds, incorrect_preds = run_branch_prediction(trace_data, bits, buffer_size)
                    percentage = correct_preds / (correct_preds + incorrect_preds) * 100
                    percentage = round(percentage, 2)
                    writer.writerow([
                        bits,
                        buffer_size,
                        percentage
                    ])
        print(f"CSV results for {trace_path} generated in file: {csv_filename}")

# Generate charts from the CSV files (as one combined chart)
def generate_charts():
    output_dir = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_dir) or not os.path.isdir(output_dir):
        print(f"Output directory '{output_dir}' does not exist or is not a directory")
        return

    csv_files = [f for f in os.listdir(output_dir) if f.endswith(".csv")]
    if not csv_files:
        print(f"No CSV files found in the output directory '{output_dir}'.")
        return

    csv_files.sort()
    
    fig, axs = plt.subplots(2, 2, figsize=(19, 10))
    axs = axs.flatten()
    for ax, csv_file in zip(axs, csv_files):
        csv_path = os.path.join(output_dir, csv_file)
        data = {}
        with open(csv_path, 'r', newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    pred_bit = int(row["num_predictor_bits"])
                    buffer_size = int(row["branch_prediction_buffer"])
                    percentage = float(row["correct_predictions"])
                except ValueError:
                    continue

                if buffer_size not in data:
                    data[buffer_size] = {}
                data[buffer_size][pred_bit] = percentage

        buffer_sizes = [256, 512, 768, 1024]
        predictor_bits = [0, 1, 2, 3]

        x = np.arange(len(buffer_sizes)) * 1.5
        width = 0.2

        for i, pred in enumerate(predictor_bits):
            percentages = [data.get(bs, {}).get(pred, 0) for bs in buffer_sizes]
            offset = (i - 1.5) * width
            ax.bar(x + offset, percentages, width, label=f"{pred} bit")

        ax.set_xlabel("Buffer Size")
        ax.set_ylabel("Percentage Correct")
        ax.set_title(os.path.splitext(csv_file)[0])
        ax.set_xticks(x)
        ax.set_xticklabels([str(bs) for bs in buffer_sizes])
        ax.set_ylim(0, 100)
        ax.grid(axis="y", linestyle='--', alpha=0.7)
        ax.legend(title="Predictor Bits", loc='upper left', bbox_to_anchor=(1, 1))
        ax.set_facecolor("#f0f0f0")

    plt.tight_layout()
    combined_chart_filename = os.path.join(output_dir, "combined_chart.png")
    plt.savefig(combined_chart_filename)
    plt.show()
    plt.close(fig)
    print(f"Combined chart generated and saved as {combined_chart_filename}")

# Clear the output directory (run a 2 step check to make sure they are sure)
def clear_output_dir():
    confirmation = input("Are you sure you want to clear the output directory? (y/n): ").strip().lower()
    if confirmation != 'y':
        print("Output directory not cleared.")
        return
    elif confirmation == 'y':
        print("Clearing output directory...")
        output_dir = os.path.join(os.getcwd(), "output")
        if os.path.exists(output_dir) and os.path.isdir(output_dir):
            for file in os.listdir(output_dir):
                file_path = os.path.join(output_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        os.rmdir(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
            print(f"Output directory '{output_dir}' cleared.")
        else:
            print(f"Output directory '{output_dir}' does not exist or is not a directory.")