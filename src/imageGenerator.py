import base64
import json
from IPython.display import display, Image
import os
from PIL import Image as PILImage
from together import Together
import io

class diffusion: 
    def __init__(self, key=None, intel=None): 
        self.__key = "8069bcddb5b335ea3e2f23e9d58d83d5dfb270ee6ffcb8a546fbcdf8fb336dac" if key is None else key  
        self.__client = Together(api_key=self.__key) 
        
    def generateImage(self, prompt, steps=10, seed=0): 
        response = self.__client.images.generate(
        prompt=prompt,
        model="stabilityai/stable-diffusion-2-1",
        steps=steps,
        n=4,
        seed=seed)
        base64_string = response.data[0].b64_json
        # Decode the Base64 string to get image bytes
        image_bytes = io.BytesIO(base64.b64decode(base64_string))
        # Open image using Pillow
        img = PILImage.open(image_bytes)
        # Display the image in the Jupyter notebook
        return img

