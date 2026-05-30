# Qualitative Analysis Scripts — Romanian Publishing Sector

Python scripts for the computational analysis in the qualitative chapter of the doctoral thesis *Integrating Digital Business Models: A Study of the Romanian Publishing Sector* (SNSPA).

The analysis supports a qualitative study of ten semi-structured interviews with Romanian publishing professionals (January–February 2025). Two techniques are applied: sentiment analysis (polarity and subjectivity) and word-frequency visualization (word clouds), computed both for the full aggregated corpus and per interview question.

## What each script does

- `scripts/sentiment_analysis.py` — Computes TextBlob polarity (−1 to 1) and subjectivity (0 to 1) for the whole document and for each of the 15 questions. Prints results to the console.
- `scripts/wcloud_analysis_full.py` — Generates one word cloud from the full corpus, based on the 50 most frequent terms after compound-term grouping and stopword removal. Prints the top-50 frequency list and saves the figure.
- `scripts/wcloud_analysis_question.py` — Generates a separate word cloud per question, based on the top 15 terms each. Prints frequency lists and saves the figures.

The two word-cloud scripts use deliberately different compound-term dictionaries and stopword lists, matching the macro (full-document) and micro (per-question) scope of each analysis. This is intentional and described in the thesis methodology.

## Data availability

The interview data (`data/Aggregated_EN.docx`) is **not** included in this repository.

The interviews were conducted under a confidentiality agreement guaranteeing participant anonymity. The aggregated transcripts contain organizational detail that could identify participants, so they are not publicly distributed.

Researchers who wish to verify the analysis may request the data directly from the author. Requests are evaluated case by case and access is granted at the author's discretion, consistent with the confidentiality terms given to participants.

When the data file is absent, the scripts exit with a message explaining how to supply it. They do not fail silently.

## Reproducing the analysis

The numbers reported in the thesis were reproduced with the exact package versions pinned in `requirements.txt`. TextBlob's polarity model can vary across versions, so use these pins to reproduce the reported values.

```bash
# 1. Clone
git clone https://github.com/anamariaosadci/phd-thesis-qualitative-analysis.git
cd phd-thesis-qualitative-analysis

# 2. Virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install pinned dependencies
pip install -r requirements.txt

# 4. One-time NLTK + TextBlob corpora download
python -m textblob.download_corpora
python -c "import nltk; nltk.download('stopwords')"

# 5. Place the data file (obtained via request) in:
#    data/Aggregated_EN.docx

# 6. Run
python scripts/sentiment_analysis.py
python scripts/wcloud_analysis_full.py
python scripts/wcloud_analysis_question.py
```

Word-cloud figures are written to `figures/`.

You can also point a script at a file elsewhere:

```bash
python scripts/sentiment_analysis.py /path/to/Aggregated_EN.docx
```

## Reported results (for verification)

Full corpus: polarity **0.12**, subjectivity **0.45**.
Questions with polarity below 0.1: **Q9** (0.087), **Q13** (0.083), **Q14** (0.059).

These values were verified against the pinned environment above.

## Note on language

The interviews were conducted in Romanian and translated to English before analysis. The sentiment scores are computed on the English translation, not the Romanian originals. This is noted as a limitation in the thesis.

## Citation

If you use or reference this code, please cite the thesis. Citation details will be added on completion.

## License

See `LICENSE`.
