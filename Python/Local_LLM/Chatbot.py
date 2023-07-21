#*****************************************************************************#
# REQUIREMENTS
#*****************************************************************************#
#Large Language Models to use can be found here: https://gpt4all.io/index.html
#!pip install gpt4all==0.3.4 (version used)
#!pip install langchain==0.0.205 (version used)
#!pip install docx2txt==0.8 (version used)
#!pip install pypdf==3.11.0 (version used)
#!pip install transformers==4.30.2 (version used)
#!pip install faiss-cpu==1.7.4 (version used)
#!pip install -U sentence-transformers==2.2.2 (version used)
#!pip install -U spacy==3.5.3 (version used)
#!python -m spacy download en_core_web_md
#!pip install auto-py-to-exe

#*****************************************************************************#
# GENERAL
#*****************************************************************************#

# AI Model
#-----------------------------------------------------------------------------#
from gpt4all import GPT4All
from threading import Thread
User_agent = "You"
AI_agent = "AI"
System_agent = "System"
model_name = "ggml-wizardLM-7B.q4_2.bin"
model_relative_path = "./Models"
logs_relative_path = "./Logs"
embeddings_relative_path = "./CKB"
allow_model_download = False

# AI Configuration
#-----------------------------------------------------------------------------#
context_window = 8192               # Range of tokens the AI model can access and consider when generating responses to prompts (1,000 tokens ≈ 750 words)
temperature = 0.28                  # Randomness of the words
top_p_value = 0.95                  # Top P sampling parameter
top_k_value = 40                    # Top K sampling parameter
max_tokens = 8192                   # Inference stops if it reaches n_predict tokens
max_tokens_summary = 16384          # Inference stops if it reaches n_predict tokens when summarizing
prompt_batch_size = 9               # Number of tokens in the prompt that are fed into the model at a time
repeat_penalty_value = 1.1          # Repeat penalty sampling parameter
repeat_last_n_value = 64            # Last n tokens to penalize
chat_history = []                   # Messages stored from the conversation
extractive_text_summarization = 1   # Whether to use extractive or abstractive (LLM)

# GUI
#-----------------------------------------------------------------------------#
from tkinter import *
from tkinter import filedialog as fd
from tkinter import simpledialog
import datetime
import pickle
import os
import winsound
duration = 300             # Milliseconds
freq = 500                 # Frequency (in Hz)
TextBox_Selected = 0       # Whether the user has already pressed the message box

#*****************************************************************************#
# DOWNLOAD MODELS
#*****************************************************************************#

# Large Language Model
#-----------------------------------------------------------------------------#
if os.path.exists(model_relative_path) == False:
    os.mkdir(model_relative_path)
    model = GPT4All(model_name
                    ,model_path = model_relative_path
                    ,allow_download = True)
    del model
else:
    model = GPT4All(model_name
                    ,model_path = model_relative_path
                    ,allow_download = True)
    del model

# Tokenizers / Summarize
#-----------------------------------------------------------------------------#
if os.path.exists(os.path.join(model_relative_path, "Tokenizer")) == False:
    os.mkdir(os.path.join(model_relative_path, "Tokenizer"))
    from transformers import GPT2TokenizerFast
    model = GPT2TokenizerFast.from_pretrained("gpt2")
    model.save_pretrained(os.path.join(model_relative_path, "Tokenizer"))
    del model
else:
    from transformers import GPT2TokenizerFast
    model = GPT2TokenizerFast.from_pretrained("gpt2")
    model.save_pretrained(os.path.join(model_relative_path, "Tokenizer"))
    del model

# Embeddings model
#-----------------------------------------------------------------------------#
if os.path.exists(os.path.join(model_relative_path, "Embeddings")) == False:
    os.mkdir(os.path.join(model_relative_path, "Embeddings"))
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    model.save(os.path.join(model_relative_path, "Embeddings"))
    del model
else:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    model.save(os.path.join(model_relative_path, "Embeddings"))
    del model

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

def handle_summarize():
    Thread(target = summary_document, daemon = True).start()

def handle_create_CKB():
    Thread(target = create_CKB, daemon = True).start()

def handle_use_CKB():
    Thread(target = use_CKB, daemon = True).start()

