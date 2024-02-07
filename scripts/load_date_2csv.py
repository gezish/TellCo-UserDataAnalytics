import os
import pandas as pd

def convert_to_csv(input_path, output_path):
    try:
        # Determine file type
        file_extension = os.path.splitext(input_path)[1].lower()

        # Read file based on file type
        if file_extension == '.csv':
            df = pd.read_csv(input_path)
        elif file_extension == '.xlsx':
            df = pd.read_excel(input_path)
        elif file_extension == '.json':
            df = pd.read_json(input_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        # Write to CSV
        df.to_csv(output_path, index=False)
        print(f"Conversion successful. CSV file saved at {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify input directory and output directory
    input_directory = "/path/to/your/files"
    output_directory = "/path/to/your/output"

    # Loop through files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(('.csv', '.xlsx', '.json')):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.csv")
            convert_to_csv(input_path, output_path)
