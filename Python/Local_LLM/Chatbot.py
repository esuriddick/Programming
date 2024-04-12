#*****************************************************************************#
# REQUIREMENTS (PYTHON 3.10.13)
#*****************************************************************************#
#!pip install farm-haystack[inference,faiss,preprocessing,file-conversion,pdf]==1.24.1
#!pip install ctransformers==0.2.27
#!pip install clean-text==0.6.0
#!pip install langchain==0.1.8
#!pip install flask-sqlalchemy==3.1.1
#!pip install --force-reinstall -v "SQLAlchemy>=1.4.2,<2"

#*****************************************************************************#
# MODULES
#*****************************************************************************#

# AI
#-----------------------------------------------------------------------------#
import torch
from huggingface_hub import hf_hub_download
from transformers import pipeline, AutoTokenizer, AutoConfig, AutoModelForSeq2SeqLM
from ctransformers import AutoModelForCausalLM
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import messages_from_dict, messages_to_dict

# Documents
#-----------------------------------------------------------------------------#
import nltk
from nltk.tokenize import sent_tokenize
from cleantext import clean

# Haystack
#-----------------------------------------------------------------------------#
from haystack.document_stores import FAISSDocumentStore
from haystack import Pipeline
from haystack.nodes import TextConverter, PDFToTextConverter, DocxToTextConverter, PreProcessor, EmbeddingRetriever

# GUI
#-----------------------------------------------------------------------------#
from tkinter import *
from tkinter import simpledialog
from tkinter import filedialog as fd

# System
#-----------------------------------------------------------------------------#
import os
import shutil
import json
from threading import Thread
import datetime
import winsound
import pickle

#*****************************************************************************#
# SETTINGS
#*****************************************************************************#

# Conversational Model
#-----------------------------------------------------------------------------#
max_tokens_value = 2048             # Inference stops if it reaches x tokens
temperature = 0.30                  # Randomness of the words (0.7-0.90 for creative tasks, and lower for factual)
repeat_penalty_value = 1.1          # Repeat penalty sampling parameter
max_memory = 5                      # Maximum number of interactions (pair of user and AI reactions) kept in memory
chat_history = ConversationBufferWindowMemory(return_messages = True
                                              ,k = max_memory)

# GUI
#-----------------------------------------------------------------------------#
User_agent = "You"
AI_agent = "AI"
System_agent = "System"
TextBox_Selected = 0                # Whether the user has already pressed the message box

# System
#-----------------------------------------------------------------------------#
device = torch.device('cpu')        # Use CPU instead of GPU
model_chat_path = "./Models/Chat"
model_grammar_path = "./Models/Grammar"
model_summarization_news_path = "./Models/Summarization/News_article"
model_summarization_news_tokenizer_path = os.path.join(model_summarization_news_path, "Tokenizer")
model_summarization_news_model_path = os.path.join(model_summarization_news_path, "Model")
model_summarization_book_path = "./Models/Summarization/Book"
model_summarization_book_tokenizer_path = os.path.join(model_summarization_book_path, "Tokenizer")
model_summarization_book_model_path = os.path.join(model_summarization_book_path, "Model")
model_summarization_report_path = "./Models/Summarization/Report"
model_summarization_report_tokenizer_path = os.path.join(model_summarization_report_path, "Tokenizer")
model_summarization_report_model_path = os.path.join(model_summarization_report_path, "Model")
model_QA_retriever_path = "./Models/QA/Retriever"
logs_relative_path = "./Logs"
embeddings_relative_path = "./CKB"
duration = 300                      # Milliseconds
freq = 500                          # Frequency (in Hz)

# Global variables
#-----------------------------------------------------------------------------#
summary_goal = 0                    # Summarization goal

#*****************************************************************************#
# MODELS STORAGE (OFFLINE)
#*****************************************************************************#

# Conversational Model
#-----------------------------------------------------------------------------#
model_chat_ckpt = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
model_chat_file = 'mistral-7b-instruct-v0.2.Q4_K_M.gguf'
model_chat_type = 'mistral'   #Taken from config.json of model
if os.path.exists(model_chat_path) == False:
    os.makedirs(model_chat_path)
    hf_hub_download(repo_id = model_chat_ckpt
                    ,filename = model_chat_file
                    ,local_dir = model_chat_path
                    ,local_dir_use_symlinks = False)

# Grammar Model
#-----------------------------------------------------------------------------#
model_ckpt = "grammarly/coedit-large"
if os.path.exists(model_grammar_path) == False:
    os.makedirs(model_grammar_path)
    files_list = ["tokenizer_config.json"
                  ,"spiece.model"
                  ,"tokenizer.json"
                  ,"special_tokens_map.json"
                  ,"config.json"
                  ,"pytorch_model.bin"
                  ,"generation_config.json"]
    for model_file in files_list:
        hf_hub_download(repo_id = model_ckpt
                        ,filename = model_file
                        ,local_dir = model_grammar_path
                        ,local_dir_use_symlinks = False)
    del model_file, files_list

# Summarization Models
#-----------------------------------------------------------------------------#
#Text formatter
try:
    nltk.download("punkt")
except:
    pass

