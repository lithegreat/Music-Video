import os
from together import Together
import re 
class LLM: 
    def __init__(self, topic, key=None, intel=None): 
        os.environ['TOGETHER_API_KEY'] =  "8069bcddb5b335ea3e2f23e9d58d83d5dfb270ee6ffcb8a546fbcdf8fb336dac" if key is None else key 
        self.intel = "You are one of the best song writers in the world.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02" if intel is None else intel
        self.__lyric_prompt =  """Create a set of song lyrics of the topic {topic} that demonstrate your vocal abilities and emotional expression. 
                                The lyrics should be accompanied by a professional-level audio recording with clear enunciation and crystal-clear audio quality. 
                                The song should feature a captivating melody and sophisticated arrangement, production, and performance. 
                                The lyrics must rhyme to enhance the song's flow and aesthetic appeal. You are encouraged to explore various themes and musical styles, 
                                but the final composition must meet the above criteria to showcase your talent and depth as a creator and performer. 
                                The lyrics should convey emotional expression and physical actions to ensure a high-quality performance."""
        
        self.__story_prompt = """As a story writer, your task is to create a short story based on a given song lyric snippet. Each story should be detailed, highlighting the characters' emotions and relevant actions, and must be closely related to the content of the song lyric. Each story should be at least 200 words long.

                                Your response should vividly capture the essence of the song lyric, incorporating the emotions and actions of the characters in a way that resonates with the given snippet. The story should convey a strong connection to the lyrical content, enriching the narrative with depth and relevance.

                                Please ensure that each story is crafted with attention to detail and creativity, immersing the reader in a compelling and meaningful tale that aligns closely with the provided song lyric snippet. The song lyric snippet is as follows:

                                {lyrics}
                                """
        self.__intel_story_writer = "You are one of the best story writers in the world.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02"
        self.together_client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
    #General setups for the LLM 
    def __establishKey(self): 
        os.environ['TOGETHER_API_KEY'] =  self.__key

    def ask_llama_3_8b_TOGETHER_API(self, prompt, intel= None):
        chat_completion_response = self.together_client.chat.completions.create(
            messages=[{"role": "system",
                    "content": self.intel},
                    {"role": "user", "content": prompt}],
            model="meta-llama/Llama-3-8b-chat-hf",
        )
        response_message = chat_completion_response.choices[0].message.content
        return response_message

    #Generates general controlling prompt 
    def generateText(self, topic, visualize=True):
        prompt = self.__lyric_prompt.format(topic=topic)
        return self.ask_llama_3_8b_TOGETHER_API(prompt)
    def generateStory(self, text):
        self.__intel =  self.__intel_story_writer
        lyrics = self.getLyrics(text)
        prompt = self.__story_prompt.format(lyrics=lyrics)
        return self.ask_llama_3_8b_TOGETHER_API(prompt)
    
    def getTitle(self, text):
        pattern = r'\*\*Song Title:\*\*\s*"([^"]+)"'
        match = re.search(pattern, text)
        return match
    def getLyrics(self, text): 
        lyrics_pattern = re.compile(r"\*\*Lyrics:\*\*\n\n(.*?)\n\n\*\*Audio Recording:\*\*", re.DOTALL)
        # Extract the lyrics
        match = lyrics_pattern.search(text)
        lyrics = match.group(1)
        return lyrics
    def getTempo(self, text): 
        tempo_pattern = re.compile(r"\*\*Tempo:\*\* (.*? BPM)")
        match = tempo_pattern.search(text)
        try: 
            tempo = match.group(1) 
        except:  
            tempo = "100 BPM"
        return tempo
    def getKey(self, text): 
        key_pattern = re.compile(r"\*\*Key:\*\* ([A-G][#b]? (?:Major|Minor))")
        match = key_pattern.search(text)
        key = match.group(1) 
        return key
    def getAudioRecording(self, text): 
        # Regular expression patterns to extract the audio recording and vocal performance sections
        audio_recording_pattern = r"\*\*Audio Recording:\*\*([\s\S]*?)\*\*Vocal Performance:\*\*"
        audio_recording_match = re.search(audio_recording_pattern, text)
        audio_recording = audio_recording_match.group(1)
        return audio_recording
    def getVocalPerformance(self, text): 
        vocal_performance_pattern = r"\*\*Vocal Performance:\*\*([\s\S]*)"
        vocal_performance_match = re.search(vocal_performance_pattern, text)
        vocal_performance = vocal_performance_match.group(1)
        return vocal_performance
    def getTimeSignature(self, text): 
        time_signature_pattern = re.compile(r"\*\*Time Signature:\*\* ([0-9]/[0-9])")
        # Extract the time signature
        match = time_signature_pattern.search(text)
        time_signature = match.group(1)
        return time_signature         
    def generateKeyFrames(self, text): 
        key_frame_prompt= f"""
        Generate a set of key frames frames from the following stories make them compelling 
        and interesting, they should be focused on attracting attention since they are for a 
        tik-tok video {text} """
        return self.ask_llama_3_8b_TOGETHER_API(key_frame_prompt)
    def generateImagePrompt(self, text): 
        image_prompt = f"""Generate an image prompt for each of the keyframes 
            Example: 
            Prompt:
            photo of a ino woman in a race car with black hair and a black pilot outfit,morning time, dessert

            Negative prompt:
            disfigured, ugly, bad, immature, cartoon, anime, 3d, painting, b&w, 2d, 3d, illustration, sketch, nfsw, nud.
            {text}
        """
        return self.ask_llama_3_8b_TOGETHER_API(image_prompt)
    def generateImagePrompts(self, text):
        story = self.generateStory(text)
        key_frames = self.generateKeyFrames(story)
        image_prompts = self.generateImagePrompt(key_frames)
        return image_prompts, key_frames
    def extractKeyFrames(self,keyframes): 
        pattern = re.compile(r'(\*\*Keyframe \d+:.*?\*\*.*?Negative prompt:.*?(?=\*\*Keyframe \d+:|\Z))', re.DOTALL)
        # Find all keyframes
        keyframes = pattern.findall(keyframes)
        return keyframes

    def extractKeyFrameTitle(self, keyframe):
        title_match = re.search(r'\*\*(Keyframe \d+: [^*]+)\*\*', keyframe)
        title = title_match.group(1)
        return title
