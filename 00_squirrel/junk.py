import random

file_path = 'dancecard.txt'  # Replace 'your_file.txt' with the actual path to your text file

def get_text_from_line(file_path, line_number):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if 1 <= line_number <= len(lines):
            return lines[line_number - 1]
        else:
            return f"Line number {line_number} is out of range."

# Generate a random line number between 1 and 400
random_line_number = random.randint(1, 400)

# Get the text from the randomly chosen line
random_line_text = get_text_from_line(file_path, random_line_number)

print(f"Random Line Number: {random_line_number}")
print(f"Text from Line {random_line_number}: {random_line_text}")

