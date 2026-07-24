"""
summarizer.py
Local, free summarization using Hugging Face transformers (no API key required).
Model runs entirely on your machine after the first download.
"""

from transformers import pipeline
import streamlit as st


@st.cache_resource(show_spinner=False)
def load_summarizer():
    """
    Loads the summarization model once and caches it across reruns.
    distilbart-cnn is smaller/faster than bart-large-cnn, good for CPU/laptops.
    """
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6"
    )


def chunk_text(text, max_words=450):
    """
    Splits long transcripts into chunks the model can handle.
    BART-family models have a ~1024 token limit, so we chunk by words
    to stay safely within that limit.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)
    return chunks


def summarize_text(text, min_length=30, max_length=130):
    """
    Summarizes a (potentially long) transcript using a map-reduce approach:
    1. Split transcript into chunks
    2. Summarize each chunk
    3. Combine chunk summaries and summarize again for a final cohesive summary
    """
    if not text or not text.strip():
        return ""

    summarizer = load_summarizer()
    chunks = chunk_text(text)

    chunk_summaries = []
    for chunk in chunks:
        word_count = len(chunk.split())
        this_max = min(max_length, max(20, word_count // 2))
        this_min = min(min_length, this_max - 5) if this_max > 5 else 5

        result = summarizer(
            chunk,
            max_length=this_max,
            min_length=this_min,
            do_sample=False
        )
        chunk_summaries.append(result[0]["summary_text"])

    combined = " ".join(chunk_summaries)

    if len(chunks) > 1:
        final_word_count = len(combined.split())
        this_max = min(max_length, max(30, final_word_count // 2))
        this_min = min(min_length, this_max - 5) if this_max > 5 else 5

        final_result = summarizer(
            combined,
            max_length=this_max,
            min_length=this_min,
            do_sample=False
        )
        return final_result[0]["summary_text"]

    return combined