# News article
model_ckpt = "facebook/bart-large-cnn"
if os.path.exists(model_summarization_news_tokenizer_path) == False:
    os.makedirs(model_summarization_news_tokenizer_path)
    files_list = ["config.json"
                  ,"merges.txt"
                  ,"tokenizer.json"
                  ,"vocab.json"]
    for model_file in files_list:
        hf_hub_download(repo_id = model_ckpt
                        ,filename = model_file
                        ,local_dir = model_summarization_news_tokenizer_path
                        ,local_dir_use_symlinks = False)
    del model_file, files_list

if os.path.exists(model_summarization_news_model_path) == False:
    os.makedirs(model_summarization_news_model_path)
    files_list = ["config.json"
                  ,"generation_config.json"
                  ,"pytorch_model.bin"]
    for model_file in files_list:
        hf_hub_download(repo_id = model_ckpt
                        ,filename = model_file
                        ,local_dir = model_summarization_news_model_path
                        ,local_dir_use_symlinks = False)
    del model_file, files_list

# Book
model_ckpt = "pszemraj/long-t5-tglobal-base-16384-book-summary"
if os.path.exists(model_summarization_book_tokenizer_path) == False:
    os.makedirs(model_summarization_book_tokenizer_path)
    files_list = ["special_tokens_map.json"
                  ,"tokenizer.json"
                  ,"tokenizer_config.json"
                  ,"spiece.model"]
    for model_file in files_list:
        hf_hub_download(repo_id = model_ckpt
                        ,filename = model_file
                        ,local_dir = model_summarization_book_tokenizer_path
                        ,local_dir_use_symlinks = False)
    del model_file, files_list

if os.path.exists(model_summarization_book_model_path) == False:
    os.makedirs(model_summarization_book_model_path)
    files_list = ["config.json"
                  ,"pytorch_model.bin"]
    for model_file in files_list:
        hf_hub_download(repo_id = model_ckpt
                        ,filename = model_file
                        ,local_dir = model_summarization_book_model_path
                        ,local_dir_use_symlinks = False)
    del model_file, files_list

# Report
model_ckpt = "esuriddick/led-base-16384-finetuned-govreport"
if os.path.exists(model_summarization_report_tokenizer_path) == False:
    os.makedirs(model_summarization_report_tokenizer_path)
    files_list = ["tokenizer_config.json"
                  ,"vocab.json"
                  ,"merges.txt"
                  ,"tokenizer.json"
                  ,"special_tokens_map.json"]
    for model_file in files_list:
        hf_hub_download(repo_id = model_ckpt
                        ,filename = model_file
                        ,local_dir = model_summarization_report_tokenizer_path
                        ,local_dir_use_symlinks = False)
    del model_file, files_list

if os.path.exists(model_summarization_report_model_path) == False:
    os.makedirs(model_summarization_report_model_path)
    files_list = ["config.json"
                  ,"model.safetensors"
                  ,"generation_config.json"]
    for model_file in files_list:
        hf_hub_download(repo_id = model_ckpt
                        ,filename = model_file
                        ,local_dir = model_summarization_report_model_path
                        ,local_dir_use_symlinks = False)
    del model_file, files_list

# QA
#-----------------------------------------------------------------------------#
model_QA_retriever_ckpt = "sentence-transformers/all-mpnet-base-v2"
if os.path.exists(model_QA_retriever_path) == False:
    os.makedirs(model_QA_retriever_path)
    files_list = ["pytorch_model.bin"
                  ,"config.json"
                  ,"special_tokens_map.json"
                  ,"tokenizer.json"
                  ,"tokenizer_config.json"
                  ,"vocab.txt"]
    for model_file in files_list:
        hf_hub_download(repo_id = model_QA_retriever_ckpt
                        ,filename = model_file
                        ,local_dir = model_QA_retriever_path
                        ,local_dir_use_symlinks = False)
    del model_file, files_list

#*****************************************************************************#
# FUNCTIONS
#*****************************************************************************#

# General
#-----------------------------------------------------------------------------#
#Define date and time
def current_time(time_unit):
    now = datetime.datetime.now()

    #Obtain main time units
    year = now.year
    if len(str(now.month)) < 2:
        month = "0" + str(now.month)
    else:
        month = str(now.month)
    if len(str(now.day)) < 2:
        day = "0" + str(now.day)
    else:
        day = str(now.day)
    if len(str(now.hour)) < 2:
        hour = "0" + str(now.hour)
    else:
        hour = str(now.hour)
    if len(str(now.minute)) < 2:
        minute = "0" + str(now.minute)
    else:
        minute = str(now.minute)

    #Retrieve value based on time_unit
    if time_unit == "year":
        return year
    elif time_unit == "month":
        return month
    elif time_unit == "day":
        return day
    elif time_unit == "hour":
        return hour
    elif time_unit == "minute" or time_unit == "minutes":
        return minute

# Key bindings / Options
#-----------------------------------------------------------------------------#
def DeleteHint():
    global TextBox_Selected
    if TextBox_Selected == 0:
        TextBox_Selected= 1
        messageWindow.delete("1.0", END)

def handle_enter(event):
    handle_send()
    return "break" #Prevents the addition of a new line

def handle_send():
    Thread(target = send, daemon = True).start()

def handle_enter_shift(event):
    #Need to define this event or SHIFT+Enter won't add new line, but execute Enter
    messageWindow.insert(INSERT, "")

