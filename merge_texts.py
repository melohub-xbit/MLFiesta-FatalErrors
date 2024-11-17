import os
import glob

def merge_text_files(input_directory, output_file):
    # Get all text files in the directory
    text_files = glob.glob(os.path.join(input_directory, "*.txt"))
    
    # Create or overwrite the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Iterate through each text file
        for txt_file in text_files:
            print(f"Processing: {txt_file}")
            
            # Read and write content of each file
            with open(txt_file, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                # Add a newline between files
                outfile.write('\n\n')
    
    print(f"All files merged successfully into: {output_file}")

# Example usage
input_dir = "D:/forKrishna/Dell-ForKrishna-All/MLFiesta/text_dataset"
output_file = "D:/forKrishna/Dell-ForKrishna-All/MLFiesta/merged_data.txt"

# Create directory if it doesn't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Merge the files
merge_text_files(input_dir, output_file)
