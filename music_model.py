#Bring in the model this will automatically download the weights
from audiocraft.models import musicgen
from audiocraft.utils.notebook import display_audio
import torch
import soundfile as sf
class musicModel:
import librosa
from pydub import AudioSegment
import io
from gtts import gTTS

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
        self.save_audio(res[0], "output.mp3")
        return res 
    def __display_audio(self, audio): 
        display_audio(audio, 32000)

    def generateVoice(self, lyrics):
      tts = gTTS(lyrics, lang='en')
      tts.save("voice.mp3")
      return tts

    def save_audio(self, res, filename):
        # Convert the result to a byte stream
        audio_buffer = io.BytesIO()
        audio_segment = AudioSegment(
            res.tobytes(), 
            frame_rate=22050,  # Use the correct sample rate for your model's output
            sample_width=res.dtype.itemsize, 
            channels=1  # Assuming mono channel
        )
        audio_segment.export(audio_buffer, format="mp3")
        
        # Save the byte stream to a file
        with open(filename, "wb") as f:
            f.write(audio_buffer.getbuffer())
    def extract_keynotes(self, audio):
        music_file = "output.mp3"
        y_music, sr_music = librosa.load(music_file, sr=None)

        #Extract melody using librosa's piptrack
        pitches, magnitudes = librosa.core.piptrack(y=y_music, sr=sr_music)

        # Extract the predominant melody
        melody = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:  # Ignore zero-pitch (no pitch detected)
                melody.append(pitch)
            else:
                melody.append(0)

        # Convert pitch to MIDI note numbers
        melody_midi = librosa.hz_to_midi(melody)
    def extract_keyPointsVoice(self, voice): 
        voice_file = "voice.mp3"
        y_voice, sr_voice = librosa.load(voice_file, sr=None)
        phoneme_segments = librosa.effects.split(y_voice, top_db=30)
        phonemes = [y_voice[start:end] for start, end in phoneme_segments]