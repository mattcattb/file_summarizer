import os

# handles functions dealing with file

def user_file_to_string(file_path):
    # return files contents as single string (no newlines) from file_path
    
    file_text = ""
    if(len(file_path) == 0):
        # user did not specify a filelocation, so must be using file_input directory 
        file_path = file_path_from_dir()

    file = open(file_path, 'r')
    file_text += file.read()
    return file_text

def file_path_from_dir():
    # returns path of first file in file_input
    
    dir_name = "file_input"
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    finput_dir_path = os.path.join(parent_dir + dir_name)
    filename_list = os.listdir(finput_dir_path)
    file_path = os.path.join(finput_dir_path, filename_list[0])
    return file_path

def get_question_string():
    # returns the string from the question.txt file

    contents = ""
    file = open("question.txt", 'r')
    contents += file.read()
    return contents 