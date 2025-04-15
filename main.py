# Aaron Luciano
# CS 3220
# Assignment 4 - Branch Prediction
# 4/12/2025

from branch_pred_io import run_all, run_individual, clear_terminal
from gen_graphs import *

def main_menu():
    while True:
        width = 60
        border = "=" * width
        header_text = "Branch Prediction Menu".center(width)

        menu_prompt = (
            f"\n{border}\n"
            f"{header_text}\n"
            f"{border}\n"
            "1. Test specific amount of predictor bits on a trace file\n"
            "2. Test all predictor bits on a trace file\n"
            "3. Generate CSV Output Files for each trace\n"
            "4. Generate Charts\n"
            "5. Clear Output Directory\n"
            "6. Exit\n"
            f"{border}\n"
            ">>> Choose: "
        )

        selection = input(menu_prompt)
        
        if selection == "1":
            run_individual()
        elif selection == "2":
            run_all()
        elif selection == "3":
            generate_csv_results()
        elif selection == "4":
            generate_charts()
        elif selection == "5":
            clear_output_dir()
        elif selection == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid selection. Please try again.")
        
        input("\nPress Enter to return to the main menu...")
        clear_terminal()

if __name__ == "__main__":
    main_menu()