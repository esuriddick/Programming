# Purpose of this program
Allow you to make use of Large Language Models (LLMs) for private and/or work related purposes. The only time this script ever requires Internet is at first launch, when it creates a folder to store all the models required to run properly. Other than the LLM itself, the other two models that it will download is a Tokenizer ("gpt2") and a sentence-transformers model ("all-MiniLM-L6-v2").

# Large Language Model
The script makes use of GPT4All ecosystem, meaning that you can make use of all of the models provided in their <a href = "https://gpt4all.io/index.html">page</a>. These models should be able to perform in your work PC/laptop, and they only make use of your CPU. By default, the model that the script uses is WizardLM-7B (trained by Microsoft and Peking University), but you can change the model that you want to use by changing the variable _model_name_.

Limitations of the model _per se_ cannot be surpassed by changing some of the parameters, such as _context_window_, but I have left it coded in the script in case one day it becomes useful.

# Functions
* GUI based on Python's tkinter

xxx
* Chat back and forth with the AI

Please bear in mind that the knowledge of the LLM is limited to the information it was trained on, meaning that it will not be aware of recent events.
* Save the chat to continue later or to recall the messages that were exchanged
* An audio cue is played when the AI answers to you.
* Provide a document in either .pdf, .docx or .txt to be summarized (in bullet points form).

I was unhappy with how slow Abstractive Text Summarization was and how sometimes the answer provided would be cut-off. Thus, by default, a summary is first created through an Extractive Text Summarization technique. Afterwards, this summary is provided to the LLM to perform Abstractive Text Summarization.

If you would like to only use Abstractive Text Summarization, you just have to change the variable _extractive_text_summarization_ to 0.
* Create and use your Custom Knowledge Base

You can feed it documents in .pdf, .docx or .txt format and then use the created databases to ask questions. Every time you want to resort to your Custom Knowledge Base, you have to select the option and you will get a separate prompt to insert your question. This limitation is due to the fact that we cannot feed the LLM with the whole document(s) at once, so it first performs a, let's say, "Google search" across your document(s) and the 5 most relevant results are provided to the LLM. The references used by the LLM are also provided to the user once an answer is given in the chat.

# Note of caution
Most LLMs as of today (05.07.2023) have a maximum limit of 2048 tokens when talking with them (i.e., considering both your messages and the ones from the model), meaning that, after a while, it will reach a point where the LLM is unable to generate a response, since it has reached its limit. Therefore, it is advised to clear the chat when changing subject. A smaller chat will also lead to faster responses by the LLM, since it has less inputs to consider when processing an answer.
