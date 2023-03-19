import openai
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import io
import warnings
from PIL import Image

class Stability:
    api = None
    """Stability wrapper."""
    def __init__(self, key: str):
        self.key = key
        self.api = self.init_stability_api(key)

    def init_stability_api(self, key):
        return client.StabilityInference(
            key=key, # API Key reference.
            verbose=True, # Print debug messages.
            engine="stable-diffusion-v1-5", # Set the engine to use for generation. 
            # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0 
            # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-inpainting-v1-0 stable-inpainting-512-v2-0
        )

    def generate_art_sd(self, prompt, size=512) -> Image:
        answers = self.api.generate(
            prompt=prompt,
            cfg_scale=8.0,
            width=size, # Generation width, defaults to 512 if not included.
            height=size, # Generation height, defaults to 512 if not included.
            sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
            # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
            # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, 
            # k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
        )

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


class OpenAI:
    """OpenAI wrapper."""
    def __init__(self, key: str):
        openai.api_key = key
    
    def cost(self, tokens: int, model='', part='') -> float:
        """Calculate cost of tokens."""
        model_pricing = {'text-davinci-003': 0.02, 'gpt-3.5-turbo': 0.002, 
                         'gpt-4-8k-prompt': 0.03, 'gpt-4-8k-completion': 0.06,
                         'gpt-4-32k-prompt': 0.06, 'gpt-4-32k-completion': 0.12}
        if part == '':
            return tokens/1000 * model_pricing[model]
        else:
            return tokens/1000 * model_pricing[model + '-' + part]

    def text(self, prompt: str, temperature=0.9, max_tokens=70, model='text-davinci-003', **kwargs):
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
    
    def image(self, prompt: str, size="1024x1024"):
        """OpenAI Image Completion API wrapper."""
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size
        )
        return response