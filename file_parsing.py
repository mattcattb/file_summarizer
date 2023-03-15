import os
import string


def user_file_to_string(file_path):
    # return files contents as single string (no newlines) from file_path
    
    text_return = ""
    if(len(file_path) == 0):
        # user did not specify a filelocation, so must be using file_input directory 
        file_path = file_path_from_dir()

    
    file = open(file_path, 'r')
    text_return += file.read()

    return text_return

def file_path_from_dir():
    # returns path of file in file_input
    
    dir_name = "file_input"
    workingdir = os.getcwd()
    dir_path  = os.path.join(workingdir, dir_name)
    filename_list = os.listdir(dir_path)
    file_path = os.path.join(dir_path, filename_list[0])
    
    return file_path
