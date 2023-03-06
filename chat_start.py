import streamlit as st
import openai
import pandas as pd
import json
import io
from google.cloud import firestore
import datetime
from google.oauth2 import service_account

# Setup session variables
state = st.session_state

if 'sidebar_state' not in st.session_state:
    state.sidebar_state = 'collapsed'

if 'authenticated_user' not in state:
    state.authenticated_user = False

if 'show_login' not in state:
    state.show_login = False

if 'login' not in state:
    state.login = ''

if 'waitlisted' not in state:
    state.waitlisted = False

if 'conversation' not in state:
    state.conversation = []

if 'selected_messages' not in state:
    state.selected_messages = []

if 'user_prompt' not in state:
    state.user_prompt = ''

if 'dataset_generated' not in state:
    state.dataset_generated = None

if 'dalle_image' not in state:
    state.dalle_image = ''

if 'icon' not in state:
    state.icon = '💬'

if 'messages' not in state:
    state.messages = []

if 'get_code' not in state:
    state.get_code = False

if 'selected_persona' not in state:
    state.selected_persona = ''

if 'vegalite_chart' not in state:
    state.vegalite_chart = ''

if 'state.youtube_trailer' not in state:
    state.youtube_trailer = ''

# Set page config
st.set_page_config(
    page_title="ChatStart - Ideate, explore, generate code for ChatGPT integration with your app",
    page_icon="chatstart_icon_32.png",
    layout="centered",
    initial_sidebar_state=state.sidebar_state)

# Setup personas
personas = {
"🎨 DALL.E Expert Artist":
'''System: You are a DALL.E Expert Artist who will ask the user questions about various 
features of art they want to create and then generate a prompt using 
DALL.E advanced features to get the best results.
User: I want to create an image of a futuristic city.
Assistant: Do you have a reference movie, style, or concept this is based on?
User: Yes, it is based on the movie Blade Runner.''',

"💻 Mac Terminal": 
'''System: You are a Mac Terminal. Based on natural language instructions respond
only in single line shell commands. If the command is not recognized, respond with "Command not found".
User: List files of current directory and copy to a text file called files_list.txt
Assistant: `ls > files_list.txt`
User: Parse paragraphs from https://en.wikipedia.org/wiki/Earth into a text file called earth.txt
''',        
    
"🍿 Movie Database": 
'''System: You are a Movie Database that responds with movies related information.
Provide information in a crisp single sentence.
User: What is the movie rating of The Matrix?
Assistant: The Matrix is rated 8.7/10 on IMDb.
User: What is the link of the official trailer?''',

"👩‍⚕️ Doctor": 
'''System: You are a Doctor who understands symptoms by asking follow up questions 
and when sufficient symptoms are known provides a diagnosis.
User: I have a headache.
Assistant: How long have you had a headache?
User: For a week.
Assistant: Do you have blurred vision?
User: No, but I have a fever.''',

"💊 Pharmacist": 
'''System: You are a Pharmacist who provides information about medicines, their usual dosage, 
side effects, and interactions. Provide information in a crisp single sentence.
User: What is the usual dosage of paracetamol?
Assistant: The usual dosage of paracetamol is 1-2 tablets every 4-6 hours.
User: What are the side effects of paracetamol?''',

"🎨 Stable Diffusion Pro Creator":
'''System: You are a Stable Diffusion Pro Creator who will ask the user questions about various 
features of image they want to create and then generate a prompt using 
Stable Diffusion advanced prompt engineering features to get the best results.
User: I want to create an image for my blog post.
Assistant: What is the blog post about?
User: It is about using physics to create innovative art for a city.''',

"📊 Vegalite Chart Generator":
'''System: You are a Vegalite Chart Generator that can also generate datasets to use in the chart.
You ask the user a few questions about the data they want to visualize, type of chart,
style, and other options. Then generate a vegalite chart code based on the instructions.
User: Create a chart.
Assistant: What data source should I use?
User: Create a list of 10 most populous cities in the world.''',

"🗂️ Dataset Generator":
'''System: You are a Dataset Generator. Create a code fenced csv based on user instructions.
User: Create a dataset of tallest buildings in the world.'''
}

def generate_code():
    st.markdown('### Add {idea} to your app'.format(idea = state.selected_persona))
    st.markdown('**Step 1:**' + ' ' + 'Use the following code for ChatGPT API call.')
    st.markdown(
        '''```python
import openai

openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= # Step 2: Copy the messages list here
        max_tokens=100,
        temperature=0.2,)
)
        ''')
    st.markdown('**Step 2:**' + ' ' + 'Copy the following messages list and assign to `messages` variable.')
    st.code(state.messages)

