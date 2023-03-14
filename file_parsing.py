import os
import string


def file_to_text(file_path):
    # convert file to a text file, and then read it in (making sure not too many tokens)
    text = ""
    with open(file_path, 'r') as file:    
        text += file.read() + " "

    return text

def token_estimation(text):
    # estimates amount of tokens in text using a token average and periods

    # 4 characters per token on average?
    tokens_per_alphachar = 1/4
    num_punctuation = 0
    num_alpha = 0
    num_numbers = 0
    
    for char in text:
        if char in string.punctuation:
            # . < > ( ) etc
            num_punctuation += 1
        elif(char.isalpha()):
            # a b c d etc
            num_alpha += 1
        elif(char.isnumeric()):
            num_numbers += 1
        else:
            num_alpha += 1
        
    total_tokens = tokens_per_alphachar *  num_alpha + num_numbers + num_punctuation
    return total_tokens