def handle_summarize_news_article():
    global summary_goal
    summary_goal = 0
    Thread(target = summary_document, daemon = True).start()

def handle_summarize_book():
    global summary_goal
    summary_goal = 1
    Thread(target = summary_document, daemon = True).start()

def handle_summarize_report():
    global summary_goal
    summary_goal = 2
    Thread(target = summary_document, daemon = True).start()

def handle_create_CKB():
    Thread(target = create_CKB, daemon = True).start()

def handle_use_CKB():
    Thread(target = use_CKB, daemon = True).start()

def handle_grammar_correct():
    global TextBox_Selected
    if TextBox_Selected == 0:
        TextBox_Selected= 1
        messageWindow.delete("1.0", END)
    messageWindow.insert('1.0', "[Grammar (Correct)] ")

def handle_grammar_enhance():
    global TextBox_Selected
    if TextBox_Selected == 0:
        TextBox_Selected= 1
        messageWindow.delete("1.0", END)
    messageWindow.insert('1.0', "[Grammar (Enhance)] ")

def handle_grammar_paraphrase():
    global TextBox_Selected
    if TextBox_Selected == 0:
        TextBox_Selected= 1
        messageWindow.delete("1.0", END)
    messageWindow.insert('1.0', "[Grammar (Paraphrase)] ")

def handle_grammar_simplify():
    global TextBox_Selected
    if TextBox_Selected == 0:
        TextBox_Selected= 1
        messageWindow.delete("1.0", END)
    messageWindow.insert('1.0', "[Grammar (Simplify)] ")

# File Menu
#-----------------------------------------------------------------------------#
def save_chat():

    #Check if there is already something to save
    if len(chat_history.load_memory_variables({})['history']) <= 0:

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "No chat history available to save.\n\n")
        chatWindow.config(state = DISABLED)

        #Scroll to the bottom of the chat history
        chatWindow.see(END)
    else:

        #Define log's name and path
        filename = f"{current_time('year')}{current_time('month')}{current_time('day')}_{current_time('hour')}h{current_time('minute')}_-_Chat_log.pkl"
        filepath = os.path.join(logs_relative_path, filename)
        try:
            if os.path.exists(logs_relative_path) == False:
                os.mkdir(logs_relative_path)

            #Save file
            dicts = messages_to_dict(chat_history.load_memory_variables({})['history'])
            with open(filepath, 'wb') as f:
                pickle.dump(dicts, f)

            #Send system message
            chatWindow.config(state = NORMAL)
            chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
            chatWindow.insert(END, "Chat history was saved.\n\n")
            chatWindow.config(state = DISABLED)

        except:
            #Send system message
            chatWindow.config(state = NORMAL)
            chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
            chatWindow.insert(END, "An error occurred while saving the chat history.\n\n")
            chatWindow.config(state = DISABLED)

        #Scroll to the bottom of the chat history
        chatWindow.see(END)

def load_chat():
    global chat_history

    #File Selection Menu
    filetypes = [('Pickle files', '*.pkl')]

    selected_file = fd.askopenfilename(
                                       title = 'Load chat log'
                                        ,initialdir = './'
                                        ,filetypes = filetypes
                                        )

    #Load file
    try:
        with open(selected_file, 'rb') as f:
            clear_chat()
            messages = messages_from_dict(pickle.load(f))

        #Loop chat_history and add messages
        for prompt in messages:
            if prompt.type == 'human':
                chat_history.chat_memory.add_user_message(prompt.content)
                chatWindow.config(state = NORMAL)
                chatWindow.insert(END, f"{User_agent}: ", "user")
                chatWindow.insert(END, answer_processing(prompt.content) + "\n\n")
                chatWindow.config(state = DISABLED)
            elif prompt.type == 'ai':
                chat_history.chat_memory.add_ai_message(prompt.content)
                chatWindow.config(state = NORMAL)
                chatWindow.insert(END, f"{AI_agent}: ", "ai")
                chatWindow.insert(END, answer_processing(prompt.content) + "\n\n")
                chatWindow.config(state = DISABLED)

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Chat history loaded.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred while loading the chat history.\n\n")
        chatWindow.config(state = DISABLED)

    #Scroll to the bottom of the chat history
    chatWindow.see(END)

def clear_chat():
    global chat_history
    chat_history = ConversationBufferWindowMemory(return_messages = True
                                                  ,k = max_memory)
    chatWindow.config(state = NORMAL)
    chatWindow.delete("1.0", END)
    chatWindow.config(state = DISABLED)

