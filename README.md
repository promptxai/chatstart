# 💬 ChatStart

ChatStart App for getting started with building your own chatbot reusing this code. You can also run this app on your laptop to create, ideate, explore, and download custom code snippets for chatbots you create using the app.

## How to install and run on your laptop

Clone the repo and follow the steps below to run the app on your laptop.

**Step 1:** Setup a Python virtual environment following [instructions here](https://www.promptx.ai/hugging-face/5-minutes-generative-ai-developer-setup/). 

Note: Make sure you are using Python version 3.10.0 for Stable Diffusion to work. You can use pyenv to manage multiple local versions of Python. Here is a [pyenv tutorial](https://realpython.com/intro-to-pyenv/) which might help.

**Step 2:** Install the dependencies using following command.

``` bash
pip install -r requirements.txt 
```

This will install OpenAI, Stable Diffusion, Google API Python Client, Pandas, and Streamlit.

**Step 3:** Signup for [OpenAI](https://platform.openai.com/signup) and [Stable Diffusion](https://platform.stability.ai/) API keys.

Store all your API keys as environment variables in your shell script.

``` bash
export OPENAI_API_KEY="<your key here>"
```

That's it now you can run your version of ChatStart on your laptop by typing the following command.

``` bash
streamlit run chat_start.py
```

**Step 4 (optional):** In case you are interested in integrating with Google APIs like Custom Search Engine API used by the Shopping Recommender Idea, you will need to signup for Google API credentials. Here is a [starting point](https://developers.google.com/custom-search) for integrating Programmable Search Engine via API.

Enjoy, create, and profit! Let us know when you launch :-)