import asyncio
import aiohttp
import aiofiles
from LLM_processing import LLM
from imageGenerator import diffusion
from DreamMachineAPI.util import dreamMachineMake, refreshDreamMachine
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip, concatenate_videoclips


LLManager = LLM("I met my ex on Tik-Tok")
diffusionManager = diffusion()
async def download_video(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                f = await aiofiles.open(filename, mode='wb')
                await f.write(await response.read())
                await f.close()
                print(f"Video downloaded: {filename}")
            else:
                print(f"Failed to download video: {url}")

async def process_topic(topic, LLManager, diffusionManager, access_token):
    video_list = []
    image_prompts, key_frame_list = LLManager.generateImagePrompt(topic)
    image_prompts_list = LLManager.extractKeyFrames(image_prompts)

    
    for keyframe, image_prompt in zip(key_frame_list, image_prompts_list):
        img = diffusionManager.generateImage(image_prompt, steps=20)
        title = LLManager.extractKeyFrameTitle(img)
        filename = f"{title}.png"
        img.save(filename)
        
        # Generate video
        make_json = dreamMachineMake(img, access_token, keyframe)
        task_id = make_json[0]["id"]
        while True:
            response_json = refreshDreamMachine(access_token)
            for it in response_json:
                if it["id"] == task_id:
                    print(f"Processing state {it['state']}")
                    if it['video']:
                        video_url = it['video']['url']
                        video_filename = f"{title}.mp4"
                        await download_video(video_url, video_filename)
                        video_list.append(video_filename)
                        break
            await asyncio.sleep(3)
        else:
            continue
        break

    # Concatenate all videos for the current topic
    clips = [VideoFileClip(video) for video in video_list]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(f"{topic.replace(' ', '_')}_final_video.mp4", codec="libx264")

async def main():
    # Initialize managers
    LLManager = LLM("I met my ex on Tik-Tok")
    diffusionManager = diffusion()
    topic_list = ["I met my ex on Tik-Tok"]
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXNlcl91dWlkIjoiNDU4M2UxNzMtNmJkMi00NDlhLTllNzAtYzE1M2ViNzQ1MzliIiwiY2xpZW50X2lkIjoiIn0sImV4cCI6MTcyMDE4ODUxMn0.NCRjBo-GDmx0Wm78rVwxqI4U3ovz2JJnjQuWw3r03JY"
    tasks = []
    for topic in topic_list:
        tasks.append(process_topic(topic, LLManager, diffusionManager, access_token))
    await asyncio.gather(*tasks)

# Run the main function
asyncio.run(main())





