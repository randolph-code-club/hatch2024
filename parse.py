import csv
import os

def write_columns_to_files(file_path):
    try:
        with open(file_path, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="\t")
            
            # Read the header row to get column names
            headers = next(csv_reader)

            # Create a directory to store individual column files
            output_directory = 'column_files'
            os.makedirs(output_directory, exist_ok=True)

            # Create a separate file for each column and write data
            for i, header in enumerate(headers):
                column_file_path = os.path.join(output_directory, f'{header}.txt')
                with open(column_file_path, 'w') as column_file:
                    column_file.write(header + '\n')  # Write header to the file

                    # Write the data from the corresponding column
                    for row in csv_reader:
                        column_file.write(row[i] + '\n')

                # Reset file pointer for the next column
                csv_file.seek(0)
                next(csv_reader)  # Skip the header row

            print(f"Columns written to individual files in the '{output_directory}' directory.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'your_file.csv' with the actual file name or path
csv_file_path = 'tcga.gene_sums.LUAD.G026.csv'
write_columns_to_files(csv_file_path)
