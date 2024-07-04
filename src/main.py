import os
import asyncio
import time
import aiohttp
import aiofiles
from LLM_processing import LLM
from imageGenerator import diffusion
from DreamMachineAPI.util import dreamMachineMake, refreshDreamMachine
from suno_api import custom_generate_audio, get_audio_information, download_audio
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, concatenate_audioclips

LLManager = LLM("I met my ex on Tik-Tok")
diffusionManager = diffusion()


def uniteTags(text, LLManager): 
    tempo = LLManager.getTempo(text)
    key = LLManager.getKey(text)
    audio_recording = LLManager.getAudioRecording(text)
    vocal_performance = LLManager.getVocalPerformance(text)
    time_signature = LLManager.getTimeSignature(text)
    tags = tempo + ' ' + key + ' ' + audio_recording + ' ' + vocal_performance + ' ' + time_signature   
    return tags

async def download_video(url, filename):
    output_path = os.path.join("../output/video", filename)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                f = await aiofiles.open(output_path, mode="wb")
                await f.write(await response.read())
                await f.close()
                print(f"Video downloaded: {output_path}")
            else:
                print(f"Failed to download video: {url}")


async def process_topic(topic, LLManager, diffusionManager, access_token):
    video_list = []
    
    text = LLManager.generateText(topic)
    lyrics = LLManager.getLyrics(text)
    title = LLManager.getTitle(text)
    tags = uniteTags(text)

    payload = {
        "prompt": lyrics,
        "tags": tags,
        "title": title,
        "make_instrumental": False,
        "wait_audio": False
    }
    audio_data = custom_generate_audio(payload)
    audio_ids = f"{audio_data[0]['id']},{audio_data[1]['id']}"
    print(f"Audio IDs: {audio_ids}")

    # Get audio information
    for _ in range(60):
        information = get_audio_information(audio_ids)
        if information[0]["status"] == "streaming":
            audio_url_1 = information[0]['audio_url']
            audio_url_2 = information[1]['audio_url']
            download_audio(audio_url_1, f"{title}_audio1.mp3")
            download_audio(audio_url_2, f"{title}_audio2.mp3")
            break
        time.sleep(5)


    image_prompts, key_frame_list = LLManager.generateImagePrompt(text)
    image_prompts_list = LLManager.extractKeyFrames(image_prompts)

    for keyframe, image_prompt in zip(key_frame_list, image_prompts_list):
        img = diffusionManager.generateImage(image_prompt, steps=20)
        title = LLManager.extractKeyFrameTitle(image_prompt)
        filename = f"{title}.png"
        img.save(filename)

        # Generate video
        make_json = dreamMachineMake(filename, access_token, keyframe)
        task_id = make_json[0]["id"]
        while True:
            response_json = refreshDreamMachine(access_token)
            for it in response_json:
                if it["id"] == task_id:
                    print(f"Processing state {it['state']}")
                    if it["video"]:
                        video_url = it["video"]["url"]
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
    final_clip.write_videofile(
        f"{topic.replace(' ', '_')}_final_video.mp4", codec="libx264"
    )
    audio_clip_1 = AudioFileClip(f"{title}_audio1.mp3")
    audio_clip_2 = AudioFileClip(f"{title}_audio2.mp3")
    #final_audio_clip = concatenate_audioclips([audio_clip_1, audio_clip_2])


    final_clip_with_audio = final_clip.set_audio(audio_clip_1)
    final_output_filename = f"{topic.replace(' ', '_')}_final_output.mp4"
    final_clip_with_audio.write_videofile(final_output_filename, codec="libx264", audio_codec="aac")
    print(f"Video generated with the frame approach successfully! Output file: {final_output_filename}")

