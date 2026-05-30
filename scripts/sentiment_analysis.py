"""
Sentiment analysis of aggregated interview data using TextBlob.

Computes polarity (-1 negative to 1 positive) and subjectivity
(0 objective to 1 subjective) for the full document and per question.

Data file (data/Aggregated_EN.docx) is NOT included in this repository
for participant confidentiality reasons. See README.

Usage:
    python scripts/sentiment_analysis.py
"""

import os
import sys
import docx
from textblob import TextBlob

# Resolve data path relative to repo root, regardless of where the script is called from
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA = os.path.join(REPO_ROOT, "data", "Aggregated_EN.docx")
file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA

if not os.path.exists(file_path):
    sys.exit(
        f"\nData file not found at: {file_path}\n"
        "The aggregated interview data is confidential and not distributed "
        "with this repository.\nSee the README for how to request it, or pass "
        "a path: python scripts/sentiment_analysis.py path/to/file.docx\n"
    )


def load_docx(path):
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


doc_text = load_docx(file_path)
print("Document Loaded Successfully!")

# Full document
blob = TextBlob(doc_text)
sentiment = blob.sentiment
print("Full Document Sentiment Analysis:")
print("  Polarity:", sentiment.polarity)
print("  Subjectivity:", sentiment.subjectivity)


def split_by_questions(doc_text):
    questions = doc_text.split("Question ")
    question_data = {}
    for q in questions[1:]:
        lines = q.split("\n", 1)
        question_number = lines[0].strip(":")
        question_text = lines[1].strip()
        question_data[f"Question {question_number}"] = question_text
    return question_data


questions = split_by_questions(doc_text)

for question, text in questions.items():
    blob = TextBlob(text)
    sentiment = blob.sentiment
    print(f"\n{question} Sentiment Analysis:")
    print("  Polarity:", sentiment.polarity)
    print("  Subjectivity:", sentiment.subjectivity)
