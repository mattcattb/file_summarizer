import openai
import os
from file_parsing import file_to_text

api_key = os.environ["OPENAI_API_KEY"]
max_tokens = 1024
temp = 0.5

def main():
    # input file into file folder. Can be any type
    
    
    openai.api_key = api_key
    file_contents = contents_from_filedir()
    prompt = file_contents

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens = max_tokens,
        n=1,
        stop=None,
        temperature = temp,
    )

    message = response.choices[0].text
    response_file = open('response.txt', 'w')
    response_file.write(message)

def contents_from_filedir():
    # use OS 

    workingdir = os.getcwd()
    dir_name = "file_input"

    dir_path  = os.path.join(workingdir, dir_name)
    filename_list = os.listdir(dir_path)
    
    file_path = os.path.join(dir_path, filename_list[0])

    return file_to_text(file_path)


main()