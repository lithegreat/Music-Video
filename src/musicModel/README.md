# Audio Generation and Management Module

This Python module provides functions to interact with a backend service for generating and managing audio files based on provided prompts and other parameters.

## Requirements

- Python 3.x
- `requests` library

Install the required library using:
```sh
pip install requests
```

## Base URL Configuration

Replace the `base_url` with your Vercel domain:

```python
base_url = "http://localhost:3000"
```

## Functions

### `custom_generate_audio(payload)`

Sends a request to generate custom audio based on the provided payload.

- **Parameters:**
  - `payload` (dict): The data to send in the request body.

- **Returns:**
  - `response.json()` (dict): The JSON response from the server.

- **Example:**
  ```python
  data = custom_generate_audio({
      "prompt": "Your song lyrics here",
      "tags": "genre, mood",
      "title": "Song Title",
      "make_instrumental": False,
      "wait_audio": False,
  })
  ```

### `extend_audio(payload)`

Sends a request to extend existing audio based on the provided payload.

- **Parameters:**
  - `payload` (dict): The data to send in the request body.

- **Returns:**
  - `response.json()` (dict): The JSON response from the server.

- **Example:**
  ```python
  data = extend_audio({
      "audio_id": "existing_audio_id",
      "extension_params": {}
  })
  ```

### `generate_audio_by_prompt(payload)`

Sends a request to generate audio based on a text prompt.

- **Parameters:**
  - `payload` (dict): The data to send in the request body.

- **Returns:**
  - `response.json()` (dict): The JSON response from the server.

- **Example:**
  ```python
  data = generate_audio_by_prompt({
      "prompt": "Your song lyrics here",
      "tags": "genre, mood"
  })
  ```

### `get_audio_information(audio_ids)`

Fetches information about the specified audio IDs.

- **Parameters:**
  - `audio_ids` (str): Comma-separated string of audio IDs.

- **Returns:**
  - `response.json()` (dict): The JSON response from the server.

- **Example:**
  ```python
  data = get_audio_information("audio_id_1,audio_id_2")
  ```

### `get_quota_information()`

Fetches information about the current quota.

- **Returns:**
  - `response.json()` (dict): The JSON response from the server.

- **Example:**
  ```python
  quota_info = get_quota_information()
  ```

### `download_audio(url, directory, filename)`

Downloads audio from the specified URL to the given directory and filename.

- **Parameters:**
  - `url` (str): The URL to download the audio from.
  - `directory` (str): The directory to save the audio file.
  - `filename` (str): The name of the audio file.

- **Returns:**
  - `filepath` (str): The path to the downloaded audio file.

- **Example:**
  ```python
  filepath = download_audio("http://example.com/audio.mp3", "downloads", "audio.mp3")
  ```

## Usage Example

The following script demonstrates how to generate custom audio, check its status, and retrieve the audio URLs once available.

