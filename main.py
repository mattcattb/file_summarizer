import openai
import os
import argparse

from file_parsing import user_file_to_string

args = None
model_name = "gpt-3.5-turbo-0301"
max_tokens = None

def main():
    global args 
    args = arg_parse() #file_location and focus_question
    
    # setup openai key
    api_key = os.environ["OPENAI_API_KEY"]
    openai.api_key = api_key

    # get string of full user file
    full_file_contents = user_file_to_string(args.file_location)
    # segment file into strings that fit the token max for the model being used
    segmented_contents = tokenize_file(full_file_contents)

    full_response = send_all_contents(segmented_contents)
    print_response(full_response)

def tokenize_file(string):
    # break string into a list where each section is a prompt within token space
    string_chunks = []

def print_response(full_response):
    # prints out full response to terminal
    #! impliment newlines to make response more readable!
    print(f"GPTs response to {args.focus_question}:")
    print(full_response)

def arg_parse():
    # arguements for python script
    parser = argparse.ArgumentParser(description="GTP3 File Summarizer")
    parser.add_argument("--file_location", type=str, dest="file_location", help="Location of file that wants to be analyzed", default="")
    parser.add_argument("--focus_question", type=str, dest="focus_question", help="Specific question to ask before giving text promp", default="Give a summary of the files contents.")
    # parser.add_argument("--model_type", type=str, dest="model_type", help="engine used to make requests from", default="gpt-3.5-turbo-0301")
    # parser.add_argument("--temp", type=int, dest="temp", help="randomness of models response", default=0.5)
    return parser.parse_args()

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

def get_response(prompt):
    # returns response object from GPT model using prompt and focus_question from args in parameter
    # messages follow the following syntag: {"role": role, "content": content}
    # role is system, user, assistant
    
    response = openai.ChatCompletion.create(
    model=args.model_type,
    messages=[
            {"role": "system", "content": "You are a helpful file summarization bot."},
            {"role": "user", "content": f"{args.focus_question}: {prompt}"},
        ]
    )
        
    return response


main()