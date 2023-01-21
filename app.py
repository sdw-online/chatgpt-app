import openai
import os
from dotenv import load_dotenv
import logging 


# Set up root root_logger 
root_logger = logging.getLogger(__name__)
root_logger.setLevel(logging.DEBUG)


# Set up formatter for logs 
file_handler_log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s  ')
console_handler_log_formatter = logging.Formatter('%(message)s ')


# Set up file handler object for logging events to file
file_handler = logging.FileHandler('chatgpt_conversation_history.log', mode='w')
file_handler.setFormatter(file_handler_log_formatter)


# Set up console handler object for writing event logs to console in real time (i.e. streams events to stderr)
console_handler = logging.StreamHandler()
console_handler.setFormatter(console_handler_log_formatter)


# Add the file and console handlers 
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)



# Load API key from environment variables 
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')



# # Generate ChatGPT responses to console
def generate_chatgpt_responses(prompt):
    chatgpt_response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.3,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0,
    presence_penalty=0
)
    
    return chatgpt_response["choices"][0]["text"]


# Run ChatGPT 
while True:
    root_logger.debug('')
    user_input=input('::Me: ')
    root_logger.debug('--------------------------------------------------')

    root_logger.removeHandler(console_handler)
    root_logger.info(f'::Me: {user_input}' )
    root_logger.addHandler(console_handler)

    chatgpt_response = generate_chatgpt_responses(user_input)
    root_logger.info('::ChatGPT: ', chatgpt_response)
    root_logger.debug('--------------------------------------------------')