# File Menu
#-----------------------------------------------------------------------------#
def save_chat():

    #Check if there is already something to save
    if len(chat_history) <= 0:

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
            with open(filepath, 'wb') as f:
                pickle.dump(chat_history, f)

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
            chat_history = pickle.load(f)

        #Loop chat_history and add messages
        for prompt in chat_history:
            if prompt['role'] == 'user':
                chatWindow.config(state = NORMAL)
                chatWindow.insert(END, f"{User_agent}: ", "user")
                chatWindow.insert(END, prompt['content'] + "\n\n")
                chatWindow.config(state = DISABLED)
            elif prompt['role'] == 'assistant':
                chatWindow.config(state = NORMAL)
                chatWindow.insert(END, f"{AI_agent}: ", "ai")
                chatWindow.insert(END, answer_processing(prompt['content']) + "\n\n")
                chatWindow.config(state = DISABLED)

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Chat history was loaded.\n\n")
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
    chat_history = []
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

        #Store user's prompt
        messages = {"role": "user", "content": question}
        chat_history.append(messages)

        #Disable menu options
        menubar_block(1)

        #Check if model directory exists (otherwise, create it)
        try:
            if os.path.exists(model_relative_path) == False:
                os.mkdir(model_relative_path)

        except:
            #Send system message
            chatWindow.config(state = NORMAL)
            chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
            chatWindow.insert(END, "An error occurred while creating the folder to store the AI.\n\n")
            chatWindow.config(state = DISABLED)

        #Submit request to AI
        ret = AskAI(chat_history)

        #Store AI's answer
        chat_history.append(ret["choices"][0]["message"])
        draft_answer = str(ret["choices"][0]["message"]["content"]).strip()
        answer = answer_processing(draft_answer)

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

def AskAI(chat_history):
    model = GPT4All(model_name
                    ,model_path = model_relative_path
                    ,allow_download = allow_model_download)
    return(model.chat_completion(chat_history
                                 ,n_predict = max_tokens
                                 ,n_ctx = context_window
                                 ,top_k = top_k_value
                                 ,top_p = top_p_value
                                 ,temp = temperature
                                 ,repeat_penalty = repeat_penalty_value
                                 ,repeat_last_n = repeat_last_n_value
                                 ,n_batch = prompt_batch_size
                                 ,verbose = False
                                 ,streaming = False
                                 )
           )