async def process_topicCompleteVideo(topic, LLManager, diffusionManager, access_token):
    video_list = []
    text = LLManager.generateText(topic)
    lyrics = LLManager.getLyrics(text)
    title = LLManager.getTitle(text)
    tags = uniteTags(text)

    title = LLManager.get
    payload = {
        "prompt": lyrics,
        "tags": tags,
        "title": title,
        "make_instrumental": False,
        "wait_audio": False
    }
    audio_data = custom_generate_audio(payload)
    audio_ids = f"{audio_data[0]['id']},{audio_data[1]['id']}"
    print(f"Audio IDs: {audio_ids}")

    # Get audio information
    for _ in range(60):
        information = get_audio_information(audio_ids)
        if information[0]["status"] == "streaming":
            audio_url_1 = information[0]['audio_url']
            audio_url_2 = information[1]['audio_url']
            download_audio(audio_url_1, f"{title}_audio1.mp3")
            download_audio(audio_url_2, f"{title}_audio2.mp3")
            break
        time.sleep(5)

    
    image_prompts, key_frame_list = LLManager.generateImagePrompt(text)
    image_prompts_list = LLManager.extractKeyFrames(image_prompts)

    # img = diffusionManager.generateImage(image_prompt, steps=20)
    title = LLManager.extractKeyFrameTitle(image_prompts)
    filename = f"{title}.png"
    # img.save(filename)
    combined_string = " ".join(key_frame_list)


    # Generate video
    make_json = dreamMachineMake("", access_token, combined_string)
    task_id = make_json[0]["id"]
    while True:
        response_json = refreshDreamMachine(access_token)
        for it in response_json:
            if it["id"] == task_id:
                print(f"Processing state {it['state']}")
                if it["video"]:
                    video_url = it["video"]["url"]
                    video_filename = f"{title}.mp4"
                    await download_video(video_url, video_filename)
                    video_list.append(video_filename)
                    break
        await asyncio.sleep(3)
        break
    final_clip = VideoFileClip(video_list[0])
    final_clip.write_videofile(
        f"{topic.replace(' ', '_')}_final_video.mp4", codec="libx264"
    )
    audio_clip_1 = AudioFileClip(f"{title}_audio1.mp3")
    audio_clip_2 = AudioFileClip(f"{title}_audio2.mp3")
    #final_audio_clip = concatenate_audioclips([audio_clip_1, audio_clip_2])

    final_clip_with_audio = final_clip.set_audio(audio_clip_1)
    final_output_filename = f"{topic.replace(' ', '_')}_final_output.mp4"
    final_clip_with_audio.write_videofile(final_output_filename, codec="libx264", audio_codec="aac")
    print(f"Video generated with the whole video approach successfully! Output file: {final_output_filename}")
    """
    # Define a queue of prompts
    prompts = deque(key_frame_list)  
    while prompts:
        prompt = prompts.popleft()  # Get the next prompt from the queue
        # The image path can be empty
        img_file = ""
        
        print(f"Processing prompt: {prompt}")
        make_json = dreamMachineMake(prompt, access_token, img_file)
        print(make_json)
        task_id = make_json[0]["id"]
        
        while True:
            response_json = refreshDreamMachine(access_token)
    
            for it in response_json:
                if it["id"] == task_id:
                    print(f"proceeding state {it['state']}")
                    if it['video']:
                        print(f"New video link: {it['video']['url']}")
                        break
            await asyncio.sleep(3)
       
            break
     """

async def main():
    # Initialize managers
    topic_list = ["I met my ex on Tik-Tok", "Weather"]
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXNlcl91dWlkIjoiNDU4M2UxNzMtNmJkMi00NDlhLTllNzAtYzE1M2ViNzQ1MzliIiwiY2xpZW50X2lkIjoiIn0sImV4cCI6MTcyMDE4ODUxMn0.NCRjBo-GDmx0Wm78rVwxqI4U3ovz2JJnjQuWw3r03JY"
    tasks = []
    for topic in topic_list:
        tasks.append(process_topic(topic, LLManager, diffusionManager, access_token))
    await asyncio.gather(*tasks)


# Run the main function
asyncio.run(main())