# AI Model
#-----------------------------------------------------------------------------#
def send():
    global chat_history

    #Temporarily store question
    question = str(messageWindow.get("1.0", END)).strip()

    #Ensure no empty string
    if len(question) > 0:

        #Refresh message box (start)
        refresh_message_box()

        #Refresh chat history (start)
        refresh_chat_history(question)

        #Disable menu options
        menubar_block(1)

        #Submit request to AI
        chat_history.chat_memory.add_user_message(question)
        grammar_check_request = 0
        max_len_grammar = 24
        if '[Grammar (Correct)]' in question[:max_len_grammar] or '[Grammar (Enhance)]' in question[:max_len_grammar] or '[Grammar (Paraphrase)]' in question[:max_len_grammar] or '[Grammar (Simplify)]' in question[:max_len_grammar]:
            grammar_check_request = 1
        if grammar_check_request == 0:
            draft_answer = AskAI(chat_history)
        else:
            if '[Grammar (Correct)]' in question[:max_len_grammar]:
                question = question.replace('[Grammar (Correct)]', '')
                command = "Fix the grammar: "
            elif '[Grammar (Enhance)]' in question[:max_len_grammar]:
                question = question.replace('[Grammar (Enhance)]', '')
                command = "Write this more formally and coherently: "
            elif '[Grammar (Paraphrase)]' in question[:max_len_grammar]:
                question = question.replace('[Grammar (Paraphrase)]', '')
                command = "Paraphrase this: "
            elif '[Grammar (Simplify)]' in question[:max_len_grammar]:
                question = question.replace('[Grammar (Simplify)]', '')
                command = "Rewrite to make this easier to understand: "

            question = question.strip()
            tokenizer = AutoTokenizer.from_pretrained(model_grammar_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_grammar_path)
            pipe = pipeline("text2text-generation"
                            ,model = model
                            ,tokenizer = tokenizer
                            ,max_new_tokens = 1024)
            draft_answer = pipe(command + question)[0]['generated_text']

        #Store AI's answer
        answer = answer_processing(draft_answer)
        chat_history.chat_memory.add_ai_message(answer)

        #Refresh chat history (end)
        refresh_chat_history(answer, 0)

        #Scroll to the bottom of the chat history
        chatWindow.see(END)

        #Enable menu options
        menubar_block(0)

        #Refresh message box (end)
        refresh_message_box(0)

        #Close Thread
        return

def AskAI(history):

    #Instantiate model
    model = AutoModelForCausalLM.from_pretrained(model_path_or_repo_id = model_chat_path
                                                 ,model_type = model_chat_type
                                                 ,model_file = model_chat_file
                                                 ,local_files_only = True
                                                 ,context_length = 8192
                                                 ,max_new_tokens = max_tokens_value
                                                 )    

    #Create chat history
    max_input_length = 8192
    system_prompt = "You are a personal assistant that provides short, concise and direct answers."
    messages = f"<s>{system_prompt}</s> "
    new_ai_message = ''
    new_question = 0
    for i in reversed(history.load_memory_variables({})['history']):
        if i.type == 'human':
            if new_question == 0:
                new_user_message = f"<s>[INST]{i.content}[/INST] "
                new_question = 1
            else:
                new_user_message = f"<s>{i.content} "
            if len(new_ai_message) > 0:
                temp_message =  messages + new_user_message + new_ai_message + new_message
                if len(model.tokenize(temp_message)) < max_input_length:
                    new_message = new_user_message + new_ai_message + new_message
                else:
                    break
            else:
                new_message = new_user_message
        else:
            new_ai_message = f"{i.content} </s>"
    messages = messages + new_message
    
    #Generate response
    answer = model(prompt = messages
                   ,temperature = temperature
                   ,repetition_penalty = repeat_penalty_value
                   )
    return(answer)

