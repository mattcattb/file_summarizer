from src.file_io import is_supported_file, dict_add, is_textfile, num_file_tokens, string_info
from src.file_io import file_to_string, num_tokens_in_string, get_filename, isreadable_filetype, get_filetype
import os

'''
Class for directory summarization tools

path to string
path length
path tokens
path extentions summary

'''

class Path_Tools:

    @staticmethod
    def print_testing_summary(path):
        # prints out all extentions and their count 

        summary_dict = Path_Tools.valid_filetype_summary_dict(path)

        pure_string = Path_Tools.path_to_string(path)
        context_string = Path_Tools.path_to_context_string(path)

        directories = summary_dict["directory"][0]
        valid_files = summary_dict["valid"][0]
        invalid_files = summary_dict["invalid"][0]
        total_files = invalid_files + valid_files
        total_contents = directories + valid_files + invalid_files

        print("### Quick File Overview ###")
        print(f"Total file objects : {total_contents}\nTotal Files: {total_files}\nTotal Directories: {directories}")
        print(f"Valid files: {valid_files}\nInvalid files: {invalid_files}")

        print("context string information:")
        Path_Tools.print_string_summary(context_string)

        print("pure string information:")
        Path_Tools.print_string_summary(pure_string)

        for key, value in summary_dict.items():
            print(f"{key}: {value[0]} instances, {value[1]} tokens")
        
    @staticmethod
    def print_summary(path):
        # prints out summary of filepath, returns dictionary of values
        dict_info = {} 
        summary_dict = Path_Tools.filetype_summary_dict(path)
        pure_string = Path_Tools.to_string(path)

        directories = summary_dict["directory"][0]
        valid_files = summary_dict["valid"][0]
        invalid_files = summary_dict["invalid"][0]
        total_files = invalid_files + valid_files
        total_contents = directories + valid_files + invalid_files

        print("### Quick File Overview ###")
        print(f"Total file objects : {total_contents}\nTotal Files: {total_files}\nTotal Directories: {directories}")
        print(f"Valid files: {valid_files}\nInvalid files: {invalid_files}")

        print("###### Total Path Summary ##########")
        print(f"Total file objects : {total_contents}\n Total Files: {total_files}\n Total Directories:")
        Path_Tools.print_string_summary(pure_string)
        
        print("Extention information: ")
        for key, value in summary_dict.items():
            print(f"{key}: {value[0]} instances, {value[1]} tokens")

    @staticmethod
    def print_string_summary(string):
        # prints summary of a string
        (nchar, nwords, ntokens) = string_info(string)
        print(f"characters:{nchar}, words:{nwords}, tokens:{ntokens}")
        print(f"that will take around {int(ntokens *(1/4000)) + 1} api calls")

    @staticmethod
    def num_words(path):
        # number of words in a directory
        path_string = Path_Tools.to_string(path)
        return len(path_string.split())

    @staticmethod
    def return_path_info(path):
        # returns numwords, numchar, numtokens of pathstring
        path_string = Path_Tools.to_string(path)
        return string_info(path_string)
    
    @staticmethod    
    def return_context_path_into(path):
        context_string = Path_Tools.path_to_context_string(path)
        return string_info(context_string)

    @staticmethod
    def path_to_string(path):
        # converts entire directory to a string
        full_string = ""

        if(not os.path.isdir(path)):
            # if tokens in folder was called on a file, return tokens in that folder
            full_string += file_to_string(path)
            return full_string

        for filename in os.listdir(path):
            path = os.path.join(path, filename)
            if(os.path.isdir(path)):
                full_string += Path_Tools.path_to_string(path)

            else:
                if isreadable_filetype(path):
                    # only add tokens if object is valid readable filetype
                    full_string += file_to_string(path)

        return full_string

    @staticmethod
    def path_to_context_string(path):
        # returns string of entire directory including context (filename, extention, directory)

        if not os.path.isdir(path):
            # if path is not a directory, get its string and return it
            context_string = Path_Tools.file_to_context_string(path)    
            return context_string

        dir_name = os.path.basename(path)
        dir_summary = f"entering dir \"{dir_name}\" :"

        for filename in os.listdir(path):
            cur_path = os.path.join(path, filename)

            if os.path.isdir(cur_path):
                # current path is a directory, recursively go into it            
                subdir_summary = Path_Tools.path_to_context_string(cur_path)
                dir_summary += subdir_summary
            else:
                # current path is a file, add its contents with context
                context_string = Path_Tools.file_to_context_string(cur_path)
                dir_summary += context_string
            
        dir_summary += f"leaving dir \"{dir_name}\" "
        
        return dir_summary  

    def file_to_context_string(path):
        # returns a string of the files contents and the files name
        # file <filename.type>: <files contents>
        # if file is unsupported, put <unsupported contents>
        contents = file_to_string(path)
        filename = os.path.basename(path)

        if path == None:
            context_string = f"file {filename}: UNSUPPORTED"
        else:
            context_string = f"file {filename}: {contents}"

        return context_string

    @staticmethod
    def num_tokens(path):
        # returns the number of tokens in a folder, to get an estimate of how many gpt calls will need to be made

        num_tokens = 0

        if(not os.path.isdir(path)):
            # if tokens in folder was called on a file, return tokens in that folder
            return num_file_tokens(path)

        for filename in os.listdir(path):
            path = os.path.join(path, filename)
            if(os.path.isdir(path)):
                subdir_tokens = Path_Tools.num_tokens(path)
                num_tokens += subdir_tokens
            else:
                if isreadable_filetype(path):
                    # only add tokens if object is valid readable filetype
                    num_tokens += num_file_tokens(path)

        return num_tokens
    
    @staticmethod
    def num_files(path):
        # returns the total number of files in a folder
        
        total_files = 0

        if(not os.path.isdir(path)):
            # if files in folder was called on a file
            return 0

        for filename in os.listdir(path):
            path = os.path.join(path, filename)
            if os.path.isdir(path):
                total_files += Path_Tools.num_files(path)
            else:
                # Do something with the file
                total_files += 1
            
        return total_files

    @staticmethod
    def valid_filetype_summary_dict(directory):
        # recursively returns dict of all filetypes in directory and subdirectories
        # track how many filetypes are readable vs not readable
        # filetype: [num files, tokens in file]

        dir_dict = {"readable": [0,0], "unreadable": [0,0], "directory": [0,0]}

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isdir(filepath):
                # file is a directory, so go through and get subdirectories dir_dict
                subdir_dict = Path_Tools.filetype_summary_dict(filepath)
                # merge dictionaries together
                for filetype, count in subdir_dict.items():
                    if filetype in dir_dict:
                        dir_dict[filetype] += count
                    else:
                        dir_dict[filetype] = count

                dir_dict = dict_add("directory", 1, dir_dict)

            else:
                # file is a file, so add its extention to dir_dict
                if isreadable_filetype(filepath):
                    # readable file, find if on supported files, or mime file
                    file_contents = file_to_string(filepath)
                    if is_supported_file(filepath):
                        extentionID = str(filetype)

                    elif is_textfile(filepath):
                        extentionID = "mime " + str(filetype),
                    
                    extentionID = ''.join(extentionID)
                    file_tokens = num_tokens_in_string(extentionID + file_contents)
                    dir_dict = dict_add("readable", file_tokens, dir_dict)

                else:
                    extentionID = "X" + filetype
                    file_tokens = num_tokens_in_string(extentionID)
                    dir_dict = dict_add("unreadable", file_tokens, dir_dict)
                

                dir_dict = dict_add(extentionID, file_tokens, dir_dict)

        return dir_dict
    
    @staticmethod
    def filetype_summary_dict(directory):
        # recursively returns dict of all filetypes in directory and subdirectories
        # filetype: [num files, tokens in file]

        dir_dict = {"readable": [0,0], "unreadable": [0,0], "directory": [0,0]}

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isdir(filepath):
                # file is a directory, so go through and get subdirectories dir_dict
                subdir_dict = Path_Tools.filetype_summary_dict(filepath)
                # merge dictionaries together
                for filetype, count in subdir_dict.items():
                    if filetype in dir_dict:
                        dir_dict[filetype] += count
                    else:
                        dir_dict[filetype] = count

                dir_dict = dict_add("directory", 1, dir_dict)

            else:
                # file is a file, so add its extention to dir_dict

                extention = get_filetype(filepath)

                num_file_tokens()

                dir_dict = dict_add(extention, file_tokens, dir_dict)

        return dir_dict