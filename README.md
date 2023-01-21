# I built my own ChatGPT app using Python…here's how

# Preface

- First of all, what is ChatGPT?

ChatGPT is a chatbot designed and trained by OpenAI. It is powered by OpenAI’s GPT-3 model (a language model that can perform a series of powerful text-based tasks like text translations, summarizations, writing code, among others).  

- Why create your own version?

 I got frustrated over the number of times I got thrown out of the web version due to large number of users accessing it simultaneously

# Libraries

Here are the Python modules I used in creating my own custom ChatGPT:

- **flask** - for building web apps
- **os** - for communicating with my machine’s operating system
- **openai** - for accessing OpenAI API via Python
- **dotenv** - for accessing the environment variables in my .env file
- **logging** - for recording data processing events and chat history with my ChatGPT bot

```python
from flask import Flask, request, render_template
import openai
import os
from dotenv import load_dotenv
import logging
```

# Steps

## A. Environment initiators

```python
# Set up your app environment 
app = Flask(__name__, template_folder='templates')
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
```

The **first line** above ****initiates the Flask app. The `__name__` variable is used to to determine whether the current script is the main program or coming from another module/location. It does this by checking the script’s root path. 

The **second and third lines** read the API key given to me by OpenAI from a secure file I saved it in (called `.env`). 

## B. Event loggers

```python
# Set up root root_logger 
root_logger = logging.getLogger(__name__)
root_logger.setLevel(logging.DEBUG)
```

I create an object for logging called `root_logger`, and I set the logging severity level to DEBUG, which will enable the `root_logger` to record logs of every security level (i.e. debug, info, warning, error and critical)

```python
# Set up formatters for logs 
file_handler_log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s  ')
console_handler_log_formatter = logging.Formatter('%(message)s ')
```

The **first and second lines** create objects responsible for recording the logs in a clean and consistent format. But there are distinct differences between the two: 

- Line 1 records logs into a file on the machine in a ‘**current timestamp - log severity level - message**’ format
- Line 2 streams logs onto the console in a user friendly format i.e. only prints the messages to the console

```python
# Set up file handler object for logging events to file
file_handler = logging.FileHandler('chatgpt_conversation_history.log', mode='w')
file_handler.setFormatter(file_handler_log_formatter)

# Set up console handler object for writing event logs to console in real time (i.e. streams events to stderr)
console_handler = logging.StreamHandler()
console_handler.setFormatter(console_handler_log_formatter)
```

The first two lines are focused on initiating the object that records logs to file. 

- Line 1 uses the `FileHandler` class to give the `file_handler` object the ability to write logs to a log file titled `chatgpt_conversation_history.log` . The mode is set to `w` to indicate the program is writing to a file.
- Line 2 sets the log formatter to `file_handler_log_formatter` object.

The last two lines are focused on initiating the object that writes the logs directly to the console.

- Line 1 uses the `StreamHandler` class to give the `console_handler` object the ability to stream the logs to the console.
- Line 2 sets the log formatter to `console_handler_log_formatter` object

```python
# Add the file and console handlers 
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)
```

These lines add the handlers developed earlier to my primary logger object called `root_logger`.  

- Line 1 adds the `file_handler` object to the `root_logger`.
- Line 2 adds the `console_handler` object to the `root_logger`.

## C. Web app

```python
@app.route('/')
def render_index_html():
    return render_template('index.html')
```

The `app.route` decorator points the user to the home page of the Flask app, which is where the chat-box currently lives. 

The `render_index_html` function displays the home page using the `index.html` page it finds in the `templates` folder we defined in the beginning via the `render_template` function.  

The `index.html` file in the `templates` folder is the skeleton of the web page. 

```python
@app.route('/chat', methods=['POST'])
def render_chat_with_chatgpt():
    user_input = request.form['text']
    root_logger.removeHandler(console_handler)
    root_logger.info(f':: Me (SDW):   {user_input}' )
    root_logger.addHandler(console_handler)
    chatgpt_response = openai.Completion.create(
        model="text-davinci-003",
        prompt=user_input,
        temperature=0.3,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0
    )
    root_logger.info(f':: ChatGPT: {chatgpt_response["choices"][0]["text"]}  ')
    root_logger.debug('--------------------------------------------------')
    return chatgpt_response["choices"][0]["text"]
```

I created the `render_chat_with_chatgpt` function under the `@app.route('/chat', methods=['POST'])` decorator to form a fluid conversation with ChatGPT.   

I set the `methods` argument to `‘POST’` because we only want the `‘chat'` route to respond to HTTP POST requests expressed as sent messages to the ChatGPT bot. When we send a message to the `‘chat'` route, it triggers the `render_chat_with_chatgpt` function to generate a dynamic response from OpenAI GPT-3’s database. 

- The first line inside `render_chat_with_chatgpt` function is the `user_input` variable, which is used to pull my input message through `request.form['text']`.
- The second, third and fourth lines is just a temporary workaround to write the user input prompt without duplicating it in the file logs
- The fifth line contains the `chatgpt_response` variable which holds ChatGPT’s responses in key-value pairs. It calls on the `openai.Completion.create()` function which holds a few useful parameters to making it work:
    - **model** is the GPT-3 model selected. I used `text-davinci-003` because it’s one of the best models for text-completion prompts
    - **prompt** is the input message or query you send to ChatGPT
    - **temperature** deals with the model’s randomness level in the responses it gives. The higher the temperature, the more random (but interesting) the responses are likely to be. The lower the temperature, the more consistent (and predictable) the responses become. So high temperatures give more unique responses, lower temperatures give safer and predictable responses
    - **max_tokens** is the maximum number of tokens (expressed in words) can be generated in a single response
    - **top_p** is used to pick words based on how common or uncommon they are to form sentences with. A **lower top_p** value means more uncommon words will be selected for generating sentences in the response, and a **higher top_p** value will use more common words
    - **frequency_penalty** is a value between -2.0 and 2.0 used to discourage using words appearing in the input prompt frequently, which promotes more verbose responses
    - **presence_penalty** is a value between -2.0 and 2.0 used to discourage re-using words already in the input prompts, which promotes more original responses

```python
root_logger.info(f':: ChatGPT: {chatgpt_response["choices"][0]["text"]}  ')
root_logger.debug('--------------------------------------------------')
return chatgpt_response["choices"][0]["text"]
```

ChatGPT’s response is extracted from the response payload, which is unnested from a nested dictionary and then printed into the Flask app’s frontend interface.   

## D. Loading app

```python
if __name__ == '__main__':
    app.run(debug=True)
```

Once all the previous steps in A-C are completed, we can run the app in a dev location. I can access the app using [http://localhost:5000/](http://localhost:5000/) in my browser once I run my script.

# Conclusion

This is just the starter-pack in getting my custom version of ChatGPT off the ground in the event of another system crash on the web’s preview version. There’s more work to add on the front-end and UX side that is currently on my to-do list. 

Understanding what tasks ChatGPT shines in will increase your productivity rate as an engineer. ChatGPT is a great co-pilot, but it’s still far from becoming a tool that replaces many developer jobs. But that’s a topic for another day. 

Here is the link to my GitHub page that contains the full repository for the code shared: