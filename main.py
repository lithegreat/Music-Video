from LLM_processing import LLM
from imageGenerator import diffusion
import asyncio
from DreamMachineAPI.util import dreamMachineMake, refreshDreamMachine
import matplotlib.pyplot as plt 


def main(): 
    #Alternative 1: Generate the keyframes and animate each of the keyframes 
    LLManager = LLM("I met my ex on Tik-Tok")
    diffusionManager = diffusion()  
    topic_list = ["I met my ex on Tik-Tok", ]
    for topic in topic_list: 
        key_frame_prompts = LLManager.generateImagePrompt(topic)
        key_frame_prompt_list = LLManager.extractKeyFrames(key_frame_prompts)
        for keyframe in key_frame_prompt_list:
            img = diffusionManager.generateImage(keyframe, steps=20)
            title = LLManager.extractKeyFrameTitle(keyframe)
            # Save the image with the title
            filename = f"{title}.png"
            img.save(filename)
            #Luma Key 
            access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXNlcl91dWlkIjoiNDU4M2UxNzMtNmJkMi00NDlhLTllNzAtYzE1M2ViNzQ1MzliIiwiY2xpZW50X2lkIjoiIn0sImV4cCI6MTcyMDE4ODUxMn0.NCRjBo-GDmx0Wm78rVwxqI4U3ovz2JJnjQuWw3r03JY"
            make_json = dreamMachineMake(img, access_token, keyframe)
            task_id = make_json[0]["id"]
            while True:
                response_json = refreshDreamMachine(access_token)
                for it in response_json:
                    if it["id"] == task_id:
                        print(f"proceeding state {it['state']}")
                        if it['video']:
                            print(f"New video link: {it['video']['url']}")
                            return
                    await asyncio.sleep(3)



