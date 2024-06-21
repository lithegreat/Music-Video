#Bring in the model this will automatically download the weights 
from audiocraft.models import musicgen
from audiocraft.utils.notebook import display_audio
import torch
class musicModel: 
    def __init__(self, model_type: str, audio_length):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = musicgen.MusicGen.get_pretrained(model_type, device=self.device)
        self.audio_length = audio_length
        self.__set_audio_length()
    
    def __set_audio_length(self):
        self.model.set_generation_params(duration=self.audio_length)
    def generateAudio(self, instructions): 
        res = self.model.generate([
            instructions
        ], 
            progress=True)
        self.__display_audio(res)
    def __display_audio(audio): 
        display_audio(audio, 32000)