def summary_document():
    global chat_history
    global summary_goal
    global model_summarization_news_tokenizer_path, model_summarization_news_model_path
    global model_summarization_book_tokenizer_path, model_summarization_book_model_path
    global model_summarization_report_tokenizer_path, model_summarization_report_model_path

    #File Selection Menu
    filetypes = [('PDF file', '*.pdf')
                 ,('Word file', '*.docx')
                 ,('Text file', '*.txt')]

    selected_file_path = fd.askopenfilename(
                                           title = 'Select document to summarize'
                                           ,initialdir = './'
                                           ,filetypes = filetypes
                                           )

    #No file selected
    if selected_file_path == '':
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: no file was selected.\n\n")
        chatWindow.config(state = DISABLED)

        #Close Thread
        return

    #Disable menu options
    menubar_block(1)

    #Refresh message box (start)
    refresh_message_box()

    #Data Preparation
    try:
        
        #Load text
        doc = []
        if selected_file_path.endswith('.pdf'):
            converter = PDFToTextConverter(remove_numeric_tables = True
                                           ,multiprocessing = False)    #Otherwise, it creates multiple windows
            raw_doc = converter.convert(file_path = selected_file_path)[0]
            doc.append(raw_doc)
        elif selected_file_path.endswith('.docx'):
            converter = DocxToTextConverter(remove_numeric_tables = False
                                           ,multiprocessing = False) #Otherwise, it creates multiple windows
            raw_doc = converter.convert(file_path = selected_file_path)[0]
            doc.append(raw_doc)
        elif selected_file_path.endswith('.txt'):
            converter = TextConverter(remove_numeric_tables = True
                                           ,multiprocessing = False) #Otherwise, it creates multiple windows
            raw_doc = converter.convert(file_path = selected_file_path)[0]    
            doc.append(raw_doc)
        
        #Instantiate pre-processing
        preprocessor = PreProcessor(clean_header_footer = True
                                    ,clean_whitespace = True
                                    ,clean_empty_lines = True
                                    ,split_by = "sentence" #"word", "sentence" or "passage" (i.e., paragraph)
                                    ,split_length = 8 #Maximum lenght of the unit selected (word, sentence or passage/paragraph)
                                    ,split_overlap = 0
                                    ,split_respect_sentence_boundary = False #'split_respect_sentence_boundary=True' is only compatible with split_by='word'
                                    ,add_page_number = False
                                    )
        
        #Pre-process text
        docs = preprocessor.process(doc)

        #Combine into single text
        full_text = "".join([text.content for text in docs])
        full_text = clean(full_text
                          ,lower = False
                          ,lang = "en") #Set to 'de' for German special handling
        
        #Refresh chat history (start)
        question = f"Please provide a summary of the document {os.path.basename(selected_file_path)}."
        refresh_chat_history(question)

        #Store user's prompt
        chat_history.chat_memory.add_user_message(question)

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Document was successfully loaded and pre-processed.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: it was not possible to load and pre-process the text of the selected file.\n\n")
        chatWindow.config(state = DISABLED)

    #Model loading
    try:
        if summary_goal == 0:
            summary_goal_descr = "summarization of a news article"
            tokenizer_summarization_path = model_summarization_news_tokenizer_path
            model_summarization_path = model_summarization_news_model_path
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_summarization_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_summarization_path).to(device)
            model_input_max_length = 1024
        elif summary_goal == 1:
            summary_goal_descr = "summarization of a book"
            tokenizer_summarization_path = model_summarization_book_tokenizer_path
            model_summarization_path = model_summarization_book_model_path
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_summarization_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_summarization_path).to(device)
            model_input_max_length = 16384
        elif summary_goal == 2:
            summary_goal_descr = "summarization of a report"
            tokenizer_summarization_path = model_summarization_report_tokenizer_path
            model_summarization_path = model_summarization_report_model_path
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_summarization_path)
            config = AutoConfig.from_pretrained(model_summarization_path
                                                ,min_new_tokens = 5)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_summarization_path
                                                          ,config = config).to(device)
            model_input_max_length = 16384

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, f"Model for {summary_goal_descr} was selected.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: it was not possible to load the model for the selected purpose.\n\n")
        chatWindow.config(state = DISABLED)

    #Generate summarization pipeline
    try:
        def count_tokens(text):
            number_tokens = len(tokenizer(text)["input_ids"])
            return number_tokens
        if count_tokens(full_text) < model_input_max_length:
            chunk_required = 0
            pipe = pipeline(task = 'summarization'
                            ,model = model
                            ,tokenizer = tokenizer
                            ,device = device
                            ,framework = 'pt'
                            ,truncation = False
                            ,clean_up_tokenization_spaces = True
                            ,num_beams = 5
                            ,do_sample = False
                            ,min_new_tokens = 5
                            ,max_new_tokens = 1024)
            summary = full_text

        else:
            chunk_required = 1
            summary = f"The document is too lengthy for the selected model! Model's maximum tokens = {model_input_max_length} vs. Document's tokens = {count_tokens(full_text)}."

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: it was not possible to setup the pipeline.\n\n")
        chatWindow.config(state = DISABLED)

    #Generate summary
    try:
        if chunk_required == 0:
            pipe_out = pipe(summary)
            summary_final = "\n".join(sent_tokenize(pipe_out[0]["summary_text"]
                                                    ,language = "english"))
        else:
            summary_final = summary
    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: it was not possible to generate a summary.\n\n")
        chatWindow.config(state = DISABLED)

    #Store AI's answer
    chat_history.chat_memory.add_ai_message(summary_final)

    #Refresh chat history (end)
    refresh_chat_history(summary_final, 0)

    #Scroll to the bottom of the chat history
    chatWindow.see(END)

    #Enable menu options
    menubar_block(0)

    #Refresh message box (end)
    refresh_message_box(0)

    #Close Thread
    return

