import base64
import json
from IPython.display import display, Image
import os
from together import Together

class diffusion: 
    def __init__(self, key=None, intel=None): 
        self.__key = "8069bcddb5b335ea3e2f23e9d58d83d5dfb270ee6ffcb8a546fbcdf8fb336dac" if key is None else key  
        self.__client = Together(api_key=self.__key) 
        
    def generateImage(self, prompt, steps=10): 
        response = self.__client.images.generate(
        prompt="space robots",
        model="stabilityai/stable-diffusion-xl-base-1.0",
        steps=steps,
        n=4,)
        base64_string = response.data[0].b64_json
        # Decode the Base64 string to get image bytes
        image_bytes = base64.b64decode(base64_string)
        # Display the image in the Jupyter notebook
        img = Image(data=image_bytes)
        return img 

