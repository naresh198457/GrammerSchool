import pdfplumber

def extract_questions_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

import sqlite3

conn = sqlite3.connect('exams.db')
cur = conn.cursor()

# Create table for questions
cur.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER,
    question TEXT,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct_option TEXT
)
''')

# Insert mock questions (example)
cur.execute("INSERT INTO questions (exam_id, question, option_a, option_b, option_c, option_d, correct_option) VALUES (?, ?, ?, ?, ?, ?, ?)", 
           (1, "Example question", "Option A", "Option B", "Option C", "Option D", "A"))

conn.commit()
conn.close()


def load_exams():
    questions_data = extract_questions_from_pdf('GL-Assessment-Verbal-Reasoning-Familiarisation-Test-1.pdf')
    # Process the extracted text into exam sets
    for i in range(20):
        # Insert 20 sets of questions into the database
        store_questions_in_db(i, questions_data)