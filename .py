import cv2, os, time, urllib.request, winsound, threading, sys

# Tối ưu hóa in ấn cho Terminal
sys.stdout.reconfigure(encoding='utf-8')

WIDTH, HEIGHT = 160, 80 
CHARS = "@#%*',. " # Bạn có thể thay bằng bộ ký tự Unicode tùy thích
VIDEO_URL = "https://dn721604.ca.archive.org/0/items/touhou-bad-apple-pv-g-3-c-vev-i-36s/Touhou%20-%20Bad%20Apple%21%21%20%20PV%20%5BG3C-VevI36s%5D.mp4"
AUDIO_URL = "https://ia903102.us.archive.org/26/items/a_20260419/a.wav"

def setup():
    for url, name in [(AUDIO_URL, "a.wav"), (VIDEO_URL, "v.mp4")]:
        if not os.path.exists(name):
            print(f"Đang tải {name}...")
            urllib.request.urlretrieve(url, name)

def run():
    if not os.path.exists("v.mp4"): return
    cap = cv2.VideoCapture("v.mp4")
    num_chars = len(CHARS)
    
    # Phát nhạc
    threading.Thread(target=lambda: winsound.PlaySound("a.wav", winsound.SND_FILENAME)).start()
    
    # Ẩn con trỏ chuột và xóa màn hình
    sys.stdout.write("\033[?25l\033[2J")
    
    # 160x80 in rất nặng, cần sleep thấp để bù đắp thời gian xử lý
    sleep_time = 0.015 

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            res = cv2.resize(gray, (WIDTH, HEIGHT))
            
            # ANSI Escape đưa con trỏ về đầu
            output = "\033[H"
            
            # --- CÔNG THỨC AN TOÀN TUYỆT ĐỐI ---
            for row in res:
                line = "".join([CHARS[min(int(p * num_chars / 256), num_chars - 1)] for p in row])
                output += line + "\n"
            
            sys.stdout.write(output)
            sys.stdout.flush()
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        sys.stdout.write("\033[?25h") # Hiện lại con trỏ chuột
        print("\n\nFinish!")

if __name__ == "__main__":
    setup()
    run()
