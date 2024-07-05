#For the installation process
!git clone https://github.com/justinjohn0306/Wav2Lip
!cd Wav2Lip && pip install -r requirements_colab.txt
%cd /content/Wav2Lip
!wget 'https://github.com/justinjohn0306/Wav2Lip/releases \
/download/models/wav2lip.pth' -O 'checkpoints/wav2lip.pth'

!wget 'https://github.com/justinjohn0306/Wav2Lip/releases \
/download/models/wav2lip_gan.pth' -O 'checkpoints/wav2lip_gan.pth'

!wget 'https://github.com/justinjohn0306/Wav2Lip/releases \
/download/models/mobilenet.pth' -O 'checkpoints/mobilenet.pth'

!pip install batch-face
%cd /content/Wav2Lip

pad_top =  0
pad_bottom =  15
pad_left =  0
pad_right =  0
rescaleFactor =  1

video_path_fix = f"'../{video_path}'"

!python inference.py --checkpoint_path 'checkpoints/wav2lip_gan.pth' \
--face $video_path_fix --audio "/content/final_output_synth_audio_hi.wav" \
--pads $pad_top $pad_bottom $pad_left $pad_right --resize_factor $rescaleFactor --nosmooth \ 
--outfile '/content/output_video.mp4'



