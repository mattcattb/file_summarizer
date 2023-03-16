import openai
import argparse
import os
import json

from src.summarizer_class import File_Summarizer
from src.file_io import file_to_string, get_target_path

'''
The following script summarizes a single file. Either specify the target with --location, or put the file into target_folder.
'''

def main():
    global args 
    args = arg_parse() #location and focus_question
    prepare_json(args)

    #setsup filesummarizer class
    open_api = File_Summarizer()

    # setup openai key
    try :
        api_key = os.environ["OPENAI_API_KEY"]
    except:
        api_key = open_api.key
    openai.api_key = api_key
    
    target_path = get_target_path(args)

    print("target path: " + target_path)

    # get question and file contents from file_path
    full_file_contents = file_to_string(target_path)

    # get string of every api response without performing heirarchy of summarizations
    (shallow_summaries_string, shallow_summaries_list) = open_api.summarize_string(full_file_contents)
    
    print_summaries(shallow_summaries_string, shallow_summaries_list, open_api)



def print_summaries(summary_string, summary_list, open_api):
    # prints out full response to terminal

    #! impliment newlines to make response more readable!
    print(f"GPTs full response to {open_api.question}:")
    print(summary_string)

    print(f"GPT has {len(summary_list)} responses. Each one is broken down below:")

    for i in range(len(summary_list)):
        
        print(f"\nresponse {i}:")
        print(summary_list[i])

def arg_parse():
    # arguements for python script
    parser = argparse.ArgumentParser(description="GTP3 File Summarizer")
    parser.add_argument("--location", type=str, dest="location", help="Location of file that wants to be analyzed", default="")
    parser.add_argument("--question_type", type=int, dest="question_type", help="Which question to ask. See README and questions.txt", default=0)
    # parser.add_argument("--model_name", type=str, dest="model_name", help="engine used to make requests from", default="gpt-3.5-turbo-0301")
    parser.add_argument("--response_size", type=int, dest="response_size", help="maximum number of works in final response. 50 to max tokensize", default=0)
    parser.add_argument("--temp", type=int, dest="temp", help="randomness of models response. From 0 to 1", default=0.5)
    parser.add_argument("--overlap", type=int, dest="overlap", help="overlap is the amount of text repeated in a summarization of content, to make sure context isn't lost.", default=150)
    return parser.parse_args()

def prepare_json(args):
    # changes a json file using commandline arguements that have been parsed 

    json_filename = "api_params.json"

    cur_dir = os.getcwd()
    json_path = cur_dir + "/src/" + json_filename

    with open(json_path, 'r') as f:
        params = json.load(f)

    params["temperature"] = args.temp
    params["location"] = args.location

    pass

def file_path_from_dir():
    # returns path of first file in file_input
    
    dir_name = "target_folder"
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    finput_dir_path = os.path.join(parent_dir + dir_name)
    filename_list = os.listdir(finput_dir_path)
    file_path = os.path.join(finput_dir_path, filename_list[0])
    return file_path

main()