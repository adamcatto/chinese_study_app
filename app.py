import datetime
from pathlib import Path
import random

import pandas as pd
import streamlit as st

# Define root directory and data file w/ 中文 , eng , and pinyin
ROOT_DIR = Path.home() / "chinese_study_app"
DATA_FILE = ROOT_DIR / "data" / "cmn_with_pinyin.tsv"

# Load the data
df = pd.read_csv(DATA_FILE, sep='\t')

# Initialize session state for spaced repetition
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = df.to_dict(orient='records')
    random.shuffle(st.session_state.flashcards)
    st.session_state.current_index = 0
    st.session_state.review_data = {i: {'interval': 1, 'ease': 2.5, 'next_review': datetime.date.today()} for i in range(len(st.session_state.flashcards))}

# Function to update spaced repetition schedule
def update_spaced_repetition(card_idx, quality):
    data = st.session_state.review_data[card_idx]
    if quality >= 3:
        if data['interval'] == 1:
            data['interval'] = 6
        else:
            data['interval'] = round(data['interval'] * data['ease'])
        data['ease'] += (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    else:
        data['interval'] = 1
    data['next_review'] = datetime.date.today() + datetime.timedelta(days=data['interval'])

# Display the current flashcard
current_idx = st.session_state.current_index
card = st.session_state.flashcards[current_idx]
review_info = st.session_state.review_data[current_idx]

if review_info['next_review'] <= datetime.date.today():
    st.subheader("Conversational Chinese Flashcard")
    st.write(f"**Chinese:** {card['chinese']}")
    st.write(f"**Pinyin:** {card['pinyin']}")

    if st.button("Show English"):
        st.write(f"**English:** {card['english']}")

    quality = st.radio("How well did you remember?", [5, 4, 3, 2, 1, 0], index=2, format_func=lambda x: ["Perfect", "Good", "Correct", "Hesitant", "Incorrect", "Complete blackout"][5-x])
    if st.button("Submit and Next"):
        update_spaced_repetition(current_idx, quality)
        st.session_state.current_index = (current_idx + 1) % len(st.session_state.flashcards)
        st.rerun()
else:
    st.info("No flashcards due today! Come back tomorrow.")

