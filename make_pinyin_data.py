import pandas as pd
from pathlib import Path
from pypinyin import lazy_pinyin, Style

# Define the root directory and data file path
ROOT_DIR = Path.home() / "chinese_study_app"
DATA_FILE = ROOT_DIR / "data" / "cmn.txt"

# Read the TSV file
df = pd.read_csv(DATA_FILE, sep='\t', header=None, names=['english', 'chinese', 'meta'])

# Remove duplicate entries
df = df.drop_duplicates(subset=['english', 'chinese'])

# Function to convert Chinese text to pinyin with tone marks
def to_pinyin(text):
    return ' '.join(lazy_pinyin(text, style=Style.TONE))

# Apply the function to create a new 'pinyin' column
df['pinyin'] = df['chinese'].apply(to_pinyin)

# Display the first few rows
print(df.head())

# Optionally, save the processed DataFrame to a new file
df.to_csv(ROOT_DIR / "data" / "cmn_with_pinyin.tsv", index=False, sep='\t')
