# File Summarizer

## Description

This python script summarizes the text contents of entire file, simplifying its complexities into a simple explanation using openais gpt3 apis. Instead of copy and pasting each file into the chatgpt webservice, the script breaks the file into strings that are within the models token limits. Each response is recorded and combined together, finally asking to be summarized again, until an overall single summary is created.  

### Motivation

When reading through code used in popular ML research papers, many times the level of code has gone far over my head. In my hopes of understanding, ive found it extremely helpful to use chatgpt to explain the generality of each program file, so that I can then go into greater depth or see how it ties into the overall repository. Initially, I would copy and paste each text file, but I was bogged down by chatgpts token limit, so I was only able to get summaries of fragmented code. 

This code seeks to quickly summarize entire files, rather then needing to copy and paste them into chatgpt. Futhermore, it seeks to bypass token restrictions by implimenting a heirarchy summary feature, until the overall contents are summarized. 

## Usage

### Dependencies
- created with Linux
- openai is used to make requests with the gpt-3.5-turbo model
- tiktoken counts the tokens in a string, allowing them to fit within the model promps limits 

### Install

First, prepare your key by going to https://platform.openai.com/account/api-keys and creating an API key. Store your API_key by going into api_params.json and adding it to the API_key 

Then, input the following bash to clone github, install dependencies, and setup API key.
- git clone https://github.com/mattcattb/GPT_file_summarizer.git
- cd GPT_file_summarizer
- pip install -r requirements.txt # install


## Running Script

There are 2 ways to get the summary of a file/directory. Either:
1. use the --location arguement to specify the path to the file or folder
2. place only 1 file/folder into the target_folder directory.

Then run
-python multi_target.py

## Commandline Arguements




### Future Updates

That you for using this! My major hope for the future is to either create a summary of an entire directory (every file and subdirectory within it), or perhaps a tree that explains every file in a directory.
I also hope to impliment support with filetypes that are not traditional text (such as pdf), or have settings for topic specific summaries (such as reserach paper summaries, book summaries, or website summaries)
