import os
import csv
import sys

# Get the current directory
current_directory = os.getcwd()

# List all CSV files in the current directory
csv_files = [file for file in os.listdir(current_directory) if file.lower().endswith('.csv')]

if not csv_files:
    print("No CSV files found in the current directory.")
else:
    
    while True:
        # Ask the user to choose the mode
        print("Select a mode:")
        print("1 - Buildings in separate .csv files.")
        print("2 - All buildings in one file")
        print("3 - Quit")
        mode_choice = input("Choice (1, 2, or 3): ")

        # Columns to remove
        columns_to_remove = [5, 6, 9, 10, 11, 12, 13, 14, 15, 16]

        if mode_choice == "1":

            # Mode 1: Buildings are in separate .csv files
            for csv_file in csv_files:
                input_file_path = os.path.join(current_directory, csv_file)

                with open(input_file_path, 'r') as input_file:
                    csv_reader = csv.reader(input_file)
                    lines = list(csv_reader)

                    # Determine the output file name using the first data point
                    first_data_point = lines[0][0]
                    output_file_name = first_data_point + '.csv'

                    # Remove specified columns and write to the output file
                    output_file_path = os.path.join(current_directory, output_file_name)
                    with open(output_file_path, 'w', newline='') as output_file:
                        csv_writer = csv.writer(output_file)
                        for line in lines:
                            # Check if the value in the third column is "natural gas" or "wastewater"
                            if line[2].lower() not in ["natural gas", "wastewater"]:
                                modified_line = [line[i] for i in range(len(line)) if i not in columns_to_remove]
                                csv_writer.writerow(modified_line)

                    print(f"Columns removed, and lines with 'natural gas' or 'wastewater' deleted. Output saved to {output_file_name}")
                    sys.exit()

        elif mode_choice == "2":

            # Mode 2: Buildings are in the same .csv file (vertically positioned)
            all_buildings_file = "all_buildings.csv"

            with open(all_buildings_file, 'w', newline='') as output_file:
                csv_writer = csv.writer(output_file)
                previous_building = None
                empty_lines_added = 0

                for csv_file in csv_files:
                    input_file_path = os.path.join(current_directory, csv_file)

                    with open(input_file_path, 'r') as input_file:
                        csv_reader = csv.reader(input_file)
                        lines = list(csv_reader)

                        for line in lines:
                            # Check if the value in the third column is "natural gas" or "wastewater"
                            if line[2].lower() not in ["natural gas", "wastewater"]:
                                # Remove specified columns
                                modified_line = [line[i] for i in range(len(line)) if i not in columns_to_remove]

                                # Check if the building changes
                                if line[0] != previous_building:
                                    if previous_building is not None:
                                        # Add 5 empty lines if the building changes
                                        for _ in range(5):
                                            csv_writer.writerow([])
                                    empty_lines_added = 0
                                    previous_building = line[0]

                                csv_writer.writerow(modified_line)

                print(f"Columns removed, Natural Gas and Wastewater lines skipped, and output saved to {all_buildings_file}")
                sys.exit()

        elif mode_choice == "3":
            sys.exit()

        else:
            print("Invalid mode choice. Please enter 1, 2, or 3.")