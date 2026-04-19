import cv2
import os
import time
import urllib.request
import winsound
import threading
import sys

# Đảm bảo in Unicode mượt mà
sys.stdout.reconfigure(encoding='utf-8')

# Cấu hình - 160x80 là độ phân giải cực cao cho Terminal, rất nét!
VIDEO_URL = "https://dn721604.ca.archive.org/0/items/touhou-bad-apple-pv-g-3-c-vev-i-36s/Touhou%20-%20Bad%20Apple%21%21%20%20PV%20%5BG3C-VevI36s%5D.mp4"
AUDIO_URL = "https://ia903102.us.archive.org/26/items/a_20260419/a.wav"
WIDTH, HEIGHT = 160, 80 
CHARS = "@#%*',. " # Luôn nên có khoảng trắng ở cuối cho vùng sáng nhất

def setup():
    for url, name in [(AUDIO_URL, "a.wav"), (VIDEO_URL, "v.mp4")]:
        if not os.path.exists(name):
            print(f"Đang tải {name}...")
            urllib.request.urlretrieve(url, name)

def run():
    if not os.path.exists("v.mp4"): return
    
    cap = cv2.VideoCapture("v.mp4")
    num_chars = len(CHARS)
    
    # Phát nhạc trên luồng riêng
    threading.Thread(target=lambda: winsound.PlaySound("a.wav", winsound.SND_FILENAME)).start()
    
    print("\033[2J") # Xóa màn hình
    
    # 160x80 in rất nặng, dùng 0.01s để bù trừ thời gian xử lý CPU
    sleep_time = 0.018 
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # Xử lý hình ảnh
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = cv2.resize(gray, (WIDTH, HEIGHT))
        
        # ANSI Escape đưa con trỏ về đầu (Không nhấp nháy)
        output = "\033[H" 
        
        # FIX LỖI TẠI ĐÂY: Dùng quy tắc tỉ lệ thay vì số 26 cố định
        for row in res:
            line = "".join([CHARS[int(p * (num_chars - 1) / 255)] for p in row])
            output += line + "\n"
        
        sys.stdout.write(output)
        sys.stdout.flush()
        
        time.sleep(sleep_time)

    cap.release()
    # Dọn dẹp sau khi chạy xong
    try:
        os.remove("a.wav")
        os.remove("v.mp4")
    except:
        pass

if __name__ == "__main__":
    setup()
    run()
