class Stability:
    def __init__(self):
        self.key = '' # Stability API key
        self.initialized = False # True if stability API is initialized
        self.api = None # Stabile Diffusion API object
        self.image = '' # Latest image url from stability API
        self.runs = 0 # Number of times stability API has been called

class OpenAI:
    def __init__(self):
        self.key = '' # OpenAI API key
        self.chatgpt_runs = 0 # Number of times OpenAI ChatGPT API has been called
        self.dalle_runs = 0 # Number of times OpenAI DALL.E API has been called
        self.image = '' # Latest image url from DALL.E API
        self.tokens = 0 # Number of tokens used by OpenAI API
        self.model = 'gpt-3.5-turbo' # OpenAI model

class UX:
    def __init__(self):
        self.icon = '💬' # ChatStart active persona icon unicode
        self.sidebar = 'expanded' # Sidebar state
        self.code = False # Show code
        self.keys_saved = False # True if API keys have been saved

class Chat:
    def __init__(self):
        self.messages = [] # List of messages
        self.conversation = [] # Active conversation
        self.idea = '' # Active idea
        self.prompt = '' # Active prompt

class Google:        
    def __init__(self):
        self.key = '' # Google API key
        self.runs = 0 # Number of times Google API has been called
        self.response = None # Google API response

class Content:
    def __init__(self):
        self.vegalite = None # Vega-Lite chart
        self.youtube = None # YouTube video
        self.dataframe = None # Pandas dataframe