# %%
# LIBRARY
import os
import re

# %%
# FUNCTION
def split_text_file(input_file, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split content based on <img> tags
    # Using regex to split while keeping the delimiter
    parts = re.split(r'(<img[^>]*>)', content)

    # Initialize variables
    current_file_content = []
    file_counter = 1

    for part in parts:
        # Add each part to the current file content
        current_file_content.append(part)
        
        # If the part is an <img> tag, start a new file
        if part.startswith('<img'):
            # Write the accumulated content to a new file
            output_file = os.path.join(output_dir, f'part_{file_counter:03d}.txt')
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(''.join(current_file_content))
            
            # Reset content for the next file, starting with the current <img> tag
            current_file_content = [part]
            file_counter += 1
    
    # Write any remaining content to a final file
    if current_file_content:
        output_file = os.path.join(output_dir, f'part_{file_counter:03d}.txt')
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(''.join(current_file_content))

    # Return the total number of files created
    return file_counter - 1
# %%
# DATA
## Input File
input_file_path = "./input_files/GameOfThrones_3.txt"
output_dir_path = "./output_files"

# %%
# Example usage
if __name__ == "__main__":
    input_file = input_file_path  # Replace with your input file path
    output_dir = output_dir_path  # Directory where split files will be saved
    num_parts = split_text_file(input_file, output_dir)
    print(f"Files have been split into {num_parts} parts in {output_dir}/part_XXX.txt")

# %%
