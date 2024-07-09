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
        self.__lyric_prompt_2 =  """Fill in the following template of song lyrics of the topic {topic}, restrict yourself to filling the template.
                                Template:
                                **Song Title:** "[title]"

                                **Genre:** [genre]

                                **Tempo:** [X BPM]

                                **Time Signature:** X/4

                                **Key:** [Main chord] [Major/Minor]

                                **Lyrics:**

                                [Verse 1]
                                [verse 1 lyrics]


                                [Chorus]
                                [chorus lyrics]

                                **Audio Recording:**
                                * [melody, example: nostalgia, longing, melacholy]
                                * [beat in the form of adjective list]
                                * [rythm in the form of adjective list]

                                **Vocal Performance:**
                                * [emotions in the form of adjective list]
                                * [vocal range in the form of adjective list]
                                * [expression in the form of adjective list]
        """

        self.__story_prompt = """As a story writer, your task is to create a short story,  based on a given song lyric snippet. Each story should be detailed, highlighting the characters' emotions and relevant actions, and must be closely related to the content of the song lyric. Each story should be at least 200 words long.

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
    def generateTextGeneralVideo(self, topic, visualize=True):
        prompt = self.__lyric_prompt_2.format(topic=topic)
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
        lyrics_section = self.ask_llama_3_8b_TOGETHER_API("Extract the lyrics from the following: " + text)
        return lyrics_section
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
        Fill the following template, by describing each line as a musical video scene, do a maximum of 6 scenes, incorporating detailed physical appearances, actions, and postures,
        add the character description to each scene integrate the character description into the prompt.
        From scene 2 onwards if you see any character name repetition please repeat the same physical description, wrong: the same protagonist, with the same physical description or [character name], with the same physical description.
        Add at the end of each scene:  
        Negative prompt: Negative prompt: bad anatomy, bad proportions, blurry, cloned face, deformed, disfigured, duplicate, extra arms, extra fingers, extra limbs, extra legs, fused fingers, gross proportions, long neck, malformed limbs, missing arms.
        Lyrics:         
        {text}
        Template:
        *Scene 1: Introduction*
        Prompt:
        Physical scenario: [description]
        Character/s physical description: [name][man/woman][age][hair color][hair length][hair style][eye color][face descriptions][height][clothing style][clothing color][clothing material], [name][man/woman][age][hair color][hair length][hair style][eye color][face descriptions][height][clothing style][clothing color][clothing material]
        Character actions: [description]
        Plot development: [description]
        Negative prompt: bad anatomy, bad proportions, blurry, cloned face, deformed, disfigured, duplicate, extra arms, extra fingers, extra limbs, extra legs, fused fingers, gross proportions, long neck, malformed limbs, missing arms.
        *Scene 2: scene 2 title*
        Prompt:
        Physical scenario: [description]
        Character/s physical description: [name][man/woman][age][hair color][hair length][hair style][eye color][face descriptions][height][clothing style][clothing color][clothing material], [name][man/woman][age][hair color][hair length][hair style][eye color][face descriptions][height][clothing style][clothing color][clothing material]
        Characters actions: [description]
        Plot development: [description] 
        Negative prompt: bad anatomy, bad proportions, blurry, cloned face, deformed, disfigured, duplicate, extra arms, extra fingers, extra limbs, extra legs, fused fingers, gross proportions, long neck, malformed limbs, missing arms.
        *Scene 3: scene 3 title*
        Prompt:
        Physical scenario: [description]
        Character/s physical description: [name][man/woman][age][hair color][hair length][hair style][eye color][face descriptions][height][clothing style][clothing color][clothing material], [name][man/woman][age][hair color][hair length][hair style][eye color][face descriptions][height][clothing style][clothing color][clothing material]
        Character/s actions: [description]
        Plot development: [description] 
        Negative prompt: bad anatomy, bad proportions, blurry, cloned face, deformed, disfigured, duplicate, extra arms, extra fingers, extra limbs, extra legs, fused fingers, gross proportions, long neck, malformed limbs, missing arms.
        *Scene 4: scene 4 title*
        Prompt:
        Physical scenario: [description]
        Character/s physical description: [name][man/woman][age][hair color][hair length][hair style][eye color][face descriptions][height][clothing style][clothing color][clothing material], [name][man/woman][age][hair color][hair length][hair style][eye color][face descriptions][height][clothing style][clothing color][clothing material]
        Character actions: [description]
        Plot development: [description] 
        Negative prompt: bad anatomy, bad proportions, blurry, cloned face, deformed, disfigured, duplicate, extra arms, extra fingers, extra limbs, extra legs, fused fingers, gross proportions, long neck, malformed limbs, missing arms.
        *Scene 5: [scene 5 title]*
        Prompt:
        Physical scenario: [description]
        Character/s physical description: [name][man/woman][age][hair color][hair length][hair style][eye color][face descriptions][height][clothing style][clothing color][clothing material], [name][man/woman][age][hair color][hair length][hair style][eye color][face descriptions][height][clothing style][clothing color][clothing material]
        Character actions: [description]
        Plot development: [description]] 
        Negative prompt: bad anatomy, bad proportions, blurry, cloned face, deformed, disfigured, duplicate, extra arms, extra fingers, extra limbs, extra legs, fused fingers, gross proportions, long neck, malformed limbs, missing arms.
        *Scene 6: Conclusion*
        Prompt:
        Physical scenario: [description]
        Character/s physical description: [name][man/woman][age][hair color][hair length][hair style][eye color][face descriptions][height][clothing style][clothing color][clothing material], [name][man/woman][age][hair color][hair length][hair style][eye color][face descriptions][height][clothing style][clothing color][clothing material]
        Plot development: [description]
        Negative prompt: bad anatomy, bad proportions, blurry, cloned face, deformed, disfigured, duplicate, extra arms, extra fingers, extra limbs, extra legs, fused fingers, gross proportions, long neck, malformed limbs, missing arms."""
        first_output = self.ask_llama_3_8b_TOGETHER_API(key_frame_prompt)
        #Add the regex pattern for extracting the keyframes as a list
        keyframe_list = self.extractKeyFrames(first_output)
        return keyframe_list

    def generateAnimationPrompt(self, keyframe, story):
        image_prompt = f"""
            Generate animation instructions, stick to the format of the example, based on the following keyframe and story keyframe: {keyframe}, story: {story}
            Example:
            **Animation Instructions:**\n 1. Start with a static image of the narrator sitting in front of a computer or phone, surrounded by a blurred background of social media feeds.\n2. Add a subtle animation of likes and comments swirling around the narrator's head, using a gentle, wispy motion. This will give the impression of the narrator being surrounded by the digital world.\n3. As the narrator scrolls through Tik-Tok, add a slight blur effect to the background to give the impression of movement.\n4. When the narrator sees the stranger with piercing blue eyes and a charming smile, add a slight zoom effect to their face to draw attention to it.\n5. Use a warm and cozy color palette to set the tone for the scene, with a focus on calming blues and whites.\n6. Add some gentle, soft lighting to the scene to create a sense of intimacy and warmth.\n7. Use a mix of 2D and 3D elements to create a sense of depth and dimensionality in the scene.\n8. Avoid using any disfigured, ugly, or immature elements in the animation, and focus on creating a clean and polished look."""
        return self.ask_llama_3_8b_TOGETHER_API(image_prompt)
    def generateImagePrompts(self, text):
        image_prompts = self.generateKeyFrames(text)
        return image_prompts
    
    def extractKeyFrames(self, keyframes):
        scene_list = []
        title_list = []
        pattern = r"""Scene \d+: (.*?)\nPhysical scenario: (.*?)\nCharacter/s physical description: (.*?)\nCharacter actions: (.*?)\nPlot development: (.*?)\nNegative prompt: (.*?)\n"""
        matches = re.findall(pattern, keyframes, re.DOTALL)
        output = ""
        for i, match in enumerate(matches):
            title  = match[0].strip()
            output += f"  Physical scenario: {match[1].strip()}\n"
            output += f"  Character/s physical description: {match[2].strip()}\n"
            output += f"  Character actions: {match[3].strip()}\n"
            output += f"  Plot development: {match[4].strip()}\n"
            output += f"  Negative prompt: {match[5].strip()}\n"
            scene_list.append(output)
            title_list.append(title)
    
        return scene_list, title_list
    
    def furtherImprovePrompt(self, prompt): 
        return self.ask_llama_3_8b_TOGETHER_API(f"Improve the following scene by eliminating irrelevant details and improving engagement quality, maintain the same format: {prompt}")
    def generateExtraTags(self, lyrics): 
        answer = self.ask_llama_3_8b_TOGETHER_API(f"Get 10 words, that describe the characteristcs of the song join them by comas do not use numbers only maximum 10 words, {lyrics}")
        lines = answer.strip().split('\n')
        return lines[2]
    
    def extractIndividualKeyFrameTitle(self, keyframe):
        pattern = re.compile(r"Scene\s\d+:\s(?P<title>.*?)\n")
        match = pattern.search(keyframe)
        if match:
            title = match.group("title")
            return title
        else:
            print("No title found")


    def extractKeyFrameTitle(self, keyframe):
        title_match = re.search(r'\*\*(Keyframe \d+: [^*]+)\*\*', keyframe)
        title = title_match.group(1)
        return title
