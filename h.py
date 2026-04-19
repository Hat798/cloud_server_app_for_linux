import cv2
import os
import time
import urllib.request
import winsound
import threading

# Cấu hình
VIDEO_URL = "https://dn721604.ca.archive.org/0/items/touhou-bad-apple-pv-g-3-c-vev-i-36s/Touhou%20-%20Bad%20Apple%21%21%20%20PV%20%5BG3C-VevI36s%5D.mp4"
AUDIO_URL = "https://ia903102.us.archive.org/26/items/a_20260419/a.wav"
WIDTH, HEIGHT = 80, 40
CHARS = "@#%*•+=-:,.▹ "

# Tải file nếu chưa có
def setup():
    for url, name in [(AUDIO_URL, "a.wav"), (VIDEO_URL, "v.mp4")]:
        if not os.path.exists(name):
            print(f"Đang tải {name}...")
            urllib.request.urlretrieve(url, name)

def run():
    cap = cv2.VideoCapture("v.mp4")
    # Phát nhạc
    threading.Thread(target=lambda: winsound.PlaySound("a.wav", winsound.SND_FILENAME)).start()
    
    print("\033[2J") # Xóa màn hình
    
    # --- THÔNG SỐ QUAN TRỌNG ---
    # 30 FPS tương đương ~0.0333s mỗi khung hình. 
    # Trừ đi khoảng 0.002s máy tính dùng để render ảnh.
    sleep_time = 0.03112 
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # Xử lý ASCII
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = cv2.resize(gray, (WIDTH, HEIGHT))
        
        # Dùng mã ANSI để không bị nhấp nháy
        output = "\033[H" 
        for row in res:
            output += "".join([CHARS[p // 26] for p in row]) + "\n"
        
        print(output)
        
        # Dùng time.sleep để duy trì tốc độ
        time.sleep(sleep_time)

    cap.release()
    # Dọn dẹp sau khi xem xong
    os.remove("a.wav")
    os.remove("v.mp4")

if __name__ == "__main__":
    setup()
    run()
