# Purpose of this program
Allow you to make use of Large Language Models (LLMs) for private and/or work related purposes. The only time this script ever requires Internet is at first launch, when it creates a folder to store all the models required to run properly. All models are downloaded from the Hugging Face website (https://huggingface.co/).

# Requirements
All of the requirements are listed at the start of the script, including the version on which the script was tested, namely:
* #!pip3 install torch==2.0.0+cu117
* #!pip install huggingface_hub==0.16.4
* #!pip install transformers==4.30.2
* #!pip install ctransformers==0.2.18
* #!pip install langchain==0.0.205
* #!pip install farm-haystack==1.19.0
* #!pip install clean-text==0.6.0
* #!pip install nltk==3.8.1
* #!pip install docx2txt==0.8
* #!pip install pypdf==3.11.0

# Chat Large Language Model (LLM)
The current model used is "TheBloke/WizardLM-Uncensored-Falcon-7B-GGML". This model should be able to perform in your work PC/laptop, and make use solely of your CPU. It is **highly recommended** that you clear the chat whenever you want to change topic of discussion to increase the speed of the model and also so it does not get confused with previous messages.

# Functions
* GUI based on Python's tkinter

<img src = "https://github.com/esuriddick/Programming/blob/main/Python/Local_LLM/Preview_UI_01.jpg"></img>
<img src = "https://github.com/esuriddick/Programming/blob/main/Python/Local_LLM/Preview_UI_02.jpg?raw=true"></img>
* Chat back and forth with the AI

Please bear in mind that the knowledge of any LLM is limited to the information it was trained on, meaning that it will not be aware of recent events.
* Save the chat to continue later or to recall the messages that were exchanged
* An audio cue is played when the AI answers to you.
* Provide a document in either .pdf, .docx or .txt to be summarized (in bullet points form), according to each document type the source document resembles the most (i.e., news article, book or report).
* Create and use your Custom Knowledge Base

First of all, you need to create your Custom Knowledge Base through the option _Create CKB_ under the tab _Tools_. Afterwards, you select a folder with all the files that you want to be used when using your CKB, and these files must be either in PDF, DOCX or TXT format. This will create a database to search for the answer that you are looking with the option _Use CKB_ under the tab _Tools_. Once you select this option (_Use CKB_), you must select the folder with the database that you created and you will get a separate prompt to insert your question. It will then perform a "Google search" across all the documents inside your CKB and return 5 passages deemed most relevant given your query in the chat.

# Disclaimer
As abovementioned, the model selected by default to chat with the user is uncensored. As mentioned in the original model's card: "An uncensored model has no guardrails. You are responsible for anything you do with the model, just as you are responsible for anything you do with any dangerous object such as a knife, gun, lighter, or car. Publishing anything this model generates is the same as publishing it yourself. You are responsible for the content you publish, and you cannot blame the model any more than you can blame the knife, gun, lighter, or car for what you do with it."
Moreover, I am not responsible for any damage, loss of data or other negative events that may occur as a result of using this software. I am only providing this code as a courtesy and convenience to those who may find it useful. The use of this code is entirely at your own risk.
