class Stability:
    def __init__(self):
        self.initialized = False # True if stability API is initialized
        self.api = None # Stabile Diffusion API object
        self.image = '' # Latest image url from stability API
        self.runs = 0 # Number of times stability API has been called

class OpenAI:
    def __init__(self):
        self.chatgpt_runs = 0 # Number of times OpenAI ChatGPT API has been called
        self.dalle_runs = 0 # Number of times OpenAI DALL.E API has been called
        self.image = '' # Latest image url from DALL.E API
        self.tokens = 0 # Number of tokens used by OpenAI API

class UX:
    def __init__(self):
        self.icon = '💬' # ChatStart active persona icon unicode
        self.sidebar = 'collapsed' # Sidebar state
        self.code = False # Show code

class User:
    def __init__(self):
        self.login = '' # User login email
        self.waitlisted = False # True if user is waitlisted
        self.authenticated = False # True if user is authenticated
        self.login_form = False # True if login form is shown

class Chat:
    def __init__(self):
        self.messages = [] # List of messages
        self.conversation = [] # Active conversation
        self.idea = '' # Active idea
        self.prompt = '' # Active prompt

class Google:        
    def __init__(self):
        self.runs = 0 # Number of times Google API has been called
        self.response = None # Google API response

class Content:
    def __init__(self):
        self.vegalite = None # Vega-Lite chart
        self.youtube = None # YouTube video
        self.dataframe = None # Pandas dataframe