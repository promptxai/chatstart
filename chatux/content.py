import streamlit as st
import os
import yaml

def hydrate_parameters():
    with open('data/parameters.yaml', 'r') as file:
        parameters = yaml.safe_load(file)
        return parameters

def hydrate_ideas(category: str, ideas: dict):
    for file in os.listdir('ideas/' + category):
        if file.endswith('.txt'):
            with open('ideas/' + category + '/' + file, 'r') as f:
                ideas[file.replace('.txt', '')] = f.read()

def intro():
    st.markdown('### Simplest Conversation Design')
    st.markdown('**Just Text. Natural. Easy.**')
    st.image('media/text-design.png')

    st.markdown('### Instant Custom Chatbot')
    st.markdown('**Explore OpenAI. ChatGPT 4. DALL.E 2.**')

    st.image('media/chatbot.png')

    st.markdown('### Generate Code')
    st.markdown('**Python. Pandas DataFrames. JSON. Charts.**')

    st.image('media/tutorial_code.png')
    
    st.video('media/walkthrough.webm')

    st.markdown('<br/><br/>', unsafe_allow_html=True)

    logo_nav1, logo_nav2 = st.columns([3, 5])
    with logo_nav1:
        st.image('media/chatstart_logo_wide_w250.png', width=250)
    with logo_nav2:
        st.markdown("### Makes It Awesome")

    st.markdown('<br/><br/>', unsafe_allow_html=True)

    st.markdown('### Contextual Image Search')
    st.markdown('''**Integrate Google Image Search within your chat to discover images and links.
    You can use this for creating chat based visual search apps for shopping, education, etc.**''')

    st.image('media/shopping.png')

    st.markdown('### Chain multiple models')
    st.markdown('''**Make your chat sessions super productive by chaining ChatGPT text 
    with DALL.E image generations.**''')

    st.image('media/chaining.png')

    st.markdown('### Generate Python Dataframes')
    st.markdown('''**Integrate ChatStart generated code within your Python apps getting access to native constructs
    like Pandas DataFrames, JSON objects, data structures like lists and dictionaries directly from within
    a chat exploration.**''')

    st.image('media/datasets.png')

    st.markdown('### Browse Media Inplace')
    st.markdown('''**Use chat to browse media, see images, watch related videos in place.**''')

    st.image('media/media.png')

    st.markdown('### Query Data and Generate Charts Interactively')
    st.markdown('''**Use natural language to query world knowledge, create datasets, visualize these as charts, 
    and then customize and manipulate these to run analytics inside a chat UX.**''')

    st.image('media/charts.png')

    st.markdown('### Simulate Expert Advisor')
    st.markdown('''**You can build assistants for specialized functions like Doctors 
    to help them scale their presence during busy time.***''')
    st.image('media/specialist.png')

    st.markdown('### Specialized Learning Tool')
    st.markdown('''**Build a chat to query a specialized knowledge base like medicine and pharmacy information.**''')
    st.image('media/learning.png')

    st.markdown('### Visual Story Generation')
    st.markdown('''**Imagine an interactive story generator for kids where story progresses with each message 
    and generates visual imagery to match. New story every time!**''')
    st.image('media/story.png')    
