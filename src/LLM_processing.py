import os
from together import Together
import re
class LLM:
    def __init__(self, topic, product_description, key=None, intel=None):
        os.environ['TOGETHER_API_KEY'] =  "8069bcddb5b335ea3e2f23e9d58d83d5dfb270ee6ffcb8a546fbcdf8fb336dac" if key is None else key
        self.intel = "You are one of the best song writers in the world.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02" if intel is None else intel
        self.__lyric_prompt =  """Convert the product description into a song using the following format by filling in the topic part, {product_description}
                                Create a set of song lyrics of the topic {topic} that demonstrate your vocal abilities and emotional expression. 
                                The lyrics should be accompanied by a professional-level audio recording with clear enunciation and crystal-clear audio quality. 
                                The song should feature a captivating melody and sophisticated arrangement, production, and performance. 
                                The lyrics must rhyme to enhance the song's flow and aesthetic appeal. You are encouraged to explore various themes and musical styles, 
                                but the final composition must meet the above criteria to showcase your talent and depth as a creator and performer. 
                                The lyrics should convey emotional expression and physical actions to ensure a high-quality performance.
                                Example:
                                **Song Title:** "Swipe Right on Memories"

                                **Genre:** Pop-Rock with a hint of Electronic elements

                                **Tempo:** Moderate (around 120 BPM)

                                **Time Signature:** 4/4

                                **Key:** C Major

                                **Lyrics:**

                                [Verse 1]
                                I was scrolling through my feed, feeling so alone
                                When I saw your face, and my heart started to moan
                                A swipe right, and our stories aligned
                                Little did I know, our love would be redefined

                                [Verse 2]
                                We'd lip-sync to our favorite songs, and our hearts would beat as one
                                We'd create our own stories, and our love would be won
                                But like a fleeting dream, our love would fade away
                                Leaving me with just a memory, of our digital day

                                [Chorus]
                                I met my ex on Tik-Tok, in a world of endless fame
                                We danced to the rhythm, of our own little game
                                We laughed, we loved, we lived, in a virtual haze
                                But now I'm left with just a memory, and a fading phase

                                **Audio Recording:**

                                The song features a mix of acoustic and electronic elements, with a focus on showcasing the vocalist's range and emotional expression. The arrangement is designed to build tension and release, with a focus on the chorus and bridge.

                                * The verse features a simple, pulsing electronic beat, accompanied by a minimalist piano melody and subtle ambient pads.
                                * The chorus introduces a driving rock rhythm, with crunching guitars and a soaring vocal performance.
                                * The bridge features a haunting piano solo, accompanied by atmospheric synths and a subtle drum machine pattern.
                                * The final chorus features a reprise of the rock rhythm, with added layers of harmonies and a dramatic build-up to the song's conclusion.

                                **Vocal Performance:**

                                The vocalist delivers a powerful, emotive performance, with a focus on conveying the emotional depth of the lyrics. The vocal range is showcased throughout the song, with a focus on the chorus and bridge.

                                * The verse features a more subdued, introspective performance, with a focus on storytelling and emotional expression.
                                * The chorus features a more dramatic, anthemic performance, with a focus on showcasing the vocalist's range and power.
                                * The bridge features a more intimate, vulnerable performance, with a focus on conveying the emotional pain and longing.

                                **Production and Performance:**

                                The production is designed to be polished and professional, with a focus on showcasing the vocalist's performance and the song's emotional depth. The arrangement is carefully crafted to build tension and release, with a focus on the chorus and bridge.

                                * The mix is balanced and clear, with a focus on the vocalist's performance and the song's emotional impact.
                                * The mastering is designed to be loud and clear, with a focus on delivering a high-quality listening experience.

                                **Physical Actions:**

                                The performance features a range of physical actions, designed to enhance the emotional expression and storytelling of the lyrics.

                                * The vocalist performs a range of gestures and movements, including hand gestures, facial expressions, and body language.
                                * The performance features a range of props and visual elements, including screens, lights, and projections.
                                * The choreography is designed to be dynamic and engaging, with a focus on conveying the emotional depth and complexity of the lyrics.
        """

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
    def generateText(self, topic, product_description, visualize=True):
        prompt = self.__lyric_prompt.format(topic=topic, product_description=product_description)
        return self.ask_llama_3_8b_TOGETHER_API(prompt)
    def generateStory(self, text):
        self.__intel =  self.__intel_story_writer
        lyrics = self.getLyrics(text)
        prompt = self.__story_prompt.format(lyrics=lyrics)
        return self.ask_llama_3_8b_TOGETHER_API(prompt)

    def getTitle(self, text):
        pattern = re.compile(r'\*\*Song Title:\*\*\s*"([^"]+)"')
        match = re.search(pattern, text)
        title = match.group(1)
        return title
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
            tempo = "Moderate (100 BPM)"
        return tempo
    def getKey(self, text):
        key_pattern = re.compile(r"\*\*Key:\*\* ([A-G][#b]? (?:Major|Minor))")
        match = key_pattern.search(text)
        key = match.group(1)
        return key
    def getAudioRecording(self, text):
        # Regular expression patterns to extract the audio recording and vocal performance sections
        audio_recording_pattern = re.compile(r"\*\*Audio Recording:\*\*([\s\S]*?)\*\*Vocal Performance:\*\*")
        audio_recording_match = re.search(audio_recording_pattern, text)
        audio_recording = audio_recording_match.group(1)
        return audio_recording
    def getVocalPerformance(self, text):
        vocal_performance_pattern = re.compile(r"\*\*Vocal Performance:\*\*([\s\S]*)")
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
        tik-tok video {text} 
        Examples: 
        **Scene 1: Introduction**
        Prompt:
        Photo of a worn leather-bound book with the title "Fantasy" embossed on the cover, placed on a wooden table with a warm and cozy atmosphere, morning time, indoors.
        Negative prompt:
        disfigured, ugly, bad, immature, cartoon, anime, 3d, painting, b&w, 2d, illustration, sketch, nfsw, nud.

        **Scene 2: The Weight of the World**
        Prompt:
        Photo of a person (the narrator) sitting in a cozy bookstore, looking stressed and overwhelmed, with a subtle animation of words and symbols swirling around their head, representing the weight of the world, morning time, indoors.
        Negative prompt:
        disfigured, ugly, bad, immature, cartoon, anime, 3d, painting, b&w, 2d, illustration, sketch, nfsw, nud.

        **Scene 3: The World of Fantasy**
        Prompt:
        Photo of a montage of illustrations and animations showcasing mythical creatures, magical landscapes, and epic quests, with a warm and inviting color palette, morning time, indoors.
        Negative prompt:
        disfigured, ugly, bad, immature, cartoon, anime, 3d, painting, b&w, 2d, illustration, sketch, nfsw, nud.

        **Scene 4: Becoming One with the Characters**
        Prompt:
        Photo of a series of split-screen shots showing the narrator as different characters from their favorite books (e.g., a brave warrior, a cunning thief, a wise wizard), with a subtle animation of the character's features blending with theirs, morning time, indoors.
        Negative prompt:
        disfigured, ugly, bad, immature, cartoon, anime, 3d, painting, b&w, 2d, illustration, sketch, nfsw, nud.

        **Scene 5: The Power of Fantasy**
        Prompt:
        Photo of a person (the narrator) sitting in a cozy bookstore, surrounded by books, with a warm and inviting smile, and a subtle animation of fantasy elements (e.g., dragons, unicorns, magic spells) swirling around them, morning time, indoors.
        Negative prompt:
        disfigured, ugly, bad, immature, cartoon, anime, 3d, painting, b&w, 2d, illustration, sketch, nfsw, nud.

        **Scene 6: Conclusion**
        Prompt:
        Photo of a person (the narrator) closing a book and pushing it back onto the shelf, with a peaceful and content expression, morning time, indoors.
        Negative prompt:
        disfigured, ugly, bad, immature, cartoon, anime, 3d, painting, b&w, 2d, illustration, sketch, nfsw, nud.
        """
        return self.ask_llama_3_8b_TOGETHER_API(key_frame_prompt)
    def generateImagePrompt(self, text):
        image_prompt = f"""Generate an image prompt for each of the keyframes, stick to style of the example
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
    
    def extractKeyFrames(self, keyframes):
        pattern = re.compile(r"""
        \*\*Scene\s(?P<number>\d+):\s(?P<title>.*?)\*\*\nPrompt:\n (?P<prompt>.*?)\nNegative\sprompt:\n(?P<negative_prompt>.*?)\n""", re.DOTALL | re.VERBOSE)

        scenes = [match.groupdict() for match in pattern.finditer(keyframes)]

        scene_list = []
        for scene in scenes:
            scene_str = (
                f"Scene {scene['number']}: {scene['title']}\n"
                f"Prompt: {scene['prompt']}\n"
                f"Negative Prompt: {scene['negative_prompt']}\n"
            )
            scene_list.append(scene_str)
        return scene_list
    
    def extractIndividualKeyFrameTitle(self, keyframe):
        pattern = re.compile(r"Scene\s\d+:\s(?P<title>.*?)\n")

        match = pattern.search(keyframe)

        if match:
            title = match.group("title")
            return title
        else:
            print("No title found")
        
    def extractKeyFrames(self,keyframes):
        pattern = re.compile(r'(\*\*Keyframe \d+:.*?\*\*.*?Negative prompt:.*?(?=\*\*Keyframe \d+:|\Z))', re.DOTALL)
        # Find all keyframes
        keyframes = pattern.findall(keyframes)
        return keyframes

    def extractKeyFrameTitle(self, keyframe):
        title_match = re.search(r'\*\*(Keyframe \d+: [^*]+)\*\*', keyframe)
        title = title_match.group(1)
        return title
