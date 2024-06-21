import os
from together import Together
class LLM:
    def __init__(self, key, intel, topic):
        self.__key = "8069bcddb5b335ea3e2f23e9d58d83d5dfb270ee6ffcb8a546fbcdf8fb336dac" if key is None else key
        self.__establishKey()
        self.__intel = "You are one of the best song writers in the world.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02" if intel is None else intel
        self.__base_prompt =  f"""Write a set of compelling lyrics for a song with topic {topic} and perform it with your exceptional singing skills.
                                The lyrics should convey a meaningful message or tell a captivating story, and your performance should showcase your vocal
                                abilities and emotional expression. Your goal is to create an original and engaging musical piece that resonates with the audience.
                                Feel free to explore various themes and musical styles to demonstrate the depth of your talent as a lyricist and singer. """
        self.__together_client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

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

    def generateText(self, topic, visualize=True):
        prompt = self.__base_prompt.replace("topic", topic)
        if visualize:
            self.ask_llama_3_8b_stream_TOGETHER_API(prompt)



        return self.ask_llama_3_8b_TOGETHER_API(prompt)

    def save_data_to_txt(self, filename):
        prompt = self.__base_prompt.replace("topic", topic)
        data_to_save = self.ask_llama_3_8b_stream_TOGETHER_API(prompt)

        with open(filename, 'w') as f:
            f.write(data_to_save)

        print(f"Data saved to {filename}")

    save_data_to_txt('lyrics.txt')








#ToDo add examples to the prompt
topic = ""
prompt = f"""Write a set of compelling lyrics for a song with topic {topic} and perform it with your exceptional singing skills. The lyrics should
convey a meaningful message or tell a captivating story, and your performance should showcase your vocal abilities and emotional expression.
Your goal is to create an original and engaging musical piece that resonates with the audience. Feel free to explore various themes and musical styles
to demonstrate the depth of your talent as a lyricist and singer.
"""
lyrics = ask_llama_3_8b_TOGETHER_API(system_intel, prompt)