```python
if __name__ == "__main__":
    data = custom_generate_audio(
        {
            "prompt": "[Verse 1]\nCruel flames of war engulf this land\nBattlefields filled with death and dread\nInnocent souls in darkness, they rest\nMy heart trembles in this silent test\n\n[Verse 2]\nPeople weep for loved ones lost\nBattered bodies bear the cost\nSeeking peace and hope once known\nOur grief transforms to hearts of stone\n\n[Chorus]\nSilent battlegrounds, no birds' song\nShadows of war, where we don't belong\nMay flowers of peace bloom in this place\nLet's guard this precious dream with grace\n\n[Bridge]\nThrough the ashes, we will rise\nHand in hand, towards peaceful skies\nNo more sorrow, no more pain\nTogether, we'll break these chains\n\n[Chorus]\nSilent battlegrounds, no birds' song\nShadows of war, where we don't belong\nMay flowers of peace bloom in this place\nLet's guard this precious dream with grace\n\n[Outro]\nIn unity, our strength will grow\nA brighter future, we'll soon know\nFrom the ruins, hope will spring\nA new dawn, we'll together bring",
            "tags": "pop metal male melancholic",
            "title": "Silent Battlefield",
            "make_instrumental": False,
            "wait_audio": False,
        }
    )

    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"ids: {ids}")

    for _ in range(60):
        data = get_audio_information(ids)
        if data[0]["status"] == "streaming":
            print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
            print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
            break
        # sleep 5s
        time.sleep(5)

```
```markdown
# Music Model Class

This Python class provides functionalities to generate music and voice audio using a pre-trained model, as well as extract keynotes from the generated audio.

## Requirements

- Python 3.x
- `audiocraft` library
- `torch` library
- `soundfile` library
- `librosa` library
- `pydub` library
- `gTTS` library

Install the required libraries using:
```sh
pip install audiocraft torch soundfile librosa pydub gtts
```

## Class: `musicModel`

### `__init__(self, model_type: str, audio_length)`

Initializes the `musicModel` class.

- **Parameters:**
  - `model_type` (str): The type of the model to be used.
  - `audio_length` (int): The duration of the audio to be generated in seconds.

- **Example:**
  ```python
  music_model = musicModel(model_type="melody", audio_length=30)
  ```

### `__set_audio_length(self)`

Sets the audio length for the model's generation parameters. This is an internal method.

### `generateAudio(self, instructions)`

Generates audio based on the provided instructions.

- **Parameters:**
  - `instructions` (str): The instructions for generating the audio.

- **Returns:**
  - `res` (list): The generated audio.

- **Example:**
  ```python
  audio = music_model.generateAudio("Generate a calm and soothing melody.")
  ```

### `__display_audio(self, audio)`

Displays the generated audio in the notebook. This is an internal method.

### `generateVoice(self, lyrics)`

Generates a voice audio based on the provided lyrics using Google Text-to-Speech (gTTS).

- **Parameters:**
  - `lyrics` (str): The lyrics to be converted to voice.

- **Returns:**
  - `tts` (gTTS): The generated voice audio.

- **Example:**
  ```python
  voice = music_model.generateVoice("Hello, this is a generated voice.")
  ```

### `save_audio(self, res, filename)`

Saves the generated audio to a file.

- **Parameters:**
  - `res` (ndarray): The generated audio data.
  - `filename` (str): The name of the file to save the audio.

- **Example:**
  ```python
  music_model.save_audio(audio, "output.mp3")
  ```

### `extract_keynotes(self, audio)`

Extracts keynotes from the provided audio file.

- **Parameters:**
  - `audio` (str): The path to the audio file.

- **Example:**
  ```python
  music_model.extract_keynotes("output.mp3")
  ```

### `extract_keyPointsVoice(self, voice)`

Extracts key points from the provided voice file.

- **Parameters:**
  - `voice` (str): The path to the voice file.

- **Example:**
  ```python
  music_model.extract_keyPointsVoice("voice.mp3")
  ```

## Usage Example

The following script demonstrates how to initialize the `musicModel` class, generate audio and voice, save the audio, and extract keynotes from the audio.

```python
# Import the necessary libraries
from audiocraft.models import musicgen
from audiocraft.utils.notebook import display_audio
import torch
import soundfile as sf
import librosa
from pydub import AudioSegment
import io
from gtts import gTTS

# Define the musicModel class
class musicModel: 
    def __init__(self, model_type: str, audio_length):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = musicgen.MusicGen.get_pretrained(model_type, device=self.device)
        self.audio_length = audio_length
        self.__set_audio_length()

    def __set_audio_length(self):
        self.model.set_generation_params(duration=self.audio_length)
    
    def generateAudio(self, instructions): 
        res = self.model.generate([instructions], progress=True)
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
        audio_buffer = io.BytesIO()
        audio_segment = AudioSegment(
            res.tobytes(), 
            frame_rate=22050, 
            sample_width=res.dtype.itemsize, 
            channels=1  
        )
        audio_segment.export(audio_buffer, format="mp3")
        
        with open(filename, "wb") as f:
            f.write(audio_buffer.getbuffer())

    def extract_keynotes(self, audio):
        music_file = "output.mp3"
        y_music, sr_music = librosa.load(music_file, sr=None)
        pitches, magnitudes = librosa.core.piptrack(y=y_music, sr=sr_music)
        melody = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:  
                melody.append(pitch)
            else:
                melody.append(0)
        melody_midi = librosa.hz_to_midi(melody)
    
    def extract_keyPointsVoice(self, voice): 
        voice_file = "voice.mp3"
        y_voice, sr_voice = librosa.load(voice_file, sr=None)
        phoneme_segments = librosa.effects.split(y_voice, top_db=30)
        phonemes = [y_voice[start:end] for start, end in phoneme_segments]

# Initialize the musicModel
music_model = musicModel(model_type="melody", audio_length=30)

# Generate audio
audio = music_model.generateAudio("Generate a calm and soothing melody.")

# Generate voice
voice = music_model.generateVoice("Hello, this is a generated voice.")

# Save the generated audio
music_model.save_audio(audio[0], "output.mp3")

# Extract keynotes from the audio
music_model.extract_keynotes("output.mp3")

# Extract key points from the voice
music_model.extract_keyPointsVoice("voice.mp3")
```
```