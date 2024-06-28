# conda env update -f environment.yml
# conda activate lsync

from lsync import LyricsSync
audio_path = "./generated_audio.wav"
lyrics_path = "./lyrics.txt"
lsync = LyricsSync()
words, lrc = lsync.sync(audio_path, lyrics_path)