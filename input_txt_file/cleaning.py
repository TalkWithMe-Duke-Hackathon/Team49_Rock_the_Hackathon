import pandas as pd
import re

# Path to your text file
file_path = "formatted_sentences.txt"

# Initialize an empty list to store the cleaned text
cleaned_lines = []

# Read the text file line by line
with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        # Check if the line contains Chinese characters (assuming Chinese sentences have Chinese characters)
        if re.search(r"[\u4e00-\u9fff]", line):
            # Skip Chinese sentences
            continue
        # Remove Chinese characters and Chinese punctuation
        line = re.sub(r"[\u4e00-\u9fff，。]+", "", line)

        # Remove leading and trailing spaces
        line = line.strip('"').strip()

        # Add the cleaned line to the list without surrounding quotation marks
        cleaned_lines.append(line)

# Convert the list to a DataFrame
df = pd.DataFrame(cleaned_lines)

# Optional: Save the cleaned text to a new file
df.to_csv("cleaned_file.txt", sep="\t", index=False, header=None)


# import pandas as pd
# import re

# # Path to your text file
# file_path = "/Users/castnut/Desktop/input_txt_file/formatted_sentences.txt"

# # Initialize an empty list to store the cleaned text
# cleaned_lines = []

# # Read the text file line by line
# with open(file_path, "r", encoding="utf-8") as file:
#     for line in file:
#         if
#         # Remove Chinese characters
#         line = re.sub(r"[\u4e00-\u9fff]+", "", line)
#         # Remove Chinese punctuation
#         line = re.sub()
#         # Remove numbers and dots at the beginning
#         line = re.sub(r"^\d+\.", "", line).strip()
#         # Add the cleaned line to the list
#         cleaned_lines.append(line)

# # Convert the list to a DataFrame
# df = pd.DataFrame(cleaned_lines, columns=["cleaned_text"])

# # Optional: Save the cleaned text to a new file
# df.to_csv(
#     "/Users/castnut/Desktop/input_txt_file/cleaned_file.txt", index=False, header=None
# )
