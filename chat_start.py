import streamlit as st
import openai
import pandas as pd
import json
import io
import datetime
import os
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from googleapiclient.discovery import build

from chatux import session, content

# Setup session variables
state = st.session_state

# Integrations with LLMs, APIs, and Content sources
if 'stability' not in state:
    state.stability = session.Stability()
if 'open_ai' not in state:
    state.open_ai = session.OpenAI()
if 'google' not in state:
    state.google = session.Google()
if 'content' not in state:
    state.content = session.Content()

# User Experience
if 'ux' not in state:
    state.ux = session.UX()
if 'chat' not in state:
    state.chat = session.Chat()

# Set page config
st.set_page_config(
    page_title="ChatStart - Create, explore, generate code for a Chatbot. Fast!",
    page_icon="chatstart_icon_32.png",
    layout="centered",
    initial_sidebar_state=state.ux.sidebar)

# Setup API keys from environment variables or session state
GOOGLE_DEVELOPER_KEY = os.environ.get('GOOGLE_DEVELOPER_KEY', state.google.key)
openai.api_key = os.environ.get('OPENAI_API_KEY', state.open_ai.key)
STABILITY_KEY = os.environ.get('STABILITY_KEY', state.stability.key)
STABILITY_HOST='grpc.stability.ai:443'

if openai.api_key:
    state.ux.keys_saved = True

# Hydrate ideas
open_ai_ideas = {}
content.hydrate_ideas(category='open_ai', ideas=open_ai_ideas)

sd_ideas = {}
content.hydrate_ideas(category='sd', ideas=sd_ideas)

google_ideas = {}
content.hydrate_ideas(category='google', ideas=google_ideas)

ideas = open_ai_ideas | sd_ideas if STABILITY_KEY else open_ai_ideas
ideas = ideas | google_ideas if GOOGLE_DEVELOPER_KEY else ideas

def init_stability_api():
    state.stability.api = client.StabilityInference(
        key=STABILITY_KEY, # API Key reference.
        verbose=True, # Print debug messages.
        engine="stable-diffusion-v1-5", # Set the engine to use for generation. 
        # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0 
        # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-inpainting-v1-0 stable-inpainting-512-v2-0
    )
    state.stability.initialized = True

def generate_art_sd(prompt, size=512) -> Image:
    if state.stability.initialized is False:
        init_stability_api()

    answers = state.stability.api.generate(
        prompt=prompt,
        cfg_scale=8.0,
        width=size, # Generation width, defaults to 512 if not included.
        height=size, # Generation height, defaults to 512 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
        # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
        # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, 
        # k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
    )

    state.stability.runs += 1

    # Set up our warning to print to the console if the adult content classifier is tripped.
    # If adult content classifier is not tripped, save generated images.
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                return img


def generate_code():
    st.markdown('### Add {idea} to your app'.format(idea = state.chat.idea))
    st.markdown('**Step 1:**' + ' ' + 'Use the following code for ChatGPT API call.')
    st.markdown(
        '''```python
import openai

openai.ChatCompletion.create(
        model="{model}",
        messages= # Step 2: Copy the messages list here
        max_tokens=100,
        temperature=0.2,)
)
        '''.format(model=state.open_ai.model))
    st.markdown('**Step 2:**' + ' ' + 'Copy the following messages list and assign to `messages` variable.')
    st.code(state.chat.messages)

st.sidebar.markdown("### 💡 Select Idea")
# create a form to collect user input
with st.sidebar.form(key="idea_form"):
    # add a text field to the form
    state.chat.idea = st.selectbox("Type or scroll", ideas.keys())
    # add a submit button to the form
    submit_button = st.form_submit_button(label="Explore Chat", disabled=state.ux.keys_saved is False)

    # if the form is submitted
    if submit_button:
        # set the conversation to the selected idea after removing the last line and joining the lines with new line
        state.chat.conversation = '\n'.join(ideas[state.chat.idea].splitlines()[:-1])
        # set the last line in ideas as the user prompt
        state.chat.prompt = ideas[state.chat.idea].splitlines()[-1].replace('User: ', '')
        state.ux.code = False

st.sidebar.markdown("### 🧠 Change Model")