if not state.waitlisted and not state.show_login and not state.authenticated_user:
    with st.sidebar.form('waitlist_form'):
        st.markdown('### Waitlist for ChatStart')
        email = st.text_input("Email")
        submit_button = st.form_submit_button(label="Apply")

        if submit_button:
            key_dict = json.loads(st.secrets["textkey"])
            creds = service_account.Credentials.from_service_account_info(key_dict)
            db = firestore.Client(credentials=creds, project="chatstart-aa174")
            doc_ref = db.collection("waitlist").document(email)
            doc = doc_ref.get()
            if doc.exists:
                st.sidebar.error("Email already in waitlist")
            else:
                doc_ref.set({
                    'timestamp': datetime.datetime.now()
                })
                state.waitlisted = True
                st.sidebar.success("You have been added to the waitlist. We will notify you when you can use ChatStart.")

def login():
    state.show_login = True

if not state.authenticated_user and not state.show_login:
    st.sidebar.button('Login', on_click=login)

if not state.authenticated_user and state.show_login:
    with st.sidebar.form(key="login_form"):
        login = st.text_input("Login")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Login")

        if submit_button:
            key_dict = json.loads(st.secrets["textkey"])
            creds = service_account.Credentials.from_service_account_info(key_dict)
            db = firestore.Client(credentials=creds, project="chatstart-aa174")
            doc_ref = db.collection("users").document(login)
            doc = doc_ref.get()
            if doc.exists:
                if doc.to_dict()['password'] == password:
                    state.authenticated_user = True
                    state.login = login
                    state.show_login = False
                    st.sidebar.success("Login successful")
                else:
                    st.sidebar.error("Incorrect password")
            else:
                st.sidebar.error("User does not exist")

st.sidebar.markdown("### 💡 Select Idea")
# create a form to collect user input
with st.sidebar.form(key="role_form"):
    # add a text field to the form
    state.selected_persona = st.selectbox("Start typing to search or select", personas.keys())
    # add a submit button to the form
    submit_button = st.form_submit_button(label="Explore Chat", disabled=not state.authenticated_user)

    # if the form is submitted
    if submit_button:
        # set the conversation to the selected persona after removing the last line and joining the lines with new line
        state.conversation = '\n'.join(personas[state.selected_persona].splitlines()[:-1])
        # set the last line in personas as the user prompt
        state.user_prompt = personas[state.selected_persona].splitlines()[-1].replace('User: ', '')
        state.get_code = False

nav1, nav2 = st.columns([7, 1])
with nav1:
    st.write('Please waitlist for 💬&nbsp; ChatStart to enable featues.')
with nav2:
    if st.button('Waitlist'):
        state.sidebar_state = 'expanded'
        st.experimental_rerun()

st.markdown("## 💬&nbsp; ChatStart | " + state.selected_persona if state.conversation else "## 💬&nbsp; ChatStart")

st.markdown("**Ideate, explore, generate code for ChatGPT integration with your app**")

if not state.conversation:
    st.markdown('### ChatGPT and generative AI models are about to transform almost every industry')
    st.markdown('#### 💬&nbsp; ChatStart helps stay ahead of the curve in three easy steps')
    st.markdown('### 1. Select an idea')
    st.success('''Start by selecting an idea for your app, startup, or business project.
    We will continue to add more ideas to the list covering industries, roles, and use cases.
    &nbsp;💬&nbsp; ChatStart Premium users can also save their own ideas privately or share with others.''')
    st.image('ideate.png', width=350)
    
    st.markdown('### 2. Explore in chat')
    st.info('''Once you have selected an idea, you can explore it in a custom chat powered by ChatGPT
    and other generative AI models. You can fine tune your chatbot by simply chatting with it.
    &nbsp;💬&nbsp; ChatStart Premium users can also save their chat explorations privately or share with others.''')

    st.image('explore.png')

    st.markdown('### 3. Generate tutorial and code')
    st.warning('''Once satisfied with your chat exploration, you can hit `Generate Code` button. This will generate
    a custom tutorial for this idea and code for integrating ChatGPT with your app. Your entire chat exploration
    will be available to fine tune your chatbot.
    &nbsp;💬&nbsp; ChatStart Premium users can also get access to advanced code and tutorials to integrated
    with multiple APIs and models.''')

    st.image('tutorial_code.png')

    st.markdown('---')

    st.markdown('## More Features')

    st.markdown('### Chain multiple models')
    st.info('''Make your chat sessions super productive by chaining ChatGPT text with DALL.E image generations.
    &nbsp;💬&nbsp; ChatStart Premium users can also get access to advanced code and tutorials to integrated
    with multiple APIs and models.''')

    st.image('chaining.png')

    st.markdown('### Generate Python Dataframes')
    st.success('''Integrate ChatStart generated code within your Python apps getting access to native constructs
    like Pandas DataFrames, JSON objects, data structures like lists and dictionaries directly from within
    a chat exploration.
    &nbsp;💬&nbsp; ChatStart Premium users can also save these native objects and get access to advanced code
    and tutorials to perform improved integrations.''')

    st.image('datasets.png')

    st.markdown('### Browse Media Inplace')
    st.image('media.png')

    st.markdown('### Query Data and Generate Charts Interactively')
    st.image('charts.png')

    st.markdown('### Simulate Expert Advisor')
    st.image('specialist.png')

    st.markdown('### Specialized Learning Tool')
    st.image('learning.png')

