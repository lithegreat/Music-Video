import os
from together import Together
import re 
class LLM: 
    def __init__(self, key, intel, topic): 
        self.__key = "8069bcddb5b335ea3e2f23e9d58d83d5dfb270ee6ffcb8a546fbcdf8fb336dac" if key is None else key 
        self.__establishKey()
        self.__intel = "You are one of the best song writers in the world.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02" if intel is None else intel
        self.__base_prompt =  """Create a set of song lyrics of the topic {topic} that demonstrate your vocal abilities and emotional expression. 
                                The lyrics should be accompanied by a professional-level audio recording with clear enunciation and crystal-clear audio quality. 
                                The song should feature a captivating melody and sophisticated arrangement, production, and performance. 
                                The lyrics must rhyme to enhance the song's flow and aesthetic appeal. You are encouraged to explore various themes and musical styles, 
                                but the final composition must meet the above criteria to showcase your talent and depth as a creator and performer. 
                                The lyrics should convey emotional expression and physical actions to ensure a high-quality performance."""
        self.__together_client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
    #General setups for the LLM 
    def __establishKey(self): 
        os.environ['TOGETHER_API_KEY'] =  self.key

    def ask_llama_3_8b_stream_TOGETHER_API(self, prompt):

        chat_completion_stream_response = self.__together_client.chat.completions.create(
            messages=[{"role": "system",
                    "content": self.__intel},
                    {"role": "user", "content": prompt}],
            model="meta-llama/Llama-3-8b-chat-hf",
            stream=True,
        )
        response_message = chat_completion_stream_response['message']['content']
        #For generating the 
        for chunk in chat_completion_stream_response:
            print(chunk.choices[0].delta.content or "", end="", flush=True)
        
        return response_message
    #Generates general controlling prompt 
    def generateText(self, topic, visualize=True):
        prompt = self.__base_prompt.format(topic=topic)
        if visualize: 
            self.ask_llama_3_8b_stream_TOGETHER_API(prompt)
        return self.ask_llama_3_8b_TOGETHER_API(prompt)
    
    #Helper functions 
    def getTitle(self, text):
        pattern = r'\*\*Song Title:\*\*\s*"([^"]+)"'
        match = re.search(pattern, text)
        song_title = match.group(1)
        return song_title
    def getGenere(self, text): 
        pattern = r'\*\*Genre:\*\*\s*(.+)'
        match = re.search(pattern, text)
        genre = match.group(1)
        return genre
    def getLyrics(self, text): 
        lyrics_pattern = re.compile(r"\*\*Lyrics:\*\*\n\n(.*?)\n\n\*\*Audio Recording:\*\*", re.DOTALL)
        # Extract the lyrics
        match = lyrics_pattern.search(text)
        lyrics = match.group(1)
        return lyrics
    def getTempo(self, text): 
        tempo_pattern = re.compile(r"\*\*Tempo:\*\* (.*? BPM)")
        match = tempo_pattern.search(text)
        tempo = match.group(1) 
        return tempo
    def getTimeSignature(self, text): 
        time_signature_pattern = re.compile(r"\*\*Time Signature:\*\* ([0-9]/[0-9])")
        # Extract the time signature
        match = time_signature_pattern.search(text)
        time_signature = match.group(1)
        return time_signature
   
        
                                    



    










#ToDo add examples to the prompt 
topic = ""
prompt = f"""Write a set of compelling lyrics for a song with topic {topic} and perform it with your exceptional singing skills. The lyrics should 
convey a meaningful message or tell a captivating story, and your performance should showcase your vocal abilities and emotional expression. 
Your goal is to create an original and engaging musical piece that resonates with the audience. Feel free to explore various themes and musical styles 
to demonstrate the depth of your talent as a lyricist and singer.
"""
lyrics = ask_llama_3_8b_TOGETHER_API(system_intel, prompt)

