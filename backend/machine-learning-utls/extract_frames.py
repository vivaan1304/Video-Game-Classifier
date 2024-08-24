import cv2 as cv

DATA_DIR = "video-game-classifier/machine-learning-utls/data"
temp = "TEMP"
MAX_FRAMES = 500
def extract_frames(frames, game):
    cap = cv.VideoCapture(f"{DATA_DIR}/{temp}/test2.mp4")
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    frame_count = frames
    cur = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't recieve stream(stream end?). Exiting ...")
            break
        if cur % (total_frames//MAX_FRAMES) == 0:
            cv.imwrite(f"{DATA_DIR}/{game}/{frame_count}.jpeg", frame)
            frame_count += 1
            print(f"done {frame_count+1}") 
        cur += 1
    cap.release()
    cv.destroyAllWindows()  
    return frame_count