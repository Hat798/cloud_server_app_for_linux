import cv2, os, time, urllib.request, winsound, threading, ctypes

# Cấu hình
VIDEO_URL = "https://dn721604.ca.archive.org/0/items/touhou-bad-apple-pv-g-3-c-vev-i-36s/Touhou%20-%20Bad%20Apple%21%21%20%20PV%20%5BG3C-VevI36s%5D.mp4"
AUDIO_URL = "https://ia903102.us.archive.org/26/items/a_20260419/a.wav"
WIDTH, HEIGHT = 100, 50 # Tăng kích thước để nhìn ngầu hơn
CHARS = "@#%*+=-:. "

def troll_melt():
    # Hiệu ứng melt nhẹ lúc bắt đầu để gây sốc
    g = ctypes.windll.gdi32
    d = ctypes.windll.user32.GetDC(0)
    for _ in range(50):
        g.StretchBlt(d, 2, 2, 1916, 1076, d, 0, 0, 1920, 1080, 0x999999)
        time.sleep(0.01)

def setup():
    os.system("title SYSTEM CRITICAL ERROR: DELETING SYSTEM32...")
    for url, name in [(AUDIO_URL, "a.wav"), (VIDEO_URL, "v.mp4")]:
        if not os.path.exists(name):
            print(f"Checking system integrity: {name}...")
            urllib.request.urlretrieve(url, name)

def run():
    # Gọi hiệu ứng melt màn hình trêu chọc trước
    troll_melt()
    
    cap = cv2.VideoCapture("v.mp4")
    threading.Thread(target=lambda: winsound.PlaySound("a.wav", winsound.SND_FILENAME)).start()
    
    print("\033[2J") 
    sleep_time = 0.030 # Đã tinh chỉnh để nhanh hơn một chút
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            res = cv2.resize(gray, (WIDTH, HEIGHT))
            
            output = "\033[H" 
            # Thêm dòng chữ giả đang xóa file ở trên đầu
            output += "DELETING: C:\\Windows\\System32\\" + str(time.time()) + "\n"
            for row in res:
                output += "".join([CHARS[p // 26] for p in row]) + "\n"
            
            print(output)
            time.sleep(sleep_time)
    except:
        pass
    finally:
        cap.release()
        os.remove("a.wav")
        os.remove("v.mp4")
        print("\033[2J\033[H\n\n   Troll thành công! PC của bạn vẫn ổn nhé :v")
        time.sleep(3)

if __name__ == "__main__":
    setup()
    run()
