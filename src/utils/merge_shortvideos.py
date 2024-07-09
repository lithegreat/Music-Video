#pip install moviepy
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Define input file names
input_files = ['input1.mp4', 'input2.mp4']

# Load video clip objects from input files
video_clips = [VideoFileClip(file) for file in input_files]

# Concatenate video clips into a final clip
final_clip = concatenate_videoclips(video_clips)

# Write the final concatenated clip to an output file
final_clip.write_videofile('output.mp4')

# Optional: Close resources
final_clip.close()
for clip in video_clips:
    clip.close()