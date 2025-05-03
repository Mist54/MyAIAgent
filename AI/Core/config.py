import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTE_DIR = os.path.join(BASE_DIR, "..", "Notes")

# Ensure note directory exists
os.makedirs(NOTE_DIR, exist_ok=True)
