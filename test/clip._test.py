from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

topic = "A book of memories"
title = "A book of memories"
video_list = [
    "Introduction.mp4",
    "Uncovering Memories.mp4",
    "Whispers of the Past.mp4",
]

# 检查当前工作目录和视频、音频文件的实际路径
import os

# 输出当前工作目录
print("Current working directory:", os.getcwd())

# 输出视频文件的实际路径
for file in video_list:
    video_file_path = os.path.join("./outputs", file)
    print(f"Resolved path for {file}: {video_file_path}")

# 输出音频文件的实际路径
audio_file_path = os.path.join("./outputs", f"{title}.mp3")
print(f"Resolved path for audio file: {audio_file_path}")

# 构建视频剪辑对象
video_clips = [VideoFileClip(video_file_path) for video_file_path in [os.path.join("./outputs", file) for file in video_list]]
final_clip = concatenate_videoclips(video_clips)

# 将最终拼接的视频写入文件
final_clip.write_videofile(f'{title}.mp4')

# 加载音频文件
audio_clip_1 = AudioFileClip(audio_file_path)

# 将音频与视频合成
final_clip_with_audio = final_clip.set_audio(audio_clip_1)

# 写入最终输出文件
final_output_filename = os.path.join("./outputs", f"{topic.replace(' ', '_')}_final_output.mp4")
final_clip_with_audio.write_videofile(final_output_filename, codec="libx264", audio_codec="aac")

print(f"Video generated with the whole video approach successfully! Output file: {final_output_filename}")
