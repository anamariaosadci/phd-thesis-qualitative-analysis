import os
import sys
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from docx import Document
import nltk

# Download NLTK stopwords
nltk.download('stopwords')

# Defined compound terms
COMPOUND_TERMS = {
    'book_market': ['book market', 'market', 'book industry', 'industry', 'book business'],
    'business_model': ['business model', 'business models', 'business plan', 'model'],
    'printed_book': ['print book', 'physical format', 'copies', 'printed format', 'printed book', 'print books', 'printed books', 'physical book', 'print', 'printed', 'physical'],
    'e_book': ['e-book', 'ebook', 'e-books', 'ebooks', 'electronic book', 'digital book'],
    'audiobook': ['audio book', 'audio books', 'audiobook', 'audiobooks', 'audio format'],
    'manuscripts': ['works', 'literary works', 'written works', 'title', 'titles'],
    'digital_content': ['digital content', 'digital service', 'digital media'],
    'print_on_demand': ['print on demand', 'print-on-demand', 'POD'],
    'platform': ['platform', 'platforms', 'digital platform'],
    'digital_licensing': ['licensing', 'digital licensing'],
    'post_pandemic': ['post pandemic'],
    'post_production': ['post production'],
    'digital_marketing': ['digital marketing', 'online marketing', 'digital promotion', 'online promotion'],
    'e_commerce': ['e-commerce', 'ecommerce', 'electronic commerce', 'online sales'],
    'online_platform': ['online platform', 'online platforms', 'online service', 'online market'],
    'online_bookstore': ['online bookstore', 'online bookstores', 'online store','online stores', 'website'],
    'digital_format': ['digital format'],
    'online_library': ['online_library', 'online libraries'],
    'social_media': ['social media', 'social network', 'social', 'media'],
    'audience_reach': ['audience', 'reach', 'target audience', 'market reach'],
    'post_launch': ['post launch'],
    'book_launch': ['book launch', 'launch', 'launches', 'book launches'],
    'subscription': ['subscription', 'subscription service', 'subscription model', 'subscription based'],
    'crowdfunding': ['crowd funding', 'crowdfunding', 'crowd-funding'],
    'direct_sales': ['direct sale', 'direct sales', 'direct selling', 'direct'],
    'self_help_books': ['self help', 'personal development', 'self-help'],
    'artificial_intelligence': ['artificial intelligence'],
    'Romanian_authors': ['Romanian author', 'Romanian authors'],
    'authors': ['author', 'authors'],
    'children_books': ['children book', 'children', 'children books', 'books for children'],
    'book_consumers': ['reader', 'readers', 'people', 'listeners'],
    'book_consumption': ['reading', 'read', 'listen', 'listening'],
    'self_publishing': ['self publishing', 'self publish', 'self-publishing'],
    'experimenting': ['try', 'tried', 'experiment', 'experimented'],
    'payment': ['payment', 'pay'],
    'abroad': ['abroad', 'countries', 'states'],
    'not_enough': ['not enough'],
    'direct_payment': ['direct payment'],
    'online_payment': ['online payment'],
    'content_protection': ['content protection'],
    'sales': ['sales', 'sell'],
    'support': ['support', 'supported'],
}

