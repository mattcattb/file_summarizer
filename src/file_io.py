import os
import tiktoken

# handles functions dealing with files

def file_to_string(file_path):
    # convert file into string
    contents = ""
    with open(file_path, 'r') as file:
        for chunk in iter(lambda: file.read(4096), ''):
            contents += chunk

    file.close()
    return contents 

def get_question_string():
    # returns the string from the question.txt file

    contents = ""
    file = open("question.txt", 'r')
    contents += file.read()
    return contents 


def num_words_in_file(file): 
    # returns number of words in file 
    with open(file, 'r') as f:
        contents = f.read()
        word_count = len(contents.split())
    return word_count

def num_tokens_in_file(file):
    # returns tokens in a file

    file_string = file_to_string(file)
    tokens = num_tokens_in_string(file_string)
    return tokens

def num_tokens_in_string(string):
    # returns number of tokens in a string

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")
    input_id = encoding.encode(string)
    num_tokens = len(input_id)
    return num_tokens

def files_in_folder(dir_path):
    # returns the total number of files in a folder
    total_files = 0

    if(not os.path.isdir(dir_path)):
        # if files in folder was called on a file
        return 0

    for filename in os.listdir(dir_path):
        path = os.path.join(dir_path, filename)
        if os.path.isdir(path):
            total_files += files_in_folder(path)
        else:
            # Do something with the file
            total_files += 1
        
    return total_files

def tokens_in_folder(dir_path):
    # returns the number of tokens in a folder, to get an estimate of how many gpt calls will need to be made
    num_tokens = 0

    if(not os.path.isdir(dir_path)):
        # if tokens in folder was called on a file, return tokens in that folder
        return num_tokens_in_file(dir_path)

    for filename in os.listdir(dir_path):
        path = os.path.join(dir_path, filename)
        if(os.path.isdir(path)):
            num_tokens += tokens_in_folder(path)
        else:
            num_tokens += num_tokens_in_file(path)

    return num_tokens

def get_target_path(args):

    focused_target = True if len(args.location) > 0 else False
    # returns either the path to a focused target, or the location of the target folder
    if(focused_target):
        # use args.file_location
        target_path = args.location
    else:
        # use target dir
        path = os.getcwd()
        target_folder_path = path + "/target_folder"
        contents = os.listdir(target_folder_path)
        target_path = contents[0]
    
    return target_path