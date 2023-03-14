import openai
import os
import argparse

from file_parsing import file_to_text

args = None

def main():
    global args 
    args = arg_parse()
    setup_openai_key()

    full_file_contents = get_file_string(args)

    full_response = send_all_contents(full_file_contents)

    print_response(full_response)

def print_response(full_response):
    # prints out full response to terminal
    #! impliment newlines to make response more readable!
    print(f"GPTs response to {args.focus_question}:")
    print(full_response)

def get_file_string():
    # return files contents as string
    global args
    
    if(len(args.file_location) == 0):
        #user did not specify a filelocation, so must be using file_input directory 
        file_path = file_path_from_dir()
    else: 
        file_path = args.file_location

    return file_to_text(file_path)

def arg_parse():
    # arguements for python script
    parser = argparse.ArgumentParser(description="GTP3 File Summarizer")
    parser.add_argument("--file_location", type=str, dest="file_location", help="Location of file that wants to be analyzed", default="")
    parser.add_argument("--focus_question", type=str, dest="focus_question", help="Specific question to ask before giving text promp", default="Give a summary of the files contents.")
    parser.add_argument("--model_type", type=str, dest="model_type", help="engine used to make requests from", default="gpt-3.5-turbo-0301")
    parser.add_argument("--temp", type=int, dest="temp", help="randomness of models response", default=0.5)
    parser.add_argument("--max_tokens", type=int, dest="max_tokens", help="max tokens sent in a prompt", default=4096)
    return parser.parse_args()

def file_path_from_dir():
    # returns path of file in file_input
    workingdir = os.getcwd()
    dir_name = "file_input"

    dir_path  = os.path.join(workingdir, dir_name)
    filename_list = os.listdir(dir_path)
    file_path = os.path.join(dir_path, filename_list[0])
    return file_path

def setup_openai_key():
    # setsup openai key
    api_key = os.environ["OPENAI_API_KEY"]
    openai.api_key = api_key

def send_all_contents(file_text):
    # returns full response for entire file 

    full_prompt = file_text
    text_sent = False

    full_text_response = ""

    while(text_sent == False):
        # keep sending responses until len(reponse) is less then or equal to the length of the prompt
        full_prompt = prepare_prompt(full_prompt) # add focusquestion
        response = get_response(full_prompt)
        full_text_response += f"{response.choices[0].text} " # add response text to all contents
        response_len = len(response_text)
        prompt_len = len(full_prompt)
        if(prompt_len <= response_len):
            pass



def prepare_prompt(prompt):
    # adds focus question to prompt 
    return f"{args.focus_question} {prompt}"

def get_response(prompt):
    # returns response object from GPT model. Uses specifics from args in parameter
    # messages follow the following syntag: {"role": role, "content": content}
    # role is system, user, assistant
    openai.ChatCompletion.create(
    model=args.model_type,
    messages=[
            {"role": "system", "content": "You are a helpful file summarization bot."},
            {"role": "user", "content": f"{args.focus_question}: {prompt}"},
        ]
    )
        

    return response


main()