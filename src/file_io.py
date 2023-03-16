import os
import tiktoken
import PyPDF2
import mimetypes

# handles functions dealing with files

def file_to_string(file_path):
    # convert file into string

    ftype = get_filetype(file_path)
    file = open(file_path, 'r')

    contents = ""

    if (ftype == ".pdf"): 
        # file is a pdf
        pdf_reader = PyPDF2.PdfFileReader(file_path)
        numpages_ = pdf_reader.getNumPages()
        for page in numpages_:
            page_obj = pdf_reader.getPage(page)
            page_text = page_obj.extract_text()
            contents += page_text

    else:
        # file is not a pdf

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
    # returns either the path to a focused target, or the location of the target folder

    focused_target = True if len(args.location) > 0 else False
    if(focused_target):
        # use args.file_location
        target_path = args.location
    else:
        # use target dir
        path = os.getcwd()
        target_folder_path = path + "/target_folder/"
        contents = os.listdir(target_folder_path)
        target_path = target_folder_path + contents[0]
    
    return target_path

def get_filename(path):
    return (os.path.splitext(path)[0].lower())

def get_target_text(dir_path):
    # gets all of the text in a directory, and every directory within it. Adds context to file as well.
    dir_name = get_filename(dir_path)

    if not os.path.isdir(dir_path):
        # if path is not a directory, get its string and return it
        file_summary = f"file {dir_name}:" + file_to_string(dir_path)
        return file_summary

    dir_summary = f"entering folder {dir_name} :"

    for filename in os.listdir(dir_path):
        cur_path = os.path.join(dir_path, filename)
        cur_name = get_filename(cur_path)

        if os.path.isdir(cur_path):
            # current path is a directory, recursively go into it            
            dir_summary += get_target_text(cur_path)

        else:
            # is a filename, so extract text contents ONLY if valid filetype
            context = f"file {cur_name}: "
            if valid_filetype(cur_path):
                # valid, so get its string content 
                file_content = file_to_string(cur_path)

            else:
                file_content = "unsupported file format"

            dir_summary += context + file_content
        
    dir_summary += f"leaving directory {dir_name}. "
    return dir_summary  

def valid_filetype(path):
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

    with open("supported_files.txt", 'r') as file:
        supported_list = file.readlines()
    ftype = get_filetype(path)
    if ftype in supported_list:
        return True
    else
        return False

def get_ftype_summary_dict(dir_path):
    # returns a dictionary of every filetype, and how many of that filetype are in a directory
    ftypes_dict = {}
    rec_diranalysis(dir_path, ftypes_dict)
    return ftypes_dict

def rec_diranalysis(path, dict):
    # returns a dictionary of every ftype in directory

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        filetype = get_filetype(file_path) 

        if os.path.isdir(filename):
            # found directory, so perform directory analysis
            dict_add(filetype, dict) # add filetype (directory)
            rec_diranalysis(filename, dict)
        
        else:
            # found file, so add format to keyval pairs
            if is_supported_file(file_path):
                dict_add(filetype, dict)
            elif is_textfile(filetype):
                dict_add("mimetext (minimally supported)", dict)

            else:
                # unsupported, so incriment unsupported and add specific unsupported filetype to list
                dict_add("UNSUPPORTED", dict)
                dict_add("XXXX " + filetype, dict)


def dict_add(key, dict):
    # either makes new key at zero, or adds 1 to key
    if key in dict:
        dict[key] += 1
    else:
        # add key
        dict[key] = 1