"""
quiz_generator.py
Local, free MCQ quiz generation using spaCy (no API key required).
Approach: extract key entities/noun phrases from the transcript, then build
fill-in-the-blank multiple choice questions using those terms as answers
and other similar terms as distractors.
"""

import random
import spacy
import streamlit as st


@st.cache_resource(show_spinner=False)
def load_nlp():
    """
    Loads the spaCy English model once and caches it.
    Run this once in your terminal first:
        python -m spacy download en_core_web_sm
    """
    return spacy.load("en_core_web_sm")


def extract_candidates(doc):
    """
    Pulls out named entities and important noun chunks as quiz-worthy terms,
    grouped by a rough 'category' so distractors make sense
    (e.g. don't mix a person's name with a number).
    """
    candidates = {}  # category -> set of terms

    for ent in doc.ents:
        label = ent.label_
        term = ent.text.strip()
        if len(term.split()) <= 4 and len(term) > 2:
            candidates.setdefault(label, set()).add(term)

    # Fallback: noun chunks if not enough named entities were found
    if sum(len(v) for v in candidates.values()) < 4:
        for chunk in doc.noun_chunks:
            term = chunk.text.strip()
            if 2 < len(term) <= 30 and len(term.split()) <= 4:
                candidates.setdefault("NOUN_CHUNK", set()).add(term)

    return candidates


def build_questions(text, num_questions=5):
    """
    Generates fill-in-the-blank MCQs from the transcript text.
    Returns a list of dicts: {question, options, answer}
    """
    nlp = load_nlp()
    doc = nlp(text)

    candidates = extract_candidates(doc)

    # Flatten all terms with their categories for distractor lookup
    all_terms_by_category = {k: list(v) for k, v in candidates.items()}

    questions = []
    used_terms = set()

    sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.split()) > 4]
    random.shuffle(sentences)

    for sent in sentences:
        if len(questions) >= num_questions:
            break

        sent_doc = nlp(sent)
        sent_candidates = extract_candidates(sent_doc)

        # find a term in this sentence we haven't used yet
        chosen_term = None
        chosen_category = None
        for category, terms in sent_candidates.items():
            for term in terms:
                if term not in used_terms and term in sent:
                    chosen_term = term
                    chosen_category = category
                    break
            if chosen_term:
                break

        if not chosen_term:
            continue

        # Build distractors from the same category elsewhere in the transcript
        same_category_pool = [
            t for t in all_terms_by_category.get(chosen_category, [])
            if t != chosen_term
        ]
        random.shuffle(same_category_pool)
        distractors = same_category_pool[:3]

        # Pad distractors if we don't have enough of the same category
        if len(distractors) < 3:
            other_pool = [
                t for cat, terms in all_terms_by_category.items()
                for t in terms if t != chosen_term and t not in distractors
            ]
            random.shuffle(other_pool)
            distractors += other_pool[: (3 - len(distractors))]

        if len(distractors) < 2:
            continue  # not enough content to make a fair MCQ, skip

        options = distractors + [chosen_term]
        random.shuffle(options)

        blanked_sentence = sent.replace(chosen_term, "______")

        questions.append({
            "question": f"Fill in the blank: {blanked_sentence}",
            "options": options,
            "answer": chosen_term
        })

        used_terms.add(chosen_term)

    return questions