if state.conversation:
    # get icon from the persona name
    state.icon = state.selected_persona.split()[0]
    st.markdown(state.conversation
                .replace('System:', '⚙️ &nbsp;&nbsp;')
                .replace('User:', '\n👤 &nbsp;&nbsp;')
                .replace('Assistant:', '\n' + state.icon + ' &nbsp;&nbsp;'))
    # if state.conversation contains DALL.E prompt in a code fenced block, then use the prompt to generate a new image
    if '"' in state.conversation and 'DALL.E Expert Artist' in state.selected_persona:
        num_quotes = state.conversation.count('"')
        prompt = state.conversation.split('"')[num_quotes - 1]
        # generate image from prompt
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        generated_image = response['data'][0]['url']
        st.image(generated_image, caption='DALL.E Generated Image')
        state.dalle_image = generated_image

    if 'Dataset Generator' in state.selected_persona and '```' in state.conversation:
        num_csv = state.conversation.count('```')
        dataset_csv = state.conversation.split('```')[num_csv - 1]
        csv_source = io.StringIO(dataset_csv)
        df = pd.read_table(csv_source, sep=",", index_col=1, skipinitialspace=True)
        state.dataset_generated = df
        st.dataframe(state.dataset_generated)
    
    if 'Vegalite Chart Generator' in state.selected_persona and '$schema' in state.conversation:
        # capture the chart json from second code fenced block
        # and assign it to state.vegalite_chart
        num_jsons = state.conversation.count('```')
        chart_json = state.conversation.split('```')[num_jsons - 1]
        state.vegalite_chart = json.loads(chart_json.replace('vega-lite {', '{'))
        redundant_instruction = state.conversation.find('You can copy and paste this code into a Vega-Lite editor')
        if redundant_instruction != -1:
            state.conversation = state.conversation[:redundant_instruction]
        st.vega_lite_chart(state.vegalite_chart)

    if 'youtube.com' in state.conversation:
        # create a list of youtube links
        youtube_links = [link for link in state.conversation.split() if 'youtube.com' in link]
        youtube_url = youtube_links[-1]
        st.video(youtube_url)        
        state.youtube_trailer = youtube_url

if state.conversation:
    with st.form(key="chat_form"):
        c1, c2 = st.columns([9, 1])
        with c1:
            user_input = st.text_area("👤 &nbsp;&nbsp;Your message here", value=state.user_prompt)
        with c2:
            st.caption('Discuss')
            submit_button = st.form_submit_button(label=state.icon)
        if submit_button:
            state.conversation += '\nUser: ' + user_input
            state.user_prompt = ''
            # parse the state.conversation into messages list considering multi-line User, System, and Assistant messages.
            # If new line does not have a role, it is considered as continuation of current line.
            state.messages = []
            for line in state.conversation.splitlines():
                if line.startswith('User:'):
                    state.messages.append({"role": "user", "content": line[5:]})
                elif line.startswith('System:'):
                    state.messages.append({"role": "system", "content": line[7:]})
                elif line.startswith('Assistant:'):
                    state.messages.append({"role": "assistant", "content": line[10:]})
                else:
                    state.messages[-1]["content"] += '\n' + line
            
            # call openai api
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                messages=state.messages,
                max_tokens=500,
                temperature=0)        
            # append the response to the conversation
            state.conversation += '\n' + 'Assistant: ' + response.choices[0].message.content
            # force render the page
            state.get_code = True
            st.experimental_rerun()

if state.get_code:
    st.sidebar.markdown("### 🪄 Get code")
    st.sidebar.button('Generate tutorial with code', on_click=generate_code)