# Defined custom stop words
CUSTOM_STOP_WORDS = set(['romania', 'romanian', 'romanians','publishing house', 'happening', 'increasingly', 'next',
    'publishing company', 'publisher house', 'publishing', 'house', 'houses', 'publisher', 'publishers', 'digital', 'digital space', 'online',
    'need', 'noticed', 'days', 'day', 'need', 'years', 'year', 'ago', 'think', 'way', 'time', 'make', 'space', 'five', 'country',
    'want', 'like', 'good', 'well', 'get', 'use', 'used', 'using', 'thing', 'things', 'lot', 'much', 'many', 'book',
    'really', 'something', 'someone', 'say', 'said', 'going', 'come', 'came', 'directly', 'file', 'create', 'general',
    'example', 'also', 'now', 'one', 'can', 'would', 'could', 'should', 'may', 'focused', 'unfortunately',
    'might', 'must', 'will', 'shall', 'title', 'see', 'look', 'take', 'find', 'idea', 'cases', 'present',
    'found', 'become', 'became', 'already', 'always', 'never', 'ever', 'every', 'major', 'post',
    'each', 'started', 'beginning', 'begin', 'began', 'clear', 'focus', 'side', 'specific', 'book', 'books',
    'area', 'year', 'know', 'first', 'certain', 'especially', 'measure', 'product',
    'hand', 'run', 'answer', 'field', 'available', 'believe', 'necessary', 'currently',
    'important', 'additionally', 'case', 'three', 'two', 'yes', 'no', 'without', 'with',
    'new', 'old', 'high', 'low', 'large', 'small', 'quite', 'rather', 'however',
    'everything', 'another', 'different', 'level', 'month', 'type', 'even', 'still',
    'worked', 'work', 'send', 'related', 'made', 'moment'
])

def preprocess_text(text):
    """Initial text preprocessing"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def handle_compound_terms(text):
    """Replace compound terms with single tokens"""
    processed_text = text.lower()
    for standard_term, variations in COMPOUND_TERMS.items():
        for variant in variations:
            pattern = r'\b' + re.escape(variant.lower()) + r'\b'
            processed_text = re.sub(pattern, standard_term, processed_text)
    return processed_text

def clean_text(text):
    """Clean and preprocess the text"""
    text = preprocess_text(text)
    text = handle_compound_terms(text)
    stop_words = set(stopwords.words('english')).union(CUSTOM_STOP_WORDS)
    words = text.split()
    words = [word for word in words if word not in stop_words and len(word) > 2 and not word.isnumeric()]
    return ' '.join(words)

def generate_word_cloud(text, question_title):
    """Generate and display word cloud"""
    cleaned_text = clean_text(text)
    # Create word frequency dictionary
    word_freq = {}
    words = cleaned_text.split()
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    # Sort and get top 15 words
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:15]
    # Create text for word cloud using only top 15 words
    top_words_text = ' '.join([word + ' ' * freq for word, freq in sorted_words])
    wordcloud = WordCloud(
        width=1200,
        height=800,
        background_color='white',
        max_words=15,
        min_font_size=10,
        max_font_size=100,
        collocations=False,
        colormap='plasma',  # Use a vibrant colormap
        min_word_length=3,
        normalize_plurals=True,
        prefer_horizontal=1.0,  # Slightly more horizontal words
        scale=2,
        margin=5,
        contour_width=2,  # Add a contour for better visibility
        contour_color='black',  # Contour color
    ).generate(top_words_text)
    plt.figure(figsize=(20, 10))
    plt.title(question_title, fontsize=24, fontweight='bold', color='darkblue')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures", f"wordcloud_{question_title.replace(' ', '_')}.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Figure saved to: {out}")
    print(f"\n{question_title} - Top 15 most frequent words:")
    for word, freq in sorted_words:
        print(f"{word}: {freq}")

def analyze_questions(doc_text):
    """Analyze each question and its answers"""
    questions = re.split(r'Question \d+:', doc_text)  # Split text by questions
    for i, question_block in enumerate(questions[1:], start=1):  # Skip the first split (before Question 1)
        question_title = f"Question {i}"
        print(f"\nAnalyzing {question_title}...")
        generate_word_cloud(question_block, question_title)

# Load text from the .docx file
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA = os.path.join(REPO_ROOT, "data", "Aggregated_EN.docx")
file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA

if not os.path.exists(file_path):
    sys.exit(
        f"\nData file not found at: {file_path}\n"
        "The aggregated interview data is confidential and not distributed "
        "with this repository.\nSee the README for how to request it, or pass "
        "a path: python scripts/wcloud_analysis_question.py path/to/file.docx\n"
    )

doc = Document(file_path)
doc_text = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])

# Perform analysis
analyze_questions(doc_text)