def create_CKB():
    global chat_history

    #Folder Selection Menu
    selected_folder = fd.askdirectory(title = 'Select folder with documents in pdf, docx or txt format'
                                      ,initialdir = './'
                                      )

    #No folder selected
    if selected_folder == '':
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: no folder was selected.\n\n")
        chatWindow.config(state = DISABLED)

        #Close Thread
        return

    #Disable menu options
    menubar_block(1)

    #Refresh message box (start)
    refresh_message_box()

    #Data Preparation and split into chunks
    try:

        #Load text
        files_to_index = []
        raw_docs = []
        date_file = str(current_time('year')) + '-' + str(current_time('month')) + '-' + str(current_time('day'))
        for selected_file in os.listdir(selected_folder):
            selected_file_path = os.path.join(selected_folder, selected_file)
            if os.path.isfile(selected_file_path) == True:
                if selected_file.endswith('.pdf'):
                    name_file = os.path.basename(selected_file_path)
                    files_to_index.append(str(name_file))
                    converter = PDFToTextConverter(remove_numeric_tables = True
                                                   ,multiprocessing = False) #Otherwise, it creates multiple windows
                    doc = converter.convert(file_path = selected_file_path
                                            ,meta = {'name' : name_file
                                                     ,'date' : date_file})[0]
                    raw_docs.append(doc)
                elif selected_file.endswith('.docx'):
                    name_file = os.path.basename(selected_file_path)
                    files_to_index.append(str(name_file))
                    converter = DocxToTextConverter(remove_numeric_tables = False
                                                   ,multiprocessing = False) #Otherwise, it creates multiple windows
                    doc = converter.convert(file_path = selected_file_path
                                            ,meta = {'name' : name_file
                                                     ,'date' : date_file})[0]
                    raw_docs.append(doc)

                elif selected_file.endswith('.txt'):
                    name_file = os.path.basename(selected_file_path)
                    files_to_index.append(str(name_file))
                    converter = TextConverter(remove_numeric_tables = True) #Otherwise, it creates multiple windows
                    doc = converter.convert(file_path = selected_file_path
                                            ,meta = {'name' : name_file
                                                     ,'date' : date_file})[0]
                    raw_docs.append(doc)

        #Instantiate pre-processing
        preprocessor = PreProcessor(clean_header_footer = True
                                    ,clean_whitespace = True
                                    ,clean_empty_lines = True
                                    ,split_by = "sentence" #"word", "sentence" or "passage" (i.e., paragraph)
                                    ,split_length = 8 #Maximum lenght of the unit selected (word, sentence or passage/paragraph)
                                    ,split_overlap = 0
                                    ,split_respect_sentence_boundary = False #'split_respect_sentence_boundary=True' is only compatible with split_by='word'
                                    ,add_page_number = True
                                    )

        #Pre-process text
        docs = preprocessor.process(raw_docs)

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, f"Document(s) was(were) successfully loaded.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, f"An error occurred: it was not possible to load the text from the document {selected_file}.\n\n")
        chatWindow.config(state = DISABLED)

    #Store chunks
    try:

        #Instantiate document store
        document_store = FAISSDocumentStore(faiss_index_factory_str = "Flat")

        #Compile chunks into dictionary
        dicts = []
        for chunk in docs:
            document_text = clean(chunk.content.strip()
                                  ,lower = False
                                  ,lang = "en") #Set to 'de' for German special handling
            dicts.append({
                          'content': document_text
                          ,'meta': {'name': chunk.meta['name']
                                    ,'date': chunk.meta['date']
                                    ,'page': chunk.meta['page']
                                    }
                          }
                         )

        #Store data in document store
        document_store.write_documents(dicts)

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Document(s) was(were) successfully stored.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: it was not possible to store the document(s).\n\n")
        chatWindow.config(state = DISABLED)

    #Instantiate the embeddings/retriever model
    try:
        retriever = EmbeddingRetriever(document_store = document_store
                                       ,embedding_model = model_QA_retriever_path
                                       ,use_gpu = False
                                       ,model_format = "transformers"
                                       )

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Retriever model was successfully instantiated.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: retriever model was not instantiated.\n\n")
        chatWindow.config(state = DISABLED)

    #Index document
    try:
        document_store.update_embeddings(retriever)

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Embeddings for the document(s) was(were) sucessfully created.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: it was not possible to generate the embeddings for the document(s).\n\n")
        chatWindow.config(state = DISABLED)

    #Save Custom Knowledge Database (CKB)
    try:
        if os.path.exists(embeddings_relative_path) == False:
            os.mkdir(embeddings_relative_path)
        db_name = f"{current_time('year')}{current_time('month')}{current_time('day')}_{current_time('hour')}h{current_time('minute')}.faiss"
        db_config_name = f"{current_time('year')}{current_time('month')}{current_time('day')}_{current_time('hour')}h{current_time('minute')}.json"
        db_sql_name = f"{current_time('year')}{current_time('month')}{current_time('day')}_{current_time('hour')}h{current_time('minute')}.db"
        document_store.save(index_path = os.path.join(embeddings_relative_path, db_name)
                            ,config_path = os.path.join(embeddings_relative_path, db_config_name))
        with open(f"{embeddings_relative_path}/{current_time('year')}{current_time('month')}{current_time('day')}_{current_time('hour')}h{current_time('minute')}.txt", 'w') as f:
            for selected_file in files_to_index:
                f.write(selected_file)
                f.write('\n')
        shutil.copyfile("./faiss_document_store.db", os.path.join(embeddings_relative_path, db_sql_name))
        os.remove("./faiss_document_store.db")

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Custom Knowledge Database (CKB) was successfully saved.\n\n")
        chatWindow.config(state = DISABLED)
    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: it was not possible to save the Custom Knowledge Database (CKB).\n\n")
        chatWindow.config(state = DISABLED)

    #Scroll to the bottom of the chat history
    chatWindow.see(END)

    #Enable menu options
    menubar_block(0)

    #Refresh message box (end)
    refresh_message_box(0)

    #Close Thread
    return