with st.sidebar.form(key="model_form"):
    state.open_ai.model = st.selectbox("OpenAI Model", 
        options=['gpt-3.5-turbo', 'gpt-4', 'gpt-4-32k'])
    submit_button = st.form_submit_button(label="Change Model", disabled=state.ux.keys_saved is False)

    if submit_button:
        st.experimental_rerun()

st.sidebar.markdown('### 🔒 User Account')
if state.ux.keys_saved is False:
    with st.sidebar.form(key="key_form"):
        state.open_ai.key = st.text_input("OpenAI Key (Required)", 
            value=state.open_ai.key, type="password", 
            help="Get your required OpenAI Key from [here](https://beta.openai.com/account/api-keys).")
        state.google.key = st.text_input("Google Key", 
            value=state.google.key, type="password", 
            help="Get your optional Google Key from [here](https://console.cloud.google.com/apis/credentials).")
        state.stability.key = st.text_input("Stability Key", 
            value=state.stability.key, type="password",
            help="Get your optional Stability Key from [here](https://beta.dreamstudio.ai/membership?tab=apiKeys).")
        submit_keys = st.form_submit_button(label="Activate Session")
        if submit_keys:
            if state.open_ai.key == '':
                st.sidebar.error('OpenAI Key is required.')
            else:
                state.ux.keys_saved = True
                st.experimental_rerun()

if state.ux.keys_saved is True:
    st.sidebar.markdown('**OpenAI Model:** ' + state.open_ai.model)
    st.sidebar.markdown('**ChatGPT Tokens Used:** ' + str(state.open_ai.tokens))
    st.sidebar.markdown('**ChatGPT Runs:** ' + str(state.open_ai.chatgpt_runs))
    st.sidebar.markdown('**Stability Runs:** ' + str(state.stability.runs))
    st.sidebar.markdown('**DALL.E Runs:** ' + str(state.open_ai.dalle_runs))
    st.sidebar.markdown('**Google API Runs:** ' + str(state.google.runs))

logo_nav1, logo_nav2 = st.columns([3, 5])
with logo_nav1:
    st.image('chatstart_logo_wide_w250.png', width=250)
with logo_nav2:
    st.markdown("#### " + state.chat.idea if state.chat.conversation else "")

st.markdown("**Create, Explore, and Generate Chatbots. Fast!**")

if not state.chat.conversation:
    content.intro()