def summary_document():
    global chat_history
    global extractive_text_summarization

    #File Selection Menu
    filetypes = [('PDF file', '*.pdf')
                 ,('Word file', '*.docx')
                 ,('Text file', '*.txt')]

    selected_file = fd.askopenfilename(
                                       title = 'Select document to summarize'
                                        ,initialdir = './'
                                        ,filetypes = filetypes
                                        )

    #No file selected
    if selected_file == '':
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
        if selected_file.endswith('.pdf'):
            from langchain.document_loaders import PyPDFLoader
            loader = PyPDFLoader(selected_file)
            text = loader.load()

        elif selected_file.endswith('.docx'):
            from langchain.document_loaders import Docx2txtLoader
            loader = Docx2txtLoader(selected_file)
            text = loader.load()

        elif selected_file.endswith('.txt'):
            from langchain.docstore.document import Document
            with open(selected_file) as f:
                text = f.read()

        #Refresh chat history (start)
        question = f"Please provide a summary of the document {selected_file.split('/')[-1]}."
        refresh_chat_history(question)

        #Store user's prompt
        messages = {"role": "user", "content": question}
        chat_history.append(messages)

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Document was successfully loaded.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: it was not possible to load the text of the selected file.\n\n")
        chatWindow.config(state = DISABLED)

    #Process text into chunks
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        docs = []
        splitter = RecursiveCharacterTextSplitter(chunk_size = 1000
                                                  ,chunk_overlap = 0
                                                  ,length_function = len)
        if selected_file.endswith('.txt'):
            from langchain.docstore.document import Document
            texts = splitter.split_text(text)
            docs = [Document(page_content = t) for t in texts]
        else:
            for chunk in splitter.split_documents(text):
                docs.append(chunk)

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Document was successfully processed.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: it was not possible to process the text of the selected file.\n\n")
        chatWindow.config(state = DISABLED)

    #Generate the summary
        #Extractive Text Summarization (together with LLM to further process the summary)
    if extractive_text_summarization == 1:
        try:
            #Modules
            import spacy
            from spacy.lang.en.stop_words import STOP_WORDS
            from string import punctuation
            from heapq import nlargest

            #Text Summarizer Function
            def textSummarizer(text, percentage):

                ##Load the model into spaCy
                nlp = spacy.load('en_core_web_md')

                ##Pass the text into the nlp function
                doc = nlp(text)

                ##The score of each word is kept in a frequency table
                freq_of_word = dict()

                ##Text cleaning and vectorization
                for word in doc:
                    if word.text.lower() not in list(STOP_WORDS):
                        if word.text.lower() not in punctuation:
                            if word.text not in freq_of_word.keys():
                                freq_of_word[word.text] = 1
                            else:
                                freq_of_word[word.text] += 1

                ##Maximum frequency of word
                max_freq = max(freq_of_word.values())

                ##Normalization of word frequency
                for word in freq_of_word.keys():
                    freq_of_word[word] = freq_of_word[word] / max_freq

                ##In this part, each sentence is weighed based on how often it contains the token.
                sent_tokens= [sent for sent in doc.sents]
                sent_scores = dict()
                for sent in sent_tokens:
                    for word in sent:
                        if word.text.lower() in freq_of_word.keys():
                            if sent not in sent_scores.keys():
                                sent_scores[sent] = freq_of_word[word.text.lower()]
                            else:
                                sent_scores[sent] += freq_of_word[word.text.lower()]


                len_tokens = int(len(sent_tokens) * percentage)

                ##Summary for the sentences with maximum score. Here, each sentence in the list is of spacy.span type
                summary = nlargest(n = len_tokens
                                   ,iterable = sent_scores
                                   ,key = sent_scores.get)

                ##Prepare for final summary
                final_summary = [word.text for word in summary]

                ##Convert to a string
                summary = " ".join(final_summary)

                ##Return final summary
                return summary

            #Convert documents into raw text
            docs_text = "".join([doc.page_content for doc in docs])

            #Generate summary with Spacy (5 is the average number of characters per word)
            perc_summary = round(min((290 * 5) / len(docs_text), 1), 2) #To avoid excessive context
            context = textSummarizer(docs_text, perc_summary)

            #Load modules
            from langchain import PromptTemplate
            from langchain.llms import GPT4All as LG_GPT4All
            from langchain import LLMChain

            #Instantiate the model
            llm = LG_GPT4All(model = os.path.join(model_relative_path, model_name)
                             ,n_predict = max_tokens_summary
                             ,n_ctx = context_window
                             ,top_k = top_k_value
                             ,top_p = top_p_value
                             ,temp = 0
                             ,repeat_penalty = repeat_penalty_value
                             ,repeat_last_n = repeat_last_n_value
                             ,n_batch = prompt_batch_size
                             ,verbose = False
                             ,streaming = False)

            #Create prompt with context
            prompt_template = """Write a concise summary of the following text delimited by triple backquotes.
            Return your response in bullet points which covers the key points of the text.
            ```{text}```
            BULLET POINT SUMMARY:"""
            PROMPT = PromptTemplate(template = prompt_template
                                    ,input_variables = ["text"])

            #Generate response
            chain = LLMChain(prompt = PROMPT
                             ,llm = llm
                             ,verbose = False)
            answer = chain.run(context)

            #Store AI's answer
            messages = {"role": "assistant", "content": answer}
            chat_history.append(messages)

            #Refresh chat history (end)
            refresh_chat_history(answer, 0)

        except:
            #Send system message
            chatWindow.config(state = NORMAL)
            chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
            chatWindow.insert(END, "An error occurred: it was not possible to generate a summary.\n\n")
            chatWindow.config(state = DISABLED)
    else:
        #Abstractive Text Summarization
        try:

            from langchain import PromptTemplate
            from langchain.llms import GPT4All as LG_GPT4All
            from langchain.chains.summarize import load_summarize_chain

            #Instantiate the model
            llm = LG_GPT4All(model = os.path.join(model_relative_path, model_name)
                             ,n_predict = max_tokens_summary
                             ,n_ctx = context_window
                             ,top_k = top_k_value
                             ,top_p = top_p_value
                             ,temp = 0
                             ,repeat_penalty = repeat_penalty_value
                             ,repeat_last_n = repeat_last_n_value
                             ,n_batch = prompt_batch_size
                             ,verbose = False
                             ,streaming = False)

            #Prompt design with "MapReduce" chain
            #With LangChain, the map_reduce chain breaks the document down into 1024 token chunks max.
            #Then it runs the initial prompt (map_prompt) you define on each chunk to generate a summary of that chunk.
            #In the end, all chunks are combined with the combine_prompt
            prompt_template = """Write a concise summary of the following text delimited by triple backquotes.
            ```{text}```
            SUMMARY:"""
            PROMPT = PromptTemplate(template = prompt_template
                                    ,input_variables = ["text"])

            combined_prompt_template = """Write a concise summary of the following text delimited by triple backquotes.
            Return your response in bullet points which covers the key points of the text.
            ```{text}```
            SUMMARY:"""
            COMBINED_PROMPT = PromptTemplate(template = combined_prompt_template
                                             ,input_variables = ["text"])

            #Generate response
            chain = load_summarize_chain(llm
                                         ,chain_type = "map_reduce"
                                         ,map_prompt = COMBINED_PROMPT #Final prompt
                                         ,combine_prompt = PROMPT #Intermediate prompt
                                         ,verbose = False
                                         ,return_intermediate_steps = False
                                         )
            answer = chain.run(docs)

            #Store AI's answer
            messages = {"role": "assistant", "content": answer}
            chat_history.append(messages)

            #Refresh chat history (end)
            refresh_chat_history(answer, 0)

        except:
            #Send system message
            chatWindow.config(state = NORMAL)
            chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
            chatWindow.insert(END, "An error occurred: it was not possible to generate a summary.\n\n")
            chatWindow.config(state = DISABLED)

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
    selected_CBK = fd.askdirectory(
                                   title = 'Select folder with an existing Custom Base Knowledge index (if available)'
                                   ,initialdir = './'
                                   )

    #File Selection Menu
    filetypes = [('PDF file', '*.pdf')
                 ,('Word file', '*.docx')
                 ,('Text file', '*.txt')]

    selected_file = fd.askopenfilename(
                                       title = 'Select document to generate embeddings for'
                                        ,initialdir = './'
                                        ,filetypes = filetypes
                                        )

    #No file selected
    if selected_file == '':
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
        if selected_file.endswith('.pdf'):
            from langchain.document_loaders import PyPDFLoader
            loader = PyPDFLoader(selected_file)
            text = loader.load()

        elif selected_file.endswith('.docx'):
            from langchain.document_loaders import Docx2txtLoader
            loader = Docx2txtLoader(selected_file)
            text = loader.load()

        elif selected_file.endswith('.txt'):
            from langchain.docstore.document import Document
            with open(selected_file) as f:
                text = f.read()

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Document was successfully loaded.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: it was not possible to load the text of the selected file.\n\n")
        chatWindow.config(state = DISABLED)

    #Process text into chunks
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        docs = []
        splitter = RecursiveCharacterTextSplitter(chunk_size = 1000
                                                  ,chunk_overlap = 0
                                                  ,length_function = len)
        if selected_file.endswith('.txt'):
            from langchain.docstore.document import Document
            texts = splitter.split_text(text)
            docs = [Document(page_content = t) for t in texts]
        else:
            for chunk in splitter.split_documents(text):
                docs.append(chunk)

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Document was successfully processed.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: it was not possible to process the text of the selected file.\n\n")
        chatWindow.config(state = DISABLED)

    #Instantiate the embeddings model
    try:
        from langchain.embeddings import SentenceTransformerEmbeddings
        embeddings = SentenceTransformerEmbeddings(model_name = os.path.join(model_relative_path, "Embeddings"))

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Embeddings model was successfully instantiated.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: embeddings model 'all-MiniLM-L6-v2' was not instantiated.\n\n")
        chatWindow.config(state = DISABLED)

    #Index document
    try:
        from langchain.vectorstores.faiss import FAISS

        #Generate vector index database
        def create_index(chunks):
            texts = [doc.page_content for doc in chunks]
            metadatas = [doc.metadata for doc in chunks]
            search_index = FAISS.from_texts(texts
                                            ,embeddings
                                            ,metadatas = metadatas)
            return search_index
        db0 = create_index(docs)

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Document's embeddings were sucessfully created.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: it was not possible to generate the document's embeddings.\n\n")
        chatWindow.config(state = DISABLED)

    #Merge Custom Knowledge Database
    if selected_CBK != '':
        try:
            #Load local vector index database
            local_db = FAISS.load_local(selected_CBK, embeddings)

            #Merge created vector index database with local one
            db0.merge_from(local_db)

            #Send system message
            chatWindow.config(state = NORMAL)
            chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
            chatWindow.insert(END, "Embeddings were successfully merged with existing Custom Knowledge Database (CKB).\n\n")
            chatWindow.config(state = DISABLED)

        except:
            #Send system message
            chatWindow.config(state = NORMAL)
            chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
            chatWindow.insert(END, "An error occurred: embeddings were not merged with existing Custom Knowledge Database (CKB).\n\n")
            chatWindow.config(state = DISABLED)

    #Save updated Custom Knowledge Database
    try:
        db_name = f"{current_time('year')}{current_time('month')}{current_time('day')}_{current_time('hour')}h{current_time('minute')}"
        db0.save_local(os.path.join(embeddings_relative_path, db_name))

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
                                   title = 'Select folder with an existing Custom Base Knowledge index (if available)'
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

    #Instantiate the embeddings model
    try:
        from langchain.embeddings import SentenceTransformerEmbeddings
        embeddings = SentenceTransformerEmbeddings(model_name = os.path.join(model_relative_path, "Embeddings"))

        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "Embeddings model ('all-MiniLM-L6-v2'') was successfully instantiated.\n\n")
        chatWindow.config(state = DISABLED)

    except:
        #Send system message
        chatWindow.config(state = NORMAL)
        chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
        chatWindow.insert(END, "An error occurred: embeddings model 'all-MiniLM-L6-v2' was not instantiated.\n\n")
        chatWindow.config(state = DISABLED)

    #Load Custom Base Knowledge
    try:
        #Load local vector index database
        from langchain.vectorstores.faiss import FAISS
        local_db = FAISS.load_local(selected_CBK, embeddings)

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
    messages = {"role": "user", "content": str(query)}
    chat_history.append(messages)

    if query != '' and query != None:
        try:
            #Search for what sentences fit better the question
            def similarity_search(query, index):
                # k is the number of similarity searched that matches the query
                # default is 4
                matched_docs = index.similarity_search(query, k = 5)
                sources = []
                for doc in matched_docs:
                    sources.append(
                        {
                            "page_content": doc.page_content,
                            "metadata": doc.metadata,
                        }
                    )
                return matched_docs, sources
            matched_docs, sources = similarity_search(query, local_db)

            #Creating the context
            context = "\n".join([doc.page_content for doc in matched_docs])

            #Create prompt with context
            from langchain import PromptTemplate
            prompt_template = """Use the following pieces of context delimited by triple backquotes to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
            ```{context}```
            Question: {question}
            Answer:"""

            PROMPT = PromptTemplate(template = prompt_template
                                    ,input_variables = ["context", "question"]
                                    ).partial(context = context)

            #Instantiate the model
            from langchain.llms import GPT4All as LG_GPT4All
            llm = LG_GPT4All(model = os.path.join(model_relative_path, model_name)
                             ,n_predict = max_tokens
                             ,n_ctx = context_window
                             ,top_k = top_k_value
                             ,top_p = top_p_value
                             ,temp = 0
                             ,repeat_penalty = repeat_penalty_value
                             ,repeat_last_n = repeat_last_n_value
                             ,n_batch = prompt_batch_size
                             ,verbose = False
                             ,streaming = False)

            #Instantiate the chain
            from langchain import LLMChain
            llm_chain = LLMChain(prompt = PROMPT
                                 ,llm = llm
                                 ,verbose = False)

            #Generate response
            answer = llm_chain.run(query)

            #Store AI's answer
            messages = {"role": "assistant", "content": answer}
            chat_history.append(messages)

            #Refresh chat history (end)
            refresh_chat_history(answer, 0)

            #Send system message with sources
            list_sources_full = []
            for i in sources:
                doc_content = i['page_content']
                doc_name = i['metadata']['source'].split('/')[-1]
                doc_page = i['metadata']['page'] + 1
                list_sources_full.append(f"'{doc_content}' [taken from {doc_name} (page {doc_page})]")
            list_sources_text = '\n\n'.join([text for text in list_sources_full])
            chatWindow.config(state = NORMAL)
            chatWindow.insert(END, f"{System_agent} [{current_time('hour')}:{current_time('minute')}]: ", "system")
            chatWindow.insert(END, f"The answer was based on the following sources, ordered from highest to lowest relevance:\n{list_sources_text}.\n\n")
            chatWindow.config(state = DISABLED)
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
    #answer = answer.replace("```", "\n```\n")
    return(answer)

def menubar_block(block = 1):
    if block == 1:
        file_menu.entryconfig('Save chat', state = "disabled")
        file_menu.entryconfig('Load chat', state = "disabled")
        file_menu.entryconfig('Clear chat', state = "disabled")
        file_menu.entryconfig('Exit', state = "disabled")
        tools_menu.entryconfig('Summarize', state = "disabled")
        tools_menu.entryconfig('Create CKB', state = "disabled")
        tools_menu.entryconfig('Use CKB', state = "disabled")
    else:
        file_menu.entryconfig('Save chat', state = "normal")
        file_menu.entryconfig('Load chat', state = "normal")
        file_menu.entryconfig('Clear chat', state = "normal")
        file_menu.entryconfig('Exit', state = "normal")
        tools_menu.entryconfig('Summarize', state = "normal")
        tools_menu.entryconfig('Create CKB', state = "normal")
        tools_menu.entryconfig('Use CKB', state = "normal")

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
tools_menu.add_command(label = 'Summarize'
                      ,command = handle_summarize)
tools_menu.add_command(label = 'Create CKB'
                      ,command = handle_create_CKB)
tools_menu.add_command(label = 'Use CKB'
                      ,command = handle_use_CKB)

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
