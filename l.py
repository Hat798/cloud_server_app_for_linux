import cv2, os, time, subprocess, threading, sys

# Ép hệ thống nhận diện mã ANSI
os.system('') 
sys.stdout.reconfigure(encoding='utf-8')

# Link dữ liệu (Dùng lại link của bạn)
VIDEO_URL = "https://dn721604.ca.archive.org/0/items/touhou-bad-apple-pv-g-3-c-vev-i-36s/Touhou%20-%20Bad%20Apple%21%21%20%20PV%20%5BG3C-VevI36s%5D.mp4"
AUDIO_URL = "https://ia903102.us.archive.org/26/items/a_20260419/a.wav"

WIDTH, HEIGHT = 160, 80 
CHARS = "@#%*',. " 

def setup():
    if not os.path.exists("v.mp4"):
        print("Đang tải video...")
        import urllib.request
        urllib.request.urlretrieve(VIDEO_URL, "v.mp4")
    if not os.path.exists("a.wav"):
        print("Đang tải nhạc...")
        import urllib.request
        urllib.request.urlretrieve(AUDIO_URL, "a.wav")

def run():
    cap = cv2.VideoCapture("v.mp4")
    num_chars = len(CHARS)
    
    # PHÁT NHẠC TRÊN LINUX: Dùng ffplay (Yêu cầu đã cài ffmpeg)
    # Nếu máy bạn dùng 'aplay' hoặc 'paplay' thì thay thế lệnh tương ứng
    try:
        subprocess.Popen(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", "a.wav"])
    except FileNotFoundError:
        print("Cảnh báo: Hãy cài ffmpeg để nghe được nhạc (sudo apt install ffmpeg)")

    sys.stdout.write("\033[2J\033[?25l")
    
    # Linux terminal thường nhanh hơn Windows, thử để sleep thấp
    sleep_time = 0.025 

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            res = cv2.resize(gray, (WIDTH, HEIGHT))
            
            output = "\033[H" + "\n".join([
                "".join([CHARS[min(int(p * num_chars / 256), num_chars - 1)] for p in row]) 
                for row in res
            ])
            
            sys.stdout.write(output)
            sys.stdout.flush()
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        sys.stdout.write("\033[?25h")
        print("\nHoàn tất!")

if __name__ == "__main__":
    setup()
    run()
