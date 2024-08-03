import cv2
import mediapipe as mp
import numpy as np 
import pickle 

def image_processed(hand_img):
    # Xử lý ảnh
    # 1. Chuyển từ BGR sang RGB
    img_rgb = cv2.cvtColor(hand_img, cv2.COLOR_BGR2RGB)

    #   2. Lật ảnh theo trục Y
    img_flip = cv2.flip(img_rgb, 1)

    # Truy cập giải pháp MediaPipe
    mp_hands = mp.solutions.hands

    # Khởi tạo Hands
    hands = mp_hands.Hands(static_image_mode=True,
                           max_num_hands=1, min_detection_confidence=0.7)

    # Kết quả
    output = hands.process(img_flip)
    hands.close()

    try:
        data = output.multi_hand_landmarks[0]
        data = str(data)
        data = data.strip().split('\n')
        garbage = ['landmark {', '  visibility: 0.0', '  presence: 0.0', '}']
        without_garbage = [i for i in data if i not in garbage]
        clean = [float(i.strip()[2:]) for i in without_garbage]
        return clean
    except:
        return None

# Tải mô hình
with open('FILEUP2.pkl', 'rb') as f:
    svm = pickle.load(f)

# Bắt đầu chụp video
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Xu lý dữ liệu
    data = image_processed(frame)
    if data is not None:
        data = np.array(data)
        y_pred = svm.predict(data.reshape(-1, 63))
        print(y_pred)
        text = str(y_pred[0])
    else:
        text = "Nothing"
    
    # Hiển thị văn bản
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 100)
    fontScale = 3
    color = (255, 0, 0)
    thickness = 5
    frame = cv2.putText(frame, text, org, font, fontScale, color, thickness, cv2.LINE_AA)    
    
    # Hiện thị video
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
