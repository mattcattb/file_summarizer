import openai
import argparse
import os
import json

from src.summarizer_class import File_Summarizer
from src.file_io import tokens_in_folder, files_in_folder, get_target_path
'''
This script will summarize an entire directory specified with --location, or all the contents of target_folder.
'''

def main():
    global args 
    args = arg_parse() #file_location and focus_question
    prepare_json(args)
    open_api = File_Summarizer()

    # setup openai key
    try :
        api_key = os.environ["OPENAI_API_KEY"]
    except:
        api_key = open_api.key
    openai.api_key = api_key

    target_path = get_target_path(args)
    
    print(target_path)
    target_tokens = tokens_in_folder(target_path)
    target_files = files_in_folder(target_path)

    print(f"{target_files} files, {target_tokens} tokens")
    print(f"it will take around {target_tokens *(1/3700)} calls")

    overall_summary = summarize_directory(target_path) # summarize every file in summarize directory


def summarize_directory(directory_path):
    for filename in os.listdir(directory_path):
        path = os.path.join(directory_path, filename)
        if os.path.isdir(path):
            summarize_directory(path)
        else:
            # summarize file

            pass

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
    parser.add_argument("--file_location", type=str, dest="file_location", help="Location of directory that wants to be analyzed", default="")
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
    params["file_location"] = args.file_location

    pass

main()