if state.chat.conversation:
    # get icon from the idea name
    state.ux.icon = state.chat.idea.split()[0]
    st.markdown(state.chat.conversation
                .replace('System:', '⚙️ &nbsp;&nbsp;')
                .replace('User:', '\n👤 &nbsp;&nbsp;')
                .replace('Assistant:', '\n' + state.ux.icon + ' &nbsp;&nbsp;'))
    # if state.chat.conversation contains DALL.E prompt in a code fenced block, then use the prompt to generate a new image
    if '"' in state.chat.conversation and 'DALL.E Expert Artist' in state.chat.idea:
        num_quotes = state.chat.conversation.count('"')
        prompt = state.chat.conversation.split('"')[num_quotes - 1]
        # generate image from prompt
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        state.open_ai.dalle_runs += 1

        generated_image = response['data'][0]['url']
        st.image(generated_image, caption='DALL.E Generated Image')
        state.dalle_image = generated_image
    if '"' in state.chat.conversation and 'Shopping Recommender' in state.chat.idea:
        num_quotes = state.chat.conversation.count('"')
        search_query = state.chat.conversation.split('"')[num_quotes - 1]
        
        service = build("customsearch", "v1", developerKey=GOOGLE_DEVELOPER_KEY)

        res = (service.cse().list(
                    q=search_query,
                    cx="a65812bec92ed4b8c",
                    num=3,
                    searchType="image",
                    filter="1",
                    safe="active",
                ).execute())
        
        state.google.runs += 1

        ci1, ci2, ci3 = st.columns(3)
        with ci1:
            thumbnail = res["items"][0]["image"]["thumbnailLink"]
            link = res["items"][0]["image"]["contextLink"]
            domain = link.split('/')[2]
            st.markdown('[![]({thumbnail})]({link})'.format(thumbnail=thumbnail, link=link))
            st.markdown('[{domain}]({link})'.format(domain=domain, link=link))
        with ci2:
            thumbnail = res["items"][1]["image"]["thumbnailLink"]
            link = res["items"][1]["image"]["contextLink"]
            domain = link.split('/')[2]
            st.markdown('[![]({thumbnail})]({link})'.format(thumbnail=thumbnail, link=link))
            st.markdown('[{domain}]({link})'.format(domain=domain, link=link))
        with ci3:
            thumbnail = res["items"][2]["image"]["thumbnailLink"]
            link = res["items"][2]["image"]["contextLink"]
            domain = link.split('/')[2]
            st.markdown('[![]({thumbnail})]({link})'.format(thumbnail=thumbnail, link=link))
            st.markdown('[{domain}]({link})'.format(domain=domain, link=link))


    if '"' in state.chat.conversation and 'Stable Diffusion Story Generator' in state.chat.idea:
        num_quotes = state.chat.conversation.count('"')
        prompt = state.chat.conversation.split('"')[num_quotes - 1]
        generated_image = generate_art_sd(prompt)
        st.image(generated_image, caption='Stable Diffusion Generated Image')
        state.stability.image = generated_image

    if 'Dataset Generator' in state.chat.idea and '```' in state.chat.conversation:
        num_csv = state.chat.conversation.count('```')
        dataset_csv = state.chat.conversation.split('```')[num_csv - 1]
        csv_source = io.StringIO(dataset_csv)
        df = pd.read_table(csv_source, sep=",", index_col=1, skipinitialspace=True)
        state.content.dataframe = df
        st.dataframe(state.content.dataframe)
    
    if 'Vegalite Chart Generator' in state.chat.idea and '$schema' in state.chat.conversation:
        # capture the chart json from second code fenced block
        # and assign it to state.content.vegalite
        num_jsons = state.chat.conversation.count('```')
        chart_json = state.chat.conversation.split('```')[num_jsons - 1]
        state.content.vegalite = json.loads(chart_json.replace('vega-lite {', '{'))
        redundant_instruction = state.chat.conversation.find('You can copy and paste this code into a Vega-Lite editor')
        if redundant_instruction != -1:
            state.chat.conversation = state.chat.conversation[:redundant_instruction]
        st.vega_lite_chart(state.content.vegalite)

    if 'youtube.com' in state.chat.conversation:
        # create a list of youtube links
        youtube_links = [link for link in state.chat.conversation.split() if 'youtube.com' in link]
        youtube_url = youtube_links[-1]
        st.video(youtube_url)        
        state.content.youtube = youtube_url

if state.chat.conversation:
    with st.form(key="chat_form"):
        c1, c2 = st.columns([9, 1])
        with c1:
            user_input = st.text_area("👤 &nbsp;&nbsp;Your message here", value=state.chat.prompt)
        with c2:
            st.caption('Discuss')
            submit_button = st.form_submit_button(label=state.ux.icon)
        if submit_button:
            state.chat.conversation += '\nUser: ' + user_input
            state.chat.prompt = ''
            # parse the state.chat.conversation into messages list considering multi-line User, System, and Assistant messages.
            # If new line does not have a role, it is considered as continuation of current line.
            state.chat.messages = []
            for line in state.chat.conversation.splitlines():
                if line.startswith('User:'):
                    state.chat.messages.append({"role": "user", "content": line[5:]})
                elif line.startswith('System:'):
                    state.chat.messages.append({"role": "system", "content": line[7:]})
                elif line.startswith('Assistant:'):
                    state.chat.messages.append({"role": "assistant", "content": line[10:]})
                else:
                    state.chat.messages[-1]["content"] += '\n' + line
            
            # call openai api
            response = openai.ChatCompletion.create(
                model=state.open_ai.model,
                messages=state.chat.messages,
                max_tokens=500,
                temperature=0)

            state.open_ai.chatgpt_runs += 1
            state.open_ai.tokens += response.usage.total_tokens
            # append the response to the conversation
            state.chat.conversation += '\n' + 'Assistant: ' + response.choices[0].message.content
            # force render the page
            state.ux.code = True
            st.experimental_rerun()

if state.ux.code:
    st.sidebar.markdown("### 🪄 Get code")
    st.sidebar.button('Generate tutorial with code', on_click=generate_code)
