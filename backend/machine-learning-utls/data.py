# FORTNITE
# APEX LEGENDS
# PUBG
# PALADINS
# VALORANT
# CSGO
# CS-2

from pytubefix import Search, YouTube
from pytubefix.cli import on_progress
import os
from extract_frames import *
import tqdm as timer
DATA_DIR = "video-game-classifier/machine-learning-utls/data"
temp = "TEMP"
playlists = {'Fortnite':"https://www.youtube.com/playlist?list=PLcpME8j-OMRzC-d-gkMYscnjwTYFGHDsT",
             'Apex Legends':"https://www.youtube.com/playlist?list=PLQScuw2de7_TEX-BbBOqS8Kr8qE8WJgZY",
             'PUBG':"https://www.youtube.com/playlist?list=PLkQAJmDGGw2iKpb5oEZKcPmJiDKXZ3mOy",
             'Paladins':"https://www.youtube.com/playlist?list=PL5IfJCtcOHq3-vQUF4FCfx9Q1To2D68hw",
             'Valorant':"https://www.youtube.com/playlist?list=PL_6d-58WAdtf8uY4o_UlRJHeLCFU98ydu",
             'CSGO':"https://www.youtube.com/playlist?list=PLPGkIsTi7ZL5Ob-5_WPBm97vjLapucAka",
             'CSGO-2':"https://www.youtube.com/playlist?list=PLxTav45lEQRGiUJkfsETYo_8kCSXo6jLQ" }

DEBUG=1
MAX_VIDEOS = 10
for game, link in timer.tqdm(playlists.items()):
    if DEBUG==0 and game in os.listdir(DATA_DIR):
        continue
    if game not in os.listdir(DATA_DIR):
        os.mkdir(f"{DATA_DIR}/{game}")
    
    results = Search(f"{game} Gameplay no commentary")
    frames = 0
    num_videos = 0
    print("here")
    for video in results.videos:
        if video.length >= 1200 and video.length <= 1800:
            yt = YouTube(video.watch_url, on_progress_callback = on_progress)
            print(f"url: {video.watch_url} minutes: {video.length//60}, seconds: {video.length%60}")
            yt.streams.filter(res="720p").first().download(f"{DATA_DIR}/TEMP", filename = "test2.mp4")
            frames = extract_frames(frames, game)
            num_videos += 1
        if num_videos >= MAX_VIDEOS:
            break
    