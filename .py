import cv2, os, time, urllib.request, winsound, threading, sys

# Buff tốc độ in cho Terminal
sys.stdout.reconfigure(encoding='utf-8')

VIDEO_URL = "https://dn721604.ca.archive.org/0/items/touhou-bad-apple-pv-g-3-c-vev-i-36s/Touhou%20-%20Bad%20Apple%21%21%20%20PV%20%5BG3C-VevI36s%5D.mp4"
AUDIO_URL = "https://ia903102.us.archive.org/26/items/a_20260419/a.wav"
WIDTH, HEIGHT = 160, 80 
CHARS = "@#%*',. " 

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
    
    # Xóa màn hình và ẩn con trỏ chuột (nếu Terminal hỗ trợ)
    sys.stdout.write("\033[2J\033[?25l") 
    
    # Tinh chỉnh sleep_time dựa trên sức mạnh máy tính
    # 160x80 in rất nặng, có thể để 0.015 hoặc thấp hơn
    sleep_time = 0.016 

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            res = cv2.resize(gray, (WIDTH, HEIGHT))
            
            # Dùng list comprehension để tối ưu tốc độ xử lý mảng
            output = "\033[H" + "\n".join([
                "".join([CHARS[int(p * (num_chars - 1) / 255)] for p in row]) 
                for row in res
            ])
            
            sys.stdout.write(output)
            sys.stdout.flush()
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        # Hiện lại con trỏ chuột
        sys.stdout.write("\033[?25h")
        # Giữ lại file để xem lần sau (đỡ phải tải lại)
        print("\n\nShow's over!")

if __name__ == "__main__":
    setup()
    run()
