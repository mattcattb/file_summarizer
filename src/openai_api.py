import openai
import tiktoken

# functions dealing with the preperation of data, and communication of data with openai's API
# no longer used!

def segment_string(string, config):
    # returns string of full question content prompts for api, all within token restrictions
    encoder = get_encoding(config.model_name)
    num_string_tokens = num_tokens(string, config.model_name)
    num_question_tokens = num_tokens(string,config.model_name)
    num_sys_description_tokens = num_tokens(config.system_description, config.model_name)

    string_tokens = encoder.encode(string)
    
    chunk_size = config.max_tokens - num_question_tokens - num_sys_description_tokens
    segmented_string = []
    
    for i in range(0, num_string_tokens, chunk_size - config.overlap):
        chunk = string_tokens[i: i + chunk_size]
        segmented_string.append(config.question + encoder.decode(chunk))
        
    return segmented_string

def send_prompts(prompt_list, config):
    # sends every list to api and returns a list of each response object

    response_list = []
    # go through every prompt in prompt list, and add response to response list
    for i in range(len(prompt_list)):
        cur_prompt = prompt_list[i]
        cur_response = get_response(cur_prompt, config)
        response_list.append(cur_response)

    return response_list

def response_list_to_string(response_list):
    # gets the text of every response, and compiles into full string
    response_string = ""
    for response in response_list:
        response_text = response["choices"][0]["text"].strip()
        response_string += response_text

    return response_string

def num_tokens(string, config):
    # returns number of tokens in a string for a model
    
    encoding = get_encoding(config.model_name)
    input_id = encoding.encode(string)
    num_tokens = len(input_id)
    return num_tokens

def get_response(prompt, config):
    # returns response object from GPT model using prompt and system desctiption
    # prompt should be both the file and the question

    message = [{"role": "system", "content": config.system_description}] 
    message.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model=config.model_name,
        messages=message,
        temperature=0.5
    )
    
    return response

def get_encoding(model_name):
    # returns encoding object based on model name

    try:
      encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
    return encoding

def send_message():
    pass