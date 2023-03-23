# 💬 ChatStart

ChatStart App for getting started with building your own chatbot reusing this code. You can also run this app on your laptop to create, ideate, explore, and download custom code snippets for chatbots you create using the app.

**💬 ChatStart App [www.promptx.ai/chatstart-app/](https://www.promptx.ai/chatstart-app/)**

[!['ChatStart Video Walkthorugh](media/video-thumb.png)](https://www.youtube.com/watch?v=kr1rX9wskG0)

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

## Contributing

We welcome contributions to this project. Please read our [contributing guidelines](CONTRIBUTING.md) for more information.

One of the easiest way to extend and contribute to this project is to add new ideas to the app. You can add new ideas by adding a TXT file under [ideas](https://github.com/promptxai/chatstart/tree/main/ideas) folder. The TXT file should contain the chatbot conversation flow like the following turn-by-turn format example. Just make sure that you add a unique unicode emoji at the beginning of the file name and choose the subfolder based on API used by the idea.

*File path: `ideas/open_ai/🍿 Movie Database.txt`*

``` txt
System: You are a Movie Database that responds with movies related information.
Provide information in a crisp single sentence.
User: What is the movie rating of The Matrix?
Assistant: The Matrix is rated 8.7/10 on IMDb.
User: What is the link of the official trailer?
```

## License

This project is licensed under the terms of the [MIT license](LICENSE).

## Credits

This project was bootstrapped with [Streamlit](https://www.streamlit.io/) and [OpenAI API](https://openai.com/).

## Authors

[Manav Sehgal](https://www.linkedin.com/in/manavsehgal/)