def use_CKB():
    global chat_history

    #Folder Selection Menu
    selected_CBK = fd.askdirectory(
                                   title = 'Select folder with an existing Custom Base Knowledge index'
                                   ,initialdir = './'
                                   )

    #No CBK selected
    if selected_CBK == '':
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: no Custom Base Knowledge (CBK) was selected.\n\n")
        chatWindow.config(state = DISABLED)

        #Close Thread
        return

    #Disable menu options
    menubar_block(1)

    #Refresh message box (start)
    refresh_message_box()

    #Load Custom Knowledge Base (CKB)
    try:
        db_name = ''
        db_config_name = ''
        db_sql_name = ''
        for selected_file in os.listdir(selected_CBK):
            if selected_file.endswith('.faiss'):
                db_name = selected_file
            elif selected_file.endswith('.json'):
                db_config_name = selected_file
            elif selected_file.endswith('.db'):
                db_sql_name = selected_file

        with open(os.path.join(selected_CBK, db_config_name), 'r') as f:
                data = json.load(f)
                data['sql_url'] = "sqlite:///" + os.path.join(selected_CBK, db_sql_name)

        os.remove(os.path.join(selected_CBK, db_config_name))
        with open(os.path.join(selected_CBK, db_config_name), 'w') as f:
            json.dump(data, f, indent=4)
        document_store = FAISSDocumentStore(faiss_index_path = os.path.join(selected_CBK, db_name)
                                            ,faiss_config_path = os.path.join(selected_CBK, db_config_name)
                                            )

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Custom Knowledge Database (CKB) was successfully loaded.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: Custom Knowledge Database (CKB) was not loaded.\n\n")
        chatWindow.config(state = DISABLED)

    #Instantiate the retriever
    try:
        retriever = EmbeddingRetriever(document_store = document_store
                                       ,embedding_model = model_QA_retriever_path
                                       ,use_gpu = False
                                       ,model_format = "transformers"
                                       )

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Retriever model was successfully instantiated.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: retriever model was not instantiated.\n\n")
        chatWindow.config(state = DISABLED)

    #Prompt user to ask the question
    temp_root = Tk()
    temp_root.withdraw() #Make it invisible
    query = simpledialog.askstring('What question do you have for the CKB?'
                                   ,'Question:'
                                   ,parent = temp_root)
    temp_root.destroy()

    #Refresh chat history (start)
    refresh_chat_history(str(query))

    #Store user's prompt
    chat_history.chat_memory.add_user_message(str(query))

    if query.strip() != '' and query != None:
        try:
            #Querying pipeline
            querying_pipeline = Pipeline()
            querying_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])

            relevant_info = querying_pipeline.run(query = query
                                                  ,params = {"Retriever": {"top_k": 4}}
                                                  )

            #Define context and prompt
            context = ""
            for document in relevant_info['documents']:
                doc_cont = document.content.replace('\n', ' ').strip()
                context = context + f"\n{doc_cont}"
                
            prompt = f"""<s>Answer the question or request as truthfully as possible using the provided context. Context: {context}</s><s>[INST]{str(query)}[/INST]""".strip()
            
            #Instantiate model
            model = AutoModelForCausalLM.from_pretrained(model_path_or_repo_id = model_chat_path
                                                         ,model_type = model_chat_type
                                                         ,model_file = model_chat_file
                                                         ,local_files_only = True
                                                         ,context_length = 8192)

            #Restrict the prompt
            max_input_length = 8192
            tokens = model.tokenize(prompt)
            if len(tokens) > max_input_length:
                tokens_to_remove = max(len(tokens) - max_input_length, 0)
                tokens_context = model.tokenize(context)
                context_length = len(tokens_context)
                restricted_context_length = context_length - tokens_to_remove
                restricted_context_tokens = tokens_context[:restricted_context_length]
                context = model.detokenize(restricted_context_tokens).strip()
                prompt = f"""<s>Answer the question or request as truthfully as possible using the provided context. Context: {context}</s><s>[INST]{str(query)}[/INST]""".strip()

            #Generate answer
            answer = model(prompt = prompt
                           ,max_new_tokens = max_tokens_value
                           ,temperature = 0
                           )
            answer = answer_processing(answer)

            #Store AI's answer
            chat_history.chat_memory.add_ai_message(answer)

            #Refresh chat history (end)
            refresh_chat_history(answer, 0)

        except:
            #Send system message
            chatWindow.config(state = NORMAL)
            chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
            chatWindow.insert(END, "An error occurred: it was not possible to search the Custom Knowledge Database (CKB).\n\n")
            chatWindow.config(state = DISABLED)

    else:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: user did not insert a question.\n\n")
        chatWindow.config(state = DISABLED)

    #Scroll to the bottom of the chat history
    chatWindow.see(END)

    #Enable menu options
    menubar_block(0)

    #Refresh message box (end)
    refresh_message_box(0)

    #Close Thread
    return

# GUI
#-----------------------------------------------------------------------------#
def refresh_message_box(start = 1):
    if start == 1:

        #Freeze message box and clear content
        messageWindow.delete("1.0", END)
        messageWindow.insert(END, "Processing your request...", "hint")
        messageWindow.config(state = DISABLED)
    else:

        #Unfreeze message box and clear content
        messageWindow.config(state = NORMAL)
        messageWindow.delete("1.0", END)

        #Play sound notification
        winsound.Beep(freq, duration)

def refresh_chat_history(prompt, start = 1):
    if start == 1:

        #Post the question and time of its submission by the user
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{User_agent} [{current_time('hour')}:{current_time('minute')}]: ", "user")
        chatWindow.insert(END, prompt + "\n\n")
        chatWindow.config(state = DISABLED)
    else:

        #Post the answer and time of its submission by the AI
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{AI_agent} [{current_time('hour')}:{current_time('minute')}]: ", "ai")
        chatWindow.insert(END, prompt + "\n\n")
        chatWindow.config(state = DISABLED)

        #Scroll to the bottom of the chat history
        chatWindow.see(END)

def answer_processing(answer):
    answer = answer.strip()
    return(answer)

