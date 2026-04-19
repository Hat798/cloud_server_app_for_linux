import cv2
import os
import time
import winsound
import threading

# Cấu hình: Đảm bảo 2 file này nằm cùng thư mục với file .py
VIDEO_FILE = "v.mp4" 
AUDIO_FILE = "a.wav"
WIDTH, HEIGHT = 80, 40
CHARS = "@#%*+=-:,. "

def run():
    # Kiểm tra file trước khi chạy
    if not os.path.exists(VIDEO_FILE) or not os.path.exists(AUDIO_FILE):
        print(f"Lỗi: Không tìm thấy {VIDEO_FILE} hoặc {AUDIO_FILE} trong thư mục!")
        return

    cap = cv2.VideoCapture(VIDEO_FILE)
    
    # Phát nhạc nội bộ
    threading.Thread(target=lambda: winsound.PlaySound(AUDIO_FILE, winsound.SND_FILENAME)).start()
    
    print("\033[2J") # Xóa màn hình
    
    # Tinh chỉnh sleep_time cho khớp với máy của bạn
    sleep_time = 0.03112 
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # Xử lý ASCII
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = cv2.resize(gray, (WIDTH, HEIGHT))
        
        output = "\033[H" 
        for row in res:
            output += "".join([CHARS[p // 26] for p in row]) + "\n"
        
        print(output)
        time.sleep(sleep_time)

    cap.release()
    # Ở bản nội bộ, mình KHÔNG nên dùng os.remove để có thể xem lại nhiều lần
    print("\nĐã phát xong!")

if __name__ == "__main__":
    run()
