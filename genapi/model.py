import openai
import os

class OpenAI:
    """OpenAI wrapper."""
    default_model = 'text-davinci-003'
    openai.api_key = os.getenv('OPENAI_API_KEY')

    def __init__(self):
        self.current_model = self.default_model
        self.run_cost = 0
    
    def cost(self, tokens: int, part='', model=default_model) -> float:
        """Calculate cost of tokens."""
        model_pricing = {'text-davinci-003': 0.02, 'gpt-3.5-turbo': 0.002, 
                         'gpt-4-8k-prompt': 0.03, 'gpt-4-8k-completion': 0.06,
                         'gpt-4-32k-prompt': 0.06, 'gpt-4-32k-completion': 0.12}
        if part == '':
            return tokens/1000 * model_pricing[model]
        else:
            return tokens/1000 * model_pricing[model + '-' + part]

    def text(self, prompt: str, temperature=0.9, max_tokens=70, model=default_model, **kwargs):
        """OpenAI Text Completion API wrapper."""
        response = openai.Completion.create(
            model=model, 
            prompt=prompt, 
            temperature=temperature, 
            max_tokens=max_tokens, 
            **kwargs)
        return response

    def chat(self, messages, temperature=0.2, max_tokens=100, model='gpt-3.5-turbo', **kwargs):
        """OpenAI Chat Completion API wrapper."""
        response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs)
        return response
    
    