import json
import tiktoken
import openai
import os

# this class handles gpt api calls and file summaries

class File_Summarizer:

    def __init__(self):
        self.json_fname = "api_params.json"
        self.use_json_configs()
        pass

    def use_json_configs(self):
        # uses api_params.json file to configure self
        json_obj = self.make_json_obj()

        self.question = json_obj['question']
        self.system_description = json_obj['system_description']
        self.temperature = float(json_obj['temperature']) 
        self.model_name = json_obj['model_name']
        self.max_tokens = int(json_obj['max_tokens'])
        self.token_overlap = int(json_obj["token_overlap"])
        self.api_key = json_obj["API_key"]
        self.token_thresh = self.max_tokens - self.token_overlap - self.num_tokens(self.question) - self.num_tokens(self.system_description)   
        
    def make_json_obj(self):
        # create json object from json filename

        current_dir = os.path.abspath(__file__)
        print(current_dir)
        with open("src/" + self.json_fname, 'r') as json_file:
            data = json_file.read()
        json_obj = json.loads(data)
        return json_obj
    
    def segment_string(self, string):
        # returns string of full question content prompts for api, all within token restrictions
        encoder = self.get_encoding()
        num_string_tokens = self.num_tokens(string)
        # num_question_tokens = self.num_tokens(string)
        # num_sys_description_tokens = self.num_tokens(self.system_description)

        string_tokens = encoder.encode(string)
        
        # chunk_size = self.max_tokens - num_question_tokens - num_sys_description_tokens self.token_overlap
        chunk_size = self.token_thresh
        segmented_string = []
        
        for i in range(0, num_string_tokens, chunk_size):
            chunk = string_tokens[i: i + chunk_size]
            segmented_string.append(self.question + encoder.decode(chunk))
            
        return segmented_string
    
    def send_prompts(self, prompt_list):
    # sends every list to api and returns a list of each response object

        response_list = []
        # go through every prompt in prompt list, and add response to response list
        for i in range(len(prompt_list)):
            cur_prompt = prompt_list[i]
            cur_response = self.get_response(cur_prompt)
            response_list.append(cur_response)

        return response_list
    
    def num_tokens(self, string):
        # returns number of tokens in a string for a model
    
        encoding = self.get_encoding()
        input_id = encoding.encode(string)
        num_tokens = len(input_id)
        return num_tokens
    
    def get_response(self, prompt):
        # returns response object from GPT model using prompt and system desctiption
        # prompt should be both the file and the question

        message = [{"role": "system", "content": self.system_description}] 
        message.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model= self.model_name,
            messages=message,
            temperature=0.5
        )
        
        return response

    def get_encoding(self):
        # returns encoding object based on model name

        try:
            encoding = tiktoken.encoding_for_model(self.model_name)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        return encoding
    
    def recursive_summary(self, string):
        # recursively break string into strings small enough to be sent through api

        encoder = self.get_encoding()
        str_tokens = encoder.encode(string)

        tokens_len = len(str_tokens)

        if(tokens_len < self.token_thresh):
            # string under token thresh, can be sent.

            response_obj = self.get_response(string)
            text = self.response_to_string(response_obj)
            return text

        mid = tokens_len//2

        left_tokens = str_tokens[:,mid]
        right_tokens = str_tokens[mid,:]
        left_response = self.recursive_summary(encoder.decode(left_tokens))
        right_response = self.recursive_summary(encoder.decode(right_tokens))

        return left_response + right_response

    def response_to_string(self, response):
        return response["choices"][0]["message"]['content'].strip()

    def summarize_string(self, string):
        # breaks string down into promps, and then returns each prompts summary 

        prompts = self.segment_string(string)
        response_list = self.send_prompts(prompts) # list of promp objects
        
        # convert response object list to text list
        text_list = []
        for response in response_list:
            response_text = self.response_to_string(response)
            text_list.append(response_text) 

        full_summary = ' '.join(text_list)

        return full_summary, text_list

 
    def summarize_file(self, file_contents):
        # continues to break down and make summaries until file is completely summarized

        num_summaries = 1
        (summary_string, summary_list) = self.summarize_string(file_contents)
        print(num_summaries)
        while(summary_list > 1):
            # while there are multiple summaries being returned, summarize all summaries
            (summary_string, summary_list) = self.summarize_string(summary_string)
            num_summaries += 1
            print(num_summaries)

        return summary_string
    
    def summarize_summaries(self, summary_string):
        # break down summaries until each can be sent to chatgpt to make a sumarry off of them.
        
        pass

