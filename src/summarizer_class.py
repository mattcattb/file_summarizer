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
        
    def __make_json_obj(self):
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
        string_tokens = encoder.encode(string)
        
        chunk_size = self.token_thresh
        segmented_string = []
        
        for i in range(0, num_string_tokens, chunk_size):
            chunk = string_tokens[i: i + chunk_size]
            segmented_string.append(encoder.decode(chunk))
            
        return segmented_string
    
    def num_tokens(self, string):
        # returns number of tokens in a string for a model
        encoding = self.get_encoding()
        input_id = encoding.encode(string)
        num_tokens = len(input_id)
        
        return num_tokens
    
    def get_response(self, content, question):
        # returns response object from GPT model using prompt and system desctiption
        # prompt should be both the file and the question
        print(f"Making a response call with {self.num_tokens(question + content + self.system_description)} tokens!")
        message = [{"role": "system", "content": self.system_description}] 
        message.append({"role": "user", "content": question + content})
        print(f"sending message of length: {len(message)}")
        
        response = openai.ChatCompletion.create(
            model= self.model_name,
            messages=message,
            temperature=0.5
        )

        print("finished sending.")
        return response

    def get_encoding(self):
        # returns encoding object based on model name

        try:
            encoding = tiktoken.encoding_for_model(self.model_name)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        return encoding

    def response_to_string(self, response):
        return response["choices"][0]["message"]['content'].strip()

    def shallow_file_summary(self, file_string):
        # breaks string down into promps, and then returns each prompts summary from initial file string 

        prompts = self.segment_string(file_string)
        response_list = []
        # go through every prompt in prompt list, and add response to response list
        for i in range(len(prompts)):
            cur_prompt = prompts[i]
            cur_response = self.get_response(cur_prompt, self.question)
            response_list.append(cur_response)

        # convert response object list to text list
        text_list = []
        for response in response_list:
            response_text = self.response_to_string(response)
            text_list.append(response_text) 

        full_summary = ' '.join(text_list)

        return full_summary, text_list

    def deep_file_summary(self, file_contents):
        # continues to break down and make summaries until file is completely summarized

        history = {}
        i = 0
        (summary_string, summary_list) = self.shallow_file_summary(file_contents)
        history[str(i)] = summary_list
        print(f"i: {i}, summary_list is len {len(summary_list)}")
        i += 1

        while(len(summary_list) > 1):
            
            # while there are multiple summaries being returned, summarize all summaries
            (summary_string, summary_list) = self.shallow_file_summary(summary_string)
            history[str(i)] = summary_list
            print(f"i: {i}, summary_list is len {len(summary_list)}")
            i += 1

        return summary_string, history
    

    def print_summaries(self, summary_string, summary_list):
        # prints out full response to terminal
        #! impliment newlines to make response more readable!

        outfile = open("summary.txt", 'w')

        text_summary = f"GPTs full response to {self.question}: \n {summary_string}"
        print(text_summary)
        outfile.write(text_summary)
        list_summary = f"GPT has {len(summary_list)} responses. Each one is broken down below:"
        print(list_summary)
        outfile.write(list_summary)

        for i in range(len(summary_list)):
            text = f"\nresponse {i}:\n{summary_list[i]}"
            outfile.write(text)
            print(text)

        outfile.close