def menubar_block(block = 1):
    if block == 1:
        file_menu.entryconfig('Save chat', state = "disabled")
        file_menu.entryconfig('Load chat', state = "disabled")
        file_menu.entryconfig('Clear chat', state = "disabled")
        file_menu.entryconfig('Exit', state = "disabled")
        tools_menu.entryconfig('Summarize news article', state = "disabled")
        tools_menu.entryconfig('Summarize book', state = "disabled")
        tools_menu.entryconfig('Summarize report', state = "disabled")
        tools_menu.entryconfig('Create CKB', state = "disabled")
        tools_menu.entryconfig('Use CKB', state = "disabled")
        grammar_menu.entryconfig('Correct', state = "disabled")
        grammar_menu.entryconfig('Enhance', state = "disabled")
        grammar_menu.entryconfig('Paraphrase', state = "disabled")
        grammar_menu.entryconfig('Simplify', state = "disabled")

    else:
        file_menu.entryconfig('Save chat', state = "normal")
        file_menu.entryconfig('Load chat', state = "normal")
        file_menu.entryconfig('Clear chat', state = "normal")
        file_menu.entryconfig('Exit', state = "normal")
        tools_menu.entryconfig('Summarize news article', state = "normal")
        tools_menu.entryconfig('Summarize book', state = "normal")
        tools_menu.entryconfig('Summarize report', state = "normal")
        tools_menu.entryconfig('Create CKB', state = "normal")
        tools_menu.entryconfig('Use CKB', state = "normal")
        grammar_menu.entryconfig('Correct', state = "normal")
        grammar_menu.entryconfig('Enhance', state = "normal")
        grammar_menu.entryconfig('Paraphrase', state = "normal")
        grammar_menu.entryconfig('Simplify', state = "normal")

#*****************************************************************************#
# GUI
#*****************************************************************************#

# Parent Window
root = Tk()

# Configure Parent Window
root.title("Chat")
root['bg'] = '#2A2C36'
root.resizable(width = False
               ,height = False)

# TTK Styles
BG_COLOR_CHAT = "#393A47"
BG_COLOR_MESSAGE = "#343542"
TEXT_COLOR = "#EAECEE"
FONT = "Gadugi 12"

# Menubar
menubar = Menu(root)
root.config(menu = menubar)

# File menu
file_menu = Menu(tearoff = False)
menubar.add_cascade(label = "File"
                    ,menu = file_menu)

# Tools menu
tools_menu = Menu(tearoff = False)
menubar.add_cascade(label = "Tools"
                    ,menu = tools_menu)

# Grammar menu
grammar_menu = Menu(tearoff = False)
menubar.add_cascade(label = "Grammar"
                    ,menu = grammar_menu)

# Add File menu options
file_menu.add_command(label = 'Save chat'
                      ,command = save_chat)
file_menu.add_command(label = 'Load chat'
                      ,command = load_chat)
file_menu.add_separator()
file_menu.add_command(label = 'Clear chat'
                      ,command = clear_chat)
file_menu.add_command(label = 'Exit'
                      ,command = root.destroy)

# Add Tools menu options
tools_menu.add_command(label = 'Summarize news article'
                      ,command = handle_summarize_news_article)
tools_menu.add_command(label = 'Summarize book'
                      ,command = handle_summarize_book)
tools_menu.add_command(label = 'Summarize report'
                      ,command = handle_summarize_report)
tools_menu.add_command(label = 'Create CKB'
                      ,command = handle_create_CKB)
tools_menu.add_command(label = 'Use CKB'
                      ,command = handle_use_CKB)

# Add Grammar menu options
grammar_menu.add_command(label = 'Correct'
                      ,command = handle_grammar_correct)
grammar_menu.add_command(label = 'Enhance'
                      ,command = handle_grammar_enhance)
grammar_menu.add_command(label = 'Paraphrase'
                      ,command = handle_grammar_paraphrase)
grammar_menu.add_command(label = 'Simplify'
                      ,command = handle_grammar_simplify)

# Conversation Area
chatWindow = Text(root
                  ,wrap = WORD
                  ,bd = 1
                  ,bg = BG_COLOR_CHAT
                  ,fg = TEXT_COLOR
                  ,font = FONT
                  ,insertbackground = 'white'
                  ,width = 120)

chatWindow.grid(row = 0
                ,column = 0
                ,columnspan = 2)

# Disable the text widget
chatWindow.config(state = DISABLED)

chatWindow.tag_config("user", font = "Gadugi 12 bold", foreground = "#00FFFF")
chatWindow.tag_config("ai", font = "Gadugi 12 bold", foreground = "#FF6200")
chatWindow.tag_config("system", font = "Gadugi 12 bold", foreground = "#00b588")

# Message Area
messageWindow = Text(root
                     ,wrap = WORD
                     ,bg = BG_COLOR_MESSAGE
                     ,fg = TEXT_COLOR
                     ,font = FONT
                     ,insertbackground = 'white'
                     ,height = 5
                     ,width = 120
                     )
messageWindow.grid(row = 1
                   ,column = 0
                   ,columnspan = 2
                   ,pady = 5
                   ,padx = 2.5)

messageWindow.tag_config("hint", font = "Gadugi 12", foreground = "#5D5E6B")

messageWindow.insert(END, "Send a message...", "hint")

messageWindow.bind("<Button-1>", lambda e: DeleteHint())
messageWindow.bind('<Return>', handle_enter)
messageWindow.bind('<Shift-Return>', handle_enter_shift)

# Launch menu
root.mainloop()
