import os
import tiktoken
import PyPDF2
import mimetypes

# handles functions dealing with files and filesupport

def get_supported_list():
    # returns supported filetypes from supported_files.txt
    supported_list = []
    cwd = os.path.join(os.getcwd(), "src")
    supported_path = os.path.join(cwd, "supported_files.txt")
    with open(supported_path, 'r') as file:
        for line in file:
            line = line.strip()
            supported_list.append(line)

    return supported_list

def file_to_string(file_path):
    # convert file into string of text. If file is invalid, return NONE

    if isreadable_filetype(file_path):  
        # file is readable

        ftype = get_filetype(file_path)
        contents = ""

        if (ftype == ".pdf"): 
            # file is a pdf
            pdf_reader = PyPDF2.PdfFileReader(file_path)
            numpages_ = pdf_reader.getNumPages()
            for page in numpages_:
                page_obj = pdf_reader.getPage(page)
                page_text = page_obj.extract_text()
                contents += page_text

        elif os.path.exists(file_path):
            # file is not a pdf
            file = open(file_path, 'r')
            for chunk in iter(lambda: file.read(4096), ''):
                contents += chunk
            
            file.close()
    else:
        # if file is unreadable
        contents = None

    return contents 

def get_question_string():
    # returns the string from the question.txt file

    contents = ""
    file = open("question.txt", 'r')
    contents += file.read()
    return contents 

def get_filetype(file):
    # returns extention, or "directory" if directory.
    try:
        type = os.path.splitext(file)[1].lower()
    except:
        type = "directory"
    return type

def num_words_in_file(file): 
    # returns number of words in file 
    with open(file, 'r') as f:
        contents = f.read()
        word_count = len(contents.split())
    return word_count

def num_file_tokens(file):
    # returns tokens in a file, or 

    file_string = file_to_string(file)
    tokens = num_tokens_in_string(file_string)
    return tokens

def num_tokens_in_string(string):
    # returns number of tokens in a string
    if string is None:
        # handles if string is none
        return 0
    
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")
    input_id = encoding.encode(string)
    num_tokens = len(input_id)
    return num_tokens

def get_target_path(target_path):
    # returns either the path to a focused target, or if none specified the folder in target folder

    focused_target = True if len(target_path) > 0 else False
    if(focused_target):
        # use args.file_location
        target_path = target_path
    else:
        # use target dir
        path = os.getcwd()
        target_folder_path = path + "/target_folder/"
        contents = os.listdir(target_folder_path)
        target_path = target_folder_path + contents[0]
    
    return target_path

def get_filename(path):
    return (os.path.splitext(path)[0].lower())

def isreadable_filetype(path):
    # if supported_file format, or is a text mime file.
    if is_supported_file(path) or is_textfile(path):
        return True
    else:
        return False

def is_textfile(path):
    # if filetype has text mime extention
    mime_type, encoding = mimetypes.guess_type(path)

    if mime_type and mime_type.startswith("text"):
        return True
    else:
        return False

def is_supported_file(path):
    # if file extention is in supported_files.txt
    supp_list = get_supported_list()
    ftype = get_filetype(path)

    if ftype in supp_list:
        return True
    else:
        return False

def dict_add(key, file_tokens, dict):
    # either makes new key at zero, or adds 1 to key    
    if key in dict:
        dict[key][0] += 1
        dict[key][1] += file_tokens
    else:
        # add key
        dict[key] = [1,file_tokens]

    return dict

def string_info(string):

    numchar = len(string)
    numwords = len(string.split())
    numtokens = num_tokens_in_string(string)
    return (numchar, numwords, numtokens)