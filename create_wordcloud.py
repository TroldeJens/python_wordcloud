### Globals
# Input and output
input_filename                      = "input.txt"
result_filename                     = "resulting_wordcloud.png"

# Adjust text
lowercase_everything                = False         # Make all strings lowercase.
uppercase_everything                = False         # Make all strings uppercase.
start_all_words_with_capital_letter = True          # Start every word with a capital letter. Can be combined with lowercase_everything.

# Customize wordcloud
width                               = 1000
height                              = 500
make_background_transparent         = False         # If True, the background will be transparent. If no, use the colour defined below.
background_colour                   = "white"
use_custom_font                     = False         # If True, use the font defined below.
custom_font_path                    = "fonts/Roboto/Roboto-Italic.ttf"
use_custom_mask                     = True          # If True, use the image defined below as a mask. White is ignored. Everything else becomes the form.
custom_mask_path                    = "mask_images/arrow_left.png"

# Other
debug                               = False

import os
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import numpy as np
from PIL import Image

def capitalize_first_letter(word: str) -> str:
    """Capitalize only first letter of a string. Other letters remain unchanged."""
    return word[0].upper() + word[1:]

def capitalize_first_letter_of_every_word(text: str) -> str:
    """Split a string into separate words and capitalize each of them. Other letters remain unchanged."""
    words = []
    for word in text.split():
        words.append(capitalize_first_letter(word))
    return ' '.join(words)

def cleanup_and_adjust_mask_image(mask: Image.Image) -> Image.Image:
    """Cleanup the mask image. 
        1) Resize to fit target width and height
        2) Convert pixel values 
        3) Ensure that transparent pixels become white
    """
    # Resize the image to fit the target width and height.
    #   If we don't do this, then the target width and height will be ignored and the result will use the shape of the mask image instead. 
    mask    = mask.resize((width, height))
    # Ensure that white pixels have the value 0-255, and not 0-1.
    #   We use RGBA here, because if you use RGB, it makes all transparent background black, which is not what we want.
    mask    = mask.convert("RGBA")
    # Ensure that transparent background is coloured white.
    tmpMask = Image.new("RGBA", mask.size, "white") # Create a new image with a white rgba background.
    tmpMask.paste(mask, mask)                       # Paste the image onto the background.
    return tmpMask.convert("RGB")                   # Return a 24bit version of the tmpMask image.

def generate_wordcloud():
    """Generate wordcloud using the global variables defined in the beginning of the document."""

    # Get data directory (using getcwd() is needed to support running example in generated IPython notebook).
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Read file and add each line to a list.
    lines = []
    with open(path.join(d, input_filename)) as fileinput:
        lines = fileinput.read().splitlines()

    if lowercase_everything:
        lines = [line.lower() for line in lines]

    if uppercase_everything:
        lines = [line.upper() for line in lines]

    if start_all_words_with_capital_letter and not uppercase_everything:
        lines = [capitalize_first_letter_of_every_word(line) for line in lines]

    # Count each unique line
    word_count_dictionary = Counter(lines)

    # Debug
    if(debug):
        print("---DEBUG START---")
        print("Resulting lines:")
        print(lines)
        print("---------------")
        print("Count of unique lines:")
        print(word_count_dictionary)
        print("---DEBUG END---")

    # Setup WordCloud
    wordcloud = WordCloud()
    wordcloud.mode              = "RGBA"
    wordcloud.width             = width
    wordcloud.height            = height
    wordcloud.background_color  = None if make_background_transparent else background_colour
    if use_custom_font:
        wordcloud.font_path     = custom_font_path
    if use_custom_mask:
        mask                    = Image.open(custom_mask_path)
        mask                    = cleanup_and_adjust_mask_image(mask)
        wordcloud.mask          = np.array(mask)
        
    # Generate wordcount
    wordcloud.generate_from_frequencies(word_count_dictionary)

    plt.axis("off")
    plt.imsave(fname=result_filename, arr=np.array(wordcloud), format="png") # Use imsave in order to save image in the exact size as defined by width and height.

    return

# Run program
if __name__ == '__main__':
    generate_wordcloud()
    print("WordCloud image has been generated. Resulting image: ", result_filename)