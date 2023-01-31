# Globals
lowercase_everything                = False         # Make all strings lowercase.
uppercase_everything                = False         # Make all strings uppercase.
start_all_words_with_capital_letter = True          # Start every word with a capital letter. Can be combined with lowercase_everything
inputFilename                       = "input.txt"
debug                               = True

import os
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

def capitalize_first_letter(word: str) -> str:
    """ Capitalize only first letter of a string. Other letters remain unchanged."""
    return word[0].upper() + word[1:]

def capitalize_first_letter_of_every_word(text: str) -> str:
    """ Split a string into separate words and capitalize each of them. Other letters remain unchanged."""
    words = []
    for word in text.split():
        words.append(capitalize_first_letter(word))
    return ' '.join(words)

def generate_wordcloud():
    """ Generate wordcloud using the global variables defined in the beginning of the document."""

    # Get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Read file and add each line to a list
    lines = []
    with open(path.join(d, inputFilename)) as fileinput:
        lines = fileinput.read().splitlines()

    if lowercase_everything:
        lines = [line.lower() for line in lines]

    if uppercase_everything:
        lines = [line.upper() for line in lines]

    if start_all_words_with_capital_letter:
        lines = [capitalize_first_letter_of_every_word(line) for line in lines]

    # Count each unique line
    word_count_dictionary=Counter(lines)

    # Debug
    if(debug):
        print("---DEBUG START---")
        print("Resulting lines:")
        print(lines)
        print("---------------")
        print("Count of unique lines:")
        print(word_count_dictionary)
        print("---DEBUG END---")

    # generate wordcount
    wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(word_count_dictionary)

    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("resulting_wordcloud"+".png", bbox_inches='tight')
    plt.show()
    plt.close()

    return

# Run program
if __name__ == '__main__':
    generate_wordcloud()