"""
Word Frequency Analyzer
------------------------
Reads a text file, cleans it, counts word frequencies, finds unique
vocabulary, then uses Pandas to sort/export the results and matplotlib
to plot the top words.

Usage:
    python word_freq_analyzer.py
"""

import os
import string
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
INPUT_FILE = "data/sample_book.txt"
OUTPUT_DIR = "output"
TOP_N = 20

# A small set of common words we don't care about (feel free to extend)
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
    "in", "on", "at", "to", "of", "for", "with", "as", "by", "it",
    "this", "that", "these", "those", "i", "you", "he", "she", "they",
    "we", "be", "been", "have", "has", "had", "not", "so", "if", "then",
    "will", "would", "can", "could", "his", "her", "its", "their", "them",
}


# ---------------------------------------------------------
# STEP 0: Write text INTO the file (new!)
# ---------------------------------------------------------
def write_text_to_file(filepath, text, mode="w"):
    """
    Write text into a file.
    mode="w"  -> WRITE mode: erases whatever was in the file first, then writes fresh text.
    mode="a"  -> APPEND mode: keeps what's already there and adds new text to the end.
    """
    # Make sure the folder the file lives in actually exists first
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filepath, mode, encoding="utf-8") as f:
        f.write(text)


# ---------------------------------------------------------
# STEP 1: Read and clean the text
# ---------------------------------------------------------
def read_and_clean(filepath):
    """Read a text file and return a list of lowercase, punctuation-free words."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Lowercase everything
    text = raw_text.lower()

    # Remove punctuation (translate each punctuation char to nothing)
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)

    # Split into a list of words on whitespace
    words = text.split()

    return words


# ---------------------------------------------------------
# STEP 2: Build the frequency dictionary (plain Python)
# ---------------------------------------------------------
def build_frequency_dict(words, exclude_stopwords=True):
    """Count occurrences of each word using a plain dict."""
    freq = {}
    for word in words:
        if exclude_stopwords and word in STOPWORDS:
            continue
        freq[word] = freq.get(word, 0) + 1
    return freq


# ---------------------------------------------------------
# STEP 3: Unique vocabulary using a set
# ---------------------------------------------------------
def vocabulary_stats(words):
    """Return total word count, unique word count, and lexical diversity."""
    total_words = len(words)
    unique_words = set(words)
    diversity = len(unique_words) / total_words if total_words else 0
    return {
        "total_words": total_words,
        "unique_words": len(unique_words),
        "lexical_diversity": round(diversity, 4),
    }


# ---------------------------------------------------------
# STEP 4: Hand off to Pandas — build a DataFrame, sort, get top N
# ---------------------------------------------------------
def to_sorted_dataframe(freq_dict):
    """Convert the frequency dict into a sorted Pandas DataFrame."""
    df = pd.DataFrame(freq_dict.items(), columns=["word", "count"])
    df = df.sort_values(by="count", ascending=False).reset_index(drop=True)
    return df


# ---------------------------------------------------------
# STEP 5: Export top N words to CSV
# ---------------------------------------------------------
def export_top_words(df, top_n, output_path):
    top_df = df.head(top_n)
    top_df.to_csv(output_path, index=False)
    return top_df


# ---------------------------------------------------------
# STEP 6: Plot the top N words as a horizontal bar chart
# ---------------------------------------------------------
def plot_top_words(top_df, output_path):
    plt.figure(figsize=(10, 8))
    plt.barh(top_df["word"], top_df["count"], color="steelblue")
    plt.xlabel("Frequency")
    plt.ylabel("Word")
    plt.title(f"Top {len(top_df)} Most Frequent Words")
    plt.gca().invert_yaxis()  # highest count at the top
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 0: write some text into the input file (only if you want to
    # generate/overwrite it from Python instead of pasting into Notepad).
    # Comment this block out once you have your own real text file ready.
    sample_text = (
        "The quick brown fox jumps over the lazy dog. The dog barks at the fox, "
        "but the fox runs away quickly into the forest. In the forest, the fox "
        "meets a wise old owl sitting on a tree branch."
    )
    write_text_to_file(INPUT_FILE, sample_text, mode="w")

    # Step 1: read + clean
    words = read_and_clean(INPUT_FILE)

    # Step 2: frequency dict (plain Python)
    freq_dict = build_frequency_dict(words, exclude_stopwords=True)

    # Step 3: vocabulary stats (sets)
    stats = vocabulary_stats(words)
    print("Vocabulary stats:")
    print(f"  Total words:        {stats['total_words']}")
    print(f"  Unique words:       {stats['unique_words']}")
    print(f"  Lexical diversity:  {stats['lexical_diversity']}")

    # Step 4: Pandas DataFrame, sorted
    df = to_sorted_dataframe(freq_dict)

    # Step 5: export top N to CSV
    csv_path = os.path.join(OUTPUT_DIR, "top_words.csv")
    top_df = export_top_words(df, TOP_N, csv_path)
    print(f"\nTop {TOP_N} words:")
    print(top_df.to_string(index=False))
    print(f"\nSaved CSV to: {csv_path}")

    # Step 6: plot
    plot_path = os.path.join(OUTPUT_DIR, "frequency_plot.png")
    plot_top_words(top_df, plot_path)
    print(f"Saved plot to: {plot_path}")


if __name__ == "__main__":
    main()