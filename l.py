import cv2
import os
import time
import urllib.request
import threading
import sys
import subprocess

# Cấu hình
VIDEO_URL = "https://dn721604.ca.archive.org/0/items/touhou-bad-apple-pv-g-3-c-vev-i-36s/Touhou%20-%20Bad%20Apple%21%21%20%20PV%20%5BG3C-VevI36s%5D.mp4"
AUDIO_URL = "https://ia903102.us.archive.org/26/items/a_20260419/a.wav"
WIDTH, HEIGHT = 120, 60  # Tăng một chút độ phân giải cho nét
CHARS = "@#%*+=-:. "

def play_audio(file_path):
    """Phát nhạc dựa trên hệ điều hành"""
    if sys.platform == "win32":
        import winsound
        winsound.PlaySound(file_path, winsound.SND_FILENAME)
    elif sys.platform == "darwin":  # macOS
        subprocess.call(["afplay", file_path])
    else:  # Linux
        # Thử dùng ffplay (phổ biến nhất)
        try:
            subprocess.call(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", file_path])
        except FileNotFoundError:
            print("\nLỗi: Linux cần 'ffmpeg' để phát nhạc. Hãy cài: sudo apt install ffmpeg")

def setup():
    for url, name in [(AUDIO_URL, "a.wav"), (VIDEO_URL, "v.mp4")]:
        if not os.path.exists(name):
            print(f"Đang tải {name}...")
            urllib.request.urlretrieve(url, name)

def run():
    cap = cv2.VideoCapture("v.mp4")
    if not cap.isOpened():
        print("Không thể mở file video!")
        return

    # Khởi tạo luồng phát nhạc
    audio_thread = threading.Thread(target=play_audio, args=("a.wav",), daemon=True)
    audio_thread.start()

    # ANSI chuẩn để xóa màn hình và ẩn con trỏ
    sys.stdout.write("\033[2J\033[?25l")
    
    num_chars = len(CHARS)
    start_time = time.time()
    frame_count = 0
    fps = 30  # FPS gốc của Bad Apple

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            # Xử lý ASCII
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            res = cv2.resize(gray, (WIDTH, HEIGHT))
            
            # Ghép khung hình bằng join để tối ưu tốc độ
            output = "\033[H"
            rows = []
            for row in res:
                rows.append("".join([CHARS[min(int(p * num_chars / 256), num_chars - 1)] for p in row]))
            output += "\n".join(rows)
            
            sys.stdout.write(output)
            sys.stdout.flush()

            # Đồng bộ thời gian thực (tránh lag do render chậm)
            frame_count += 1
            elapsed = time.time() - start_time
            target_time = frame_count / fps
            sleep_duration = target_time - elapsed
            if sleep_duration > 0:
                time.sleep(sleep_duration)

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        sys.stdout.write("\033[?25h\n") # Hiện lại con trỏ
        # Dọn dẹp file
        for f in ["a.wav", "v.mp4"]:
            if os.path.exists(f): os.remove(f)

if __name__ == "__main__":
    setup()
    run()
