import csv
import os

# Define the range of file indexes
start_idx = 0
end_idx = 44999

# Define the file name pattern and output file name
input_file_pattern = os.path.join("results", "result_{}.csv")
output_file_name = "combined_results.csv"

# Open the output file for writing
with open(output_file_name, mode='w', newline='') as outfile:
    # Create a CSV writer object
    writer = csv.writer(outfile)
    
    # Loop through each file index
    for idx in range(start_idx, end_idx + 1):
        # Construct the file name
        file_name = input_file_pattern.format(idx)
        try:
            # Open the input file for reading
            with open(file_name, mode='r', newline='') as infile:
                # Create a CSV reader object
                reader = csv.reader(infile)
                
                # Read the single row from the input file
                for row in reader:
                    # Write the row to the output file
                    writer.writerow(row)
        except FileNotFoundError:
            # If the file is not found, print a message and continue to the next file
            print(f"File {file_name} not found. Skipping...")

print("Combining completed!")

