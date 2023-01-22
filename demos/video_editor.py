import os 
from dotenv import load_dotenv
from moviepy.video.fx import speedx
from moviepy.editor import VideoFileClip



# Add environment variables 
load_dotenv()
 

src_vid_1 = os.getenv('CHATGPT_SRC_DEMO_1')
src_vid_2 = os.getenv('CHATGPT_SRC_DEMO_2')
tgt_vid_1 = os.getenv('CHATGPT_TGT_DEMO_1')
tgt_vid_2 = os.getenv('CHATGPT_TGT_DEMO_2')



# Add video flags to create demos or not 
RUN_CHATGPT_DEMO_VID_1 = True
RUN_CHATGPT_DEMO_VID_2 = True


# ============ DEMO VID 1 =============

if RUN_CHATGPT_DEMO_VID_1:

    # Open the video file
    clip = VideoFileClip(src_vid_1)



    # Get the current frames per second (fps) of the video
    fps = clip.fps



    # Set the fps to be 2 times the current fps
    clip = clip.set_fps(fps*2)



    # Select the first 30 seconds of the sped up video
    clip_25s = clip.subclip(0,25)



    # Save the new video file
    clip_25s.write_videofile(tgt_vid_1)



# ============ DEMO VID 2 =============

if RUN_CHATGPT_DEMO_VID_2:
    
    # Open the video file
    clip = VideoFileClip(src_vid_2)



    # Get the current frames per second (fps) of the video
    fps = clip.fps



    # Set the fps to be 2 times the current fps
    clip = clip.set_fps(fps*5)



    # # Select the first 45 seconds of the sped up video
    clip = clip.subclip(0,92)



    # Save the new video file
    clip.write_videofile(tgt_vid_2)
