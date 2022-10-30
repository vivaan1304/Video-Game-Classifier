
import cv2 # import opencv used to process images and frames of videos
import os 
import numpy as np
import subprocess # import the suprocess module to run shell commands in python
from tqdm import tqdm # import tqdm loading bar

BASE_DIR = "./outputs" # base directory for saving the folders of the games in which frames are saved
os.makedirs(BASE_DIR, exist_ok=True) # create the base_dir

'''
Function to download and configure yt-dlp
'''
def getYtDl():
    outputDir = os.path.join(BASE_DIR, "yt-dlp")

    dlProc = subprocess.run(
        [
            "curl",
            "-L",
            "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp",
            "-o",
            outputDir,
        ]
    )

    chmodProc = subprocess.run(["chmod", "a+x", outputDir])

    return outputDir


playlists = { # a dictionary consisting of game-name(foldername)-link of yt playlist pairs
    "Among Us": "https://www.youtube.com/playlist?list=PLGtZwVE-T07slxVxf5D_Z5tWJ3P5B7zwj",
    "Apex Legends": "https://www.youtube.com/playlist?list=PLcpME8j-OMRywmvM1ZpQdbXx5YI_QyG86",
    "Forza": "https://www.youtube.com/playlist?list=PLClY3bOF3ZUALZ5pot9JSmQjO4YfZM5sU",
    "Free Fire": "https://www.youtube.com/playlist?list=PLGtZwVE-T07uEahKXKbq-FH8-mkMKk-Bb",
    "Genshin Impact": "https://youtube.com/playlist?list=PLnuhDgkSzb5pedCQ9o4SO73OxWQyZp7Qp",
    "God of War": "https://www.youtube.com/playlist?list=PLs1-UdHIwbo53L1KAkOZMvUSGHv9dAxYT",
    "Minecraft": "https://www.youtube.com/playlist?list=PL0oJ2_Q2jPrfHkS6Py1IRZBilTNpiKlXB",
    "Roblox": "https://www.youtube.com/playlist?list=PLKNadH2ebPUD52F-OWo-EB4K8Bgp8qKQp",
    "Terraria": "https://www.youtube.com/playlist?list=PL-JPD8A3qWVNUWDUU-32zCmFh3O9Xzo__",
}


# a function which returns the probability of a frame to be selected from a 
# video given the interval at which we choose frames
def getProb(f, interval, total_frames):
    return (np.cos(np.pi * f / interval) + 1.0) * 2 / (np.pi * interval)

# a function to go through the frames we selected in a video and saving them to write_dir
def getFrames(vid_path, write_dir, frame_index):
    if os.path.isdir(write_dir) == False:
        os.makedirs(write_dir)
  
    cap = cv2.VideoCapture(vid_path) # use the VideoCapture function from opencv to get the vidio at vid_path
    for frame in frame_index: # go through all the frames we need in order instead of going at all frames and choosing only those we need to reduce run time
        cap.set(cv2.cv2.CAP_PROP_POS_FRAMES, frame)
        _, frame = cap.read() # get the frame
        frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.imwrite( # write the image at the desired path
            os.path.join(
                write_dir, "frame" + str(len(os.listdir(write_dir)) + 1) + ".jpeg"
            ),
            frame,
        )

# count total number of frames in a video at vid_path
def countFrames(vid_path):
    video = cv2.VideoCapture(vid_path)
    totalframes = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    return totalframes


if __name__ == "__main__":
    ytPath = getYtDl() # get the path where yt-dlp is installed
    if os.path.exists(os.path.join(BASE_DIR, "video.mp4")):
        os.remove(os.path.join(BASE_DIR, "video.mp4"))
    np.random.rand()

    for key, playlist_link in playlists.items(): # go through all the games and playlists links
        write_dir = os.path.join(BASE_DIR, "data", key) # write directory for game = key
        os.makedirs(write_dir, exist_ok=True) # make the directory for storing the frames of game = key

        subprocess.run( # subprocess.run call to run yt-dlp command to get a list of all the video-ids in the playlist without downloading them 
            [
                ytPath,
                "--download-archive",
                os.path.join(write_dir, "videos.txt"),
                "--force-write-archive",
                "--no-download",
                playlist_link,
            ]
        )

        with open(os.path.join(write_dir, "videos.txt")) as file: # go through all the vid-ids in the file one at a time
            for line in tqdm(file):
                vid_id = line.split(" ")[1].strip()
                vid_path = os.path.join(BASE_DIR, "video.mp4")
                try:
                    subprocess.run( # subprocess call to run yt-dlp command to download the yt-video with video id = vid_id
                        [
                            ytPath,
                            f"http://www.youtube.com/watch?v={vid_id}",
                            "-o",
                            vid_path,
                        ]
                    )

                    frame_index = []
                    totalframes = countFrames(vid_path) #get total frames
                    interval = int(totalframes / 100) # get interval

                    for i in range(totalframes): # iterate over all frames in the video
                        rand_no = np.random.rand() # get rand_no b/w 0 and 1
                        p = getProb(i, interval, totalframes) # get probability of choosing ith frame
                        if p > rand_no: # if p > the rand_no then we choose that frame
                            frame_index.append(i)

                    getFrames(vid_path, write_dir, frame_index) #store all the frames

                except Exception as e:
                    pass
                finally:
                    if os.path.exists(vid_path): 
                        os.remove(vid_path) # delete the video after the frames are stored
