import json
import re
import difflib

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==============================
# DOWNLOAD NLTK RESOURCES
# ==============================

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("punkt_tab")


# ==============================
# LOAD FAQ DATA
# ==============================

with open("faqs.json", "r", encoding="utf-8") as file:
    faqs = json.load(file)


# ==============================
# NLP TOOLS
# ==============================

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


# ==============================
# TEXT PREPROCESSING
# ==============================

def preprocess_text(text):

    text = text.lower()

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Tokenize
    words = nltk.word_tokenize(text)

    # Remove stopwords and lemmatize
    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)


# ==============================
# PREPARE FAQ QUESTIONS
# ==============================

all_questions = []
question_to_faq = []

for faq_index, faq in enumerate(faqs):

    for question in faq["questions"]:

        processed = preprocess_text(question)

        all_questions.append(processed)
        question_to_faq.append(faq_index)


# ==============================
# BUILD VOCABULARY
# ==============================

vocabulary = set()

for question in all_questions:

    for word in question.split():

        vocabulary.add(word)


# ==============================
# TYPO CORRECTION
# ==============================

def correct_typos(text):

    words = text.split()
    corrected_words = []

    for word in words:

        # Keep very short words as they are
        if len(word) <= 2:
            corrected_words.append(word)
            continue

        # If word already exists, don't change it
        if word in vocabulary:

            corrected_words.append(word)
            continue

        # Find closest matching known word
        matches = difflib.get_close_matches(
            word,
            vocabulary,
            n=1,
            cutoff=0.60
        )

        if matches:

            corrected_words.append(matches[0])

        else:

            corrected_words.append(word)

    return " ".join(corrected_words)


# ==============================
# WORD TF-IDF
# ==============================

word_vectorizer = TfidfVectorizer(
    ngram_range=(1, 2)
)

word_vectors = word_vectorizer.fit_transform(
    all_questions
)


# ==============================
# CHARACTER TF-IDF
# ==============================

char_vectorizer = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(3, 5)
)

char_vectors = char_vectorizer.fit_transform(
    all_questions
)


# ==============================
# GET RESPONSE
# ==============================

def get_response(user_question):

    # --------------------------
    # NORMAL PREPROCESSING
    # --------------------------

    processed_question = preprocess_text(user_question)

    # --------------------------
    # TYPO CORRECTION
    # --------------------------

    corrected_question = correct_typos(
        processed_question
    )


    # --------------------------
    # WORD SIMILARITY
    # --------------------------

    user_word_vector = word_vectorizer.transform(
        [corrected_question]
    )

    word_similarity = cosine_similarity(
        user_word_vector,
        word_vectors
    )[0]


    # --------------------------
    # CHARACTER SIMILARITY
    # --------------------------

    user_char_vector = char_vectorizer.transform(
        [corrected_question]
    )

    char_similarity = cosine_similarity(
        user_char_vector,
        char_vectors
    )[0]


    # --------------------------
    # FUZZY MATCHING
    # --------------------------

    fuzzy_scores = []

    for question in all_questions:

        score = difflib.SequenceMatcher(
            None,
            corrected_question,
            question
        ).ratio()

        fuzzy_scores.append(score)


    # --------------------------
    # COMBINE SCORES
    # --------------------------

    combined_scores = []

    for i in range(len(all_questions)):

        score = (
            (word_similarity[i] * 0.45)
            +
            (char_similarity[i] * 0.35)
            +
            (fuzzy_scores[i] * 0.20)
        )

        combined_scores.append(score)


    # --------------------------
    # BEST MATCH
    # --------------------------

    best_question_index = max(
        range(len(combined_scores)),
        key=lambda i: combined_scores[i]
    )

    best_score = combined_scores[
        best_question_index
    ]

    best_faq_index = question_to_faq[
        best_question_index
    ]


    # ==========================
    # FALLBACK FOR VERY SHORT /
    # UNCLEAR QUESTIONS
    # ==========================

    if best_score < 0.20:

        return {
            "answer": (
                "I'm not sure about that yet. "
                "I can currently help with questions about "
                "orders, delivery, payments, returns, refunds "
                "and your account."
            ),
            "confidence": round(
                float(best_score),
                2
            )
        }


    # ==========================
    # RETURN ANSWER
    # ==========================

    return {
        "answer": faqs[best_faq_index]["answer"],
        "confidence": round(
            float(best_score),
            2
        )
    }