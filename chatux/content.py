import streamlit as st
import os

def hydrate_ideas(category: str, ideas: dict):
    for file in os.listdir('ideas/' + category):
        if file.endswith('.txt'):
            with open('ideas/' + category + '/' + file, 'r') as f:
                ideas[file.replace('.txt', '')] = f.read()

def intro():
    st.markdown('### ChatGPT and generative AI models are about to transform every industry')

    st.video('walkthrough.webm')

    st.markdown('#### 💬&nbsp; ChatStart helps stay ahead of the curve in three easy steps')
    st.markdown('### 1. Select an idea')
    st.markdown('''**Start by selecting an idea for your app, startup, or business project.
    We will continue to add more ideas to the list covering industries, roles, and use cases.**''')
    st.image('ideate.png', width=350)

    st.markdown('### 2. Explore in chat')
    st.markdown('''> Once you have selected an idea, you can explore it in a custom chat powered by ChatGPT
    and other generative AI models. You can fine tune your chatbot by simply chatting with it.''')

    st.image('explore.png')

    st.markdown('### 3. Generate tutorial and code')
    st.markdown('''> Once satisfied with your chat exploration, you can hit `Generate Code` button. This will generate
    a custom tutorial for this idea and code for integrating ChatGPT with your app. Your entire chat exploration
    will be available to fine tune your chatbot.''')

    st.image('tutorial_code.png')

    st.markdown('---')

    st.markdown('## More Features')

    st.markdown('### Contextual Image Search')
    st.markdown('''> Integrate Google Image Search within your chat to discover images and links.
    You can use this for creating chat based visual search apps for shopping, education, etc.''')

    st.image('shopping.png')

    st.markdown('### Chain multiple models')
    st.markdown('''> Make your chat sessions super productive by chaining ChatGPT text 
    with DALL.E image generations.''')

    st.image('chaining.png')

    st.markdown('### Generate Python Dataframes')
    st.markdown('''> Integrate ChatStart generated code within your Python apps getting access to native constructs
    like Pandas DataFrames, JSON objects, data structures like lists and dictionaries directly from within
    a chat exploration.''')

    st.image('datasets.png')

    st.markdown('### Browse Media Inplace')
    st.markdown('''> Use chat to browse media, see images, watch related videos in place.''')

    st.image('media.png')

    st.markdown('### Query Data and Generate Charts Interactively')
    st.markdown('''> Use natural language to query world knowledge for generating custom datasets 
    and then visualize these datasets into charts and analytics, which can be modified using plain English.''')

    st.image('charts.png')

    st.markdown('### Simulate Expert Advisor')
    st.image('specialist.png')

    st.markdown('### Specialized Learning Tool')
    st.image('learning.png')

    st.markdown('### Visual Story Generation')
    st.image('story.png')    
