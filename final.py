import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from PIL import ImageFont, ImageDraw, Image
import time

# 수어 단어 리스트 5개 추출
words = ['병원', '유치원', '약국', '아파트', '학교']

# 모델 로드
model_15 = load_model('model/my_lstm_model_15.h5') # 경로 설정 주의
model = load_model('model/my_lstm_model.h5') # 경로 설정 주의

# MediaPipe Hands 초기화
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# 한글 폰트 설정
fontpath = "C:/WINDOWS/Fonts/MALANGMALANGR.TTF"  # 사용할 한글 폰트 경로
font = ImageFont.truetype(fontpath, 32)

# 웹캠 열기
cap = cv2.VideoCapture(0)

# 손가락 관절 마디 색상 설정
landmark_drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2)  # 관절 꼭짓점: 노란색으로 설정
connection_drawing_spec = mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)  # 관절 라인: 파란색으로 설정
cv2.namedWindow('Sign Language Recognition', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Sign Language Recognition', 1200, 600) # 캠 창 크기 조절

# 초기 변수 설정
landmark_history = []
capture_duration = 1  # 예측 단어 뜨는 시간 조정
last_capture_time = time.time()
predicted_word = ""  # 마지막으로 예측된 단어

with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        # 프레임 읽기
        success, image = cap.read()
        if not success:
            continue
        
        # 이미지를 RGB로 변환하고 좌우 반전
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # 손 인식 결과 받기
        results = hands.process(image)

        # 이미지를 다시 BGR로 변환 (OpenCV는 BGR을 사용)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 손의 랜드마크 좌표를 배열로 변환
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
                landmark_history.append(landmarks)

                # 손의 랜드마크 그리기 (관절 마디는 노란색, 연결선은 파란색으로 설정)
                mp_drawing.draw_landmarks(
                    image, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS, 
                    landmark_drawing_spec,
                    connection_drawing_spec
                )

        # 일정 시간 동안 데이터를 수집한 후 예측 수행
        current_time = time.time()
        if current_time - last_capture_time >= capture_duration:
            if landmark_history:
                # 평균 랜드마크 계산
                avg_landmarks = np.mean(landmark_history, axis=0)
                avg_landmarks = np.expand_dims(avg_landmarks, axis=0)

                # 모델 예측
                prediction_15 = model_15.predict(avg_landmarks)
                prediction = model.predict(avg_landmarks)

                # 예측 결과와 정확도 비교
                predicted_label_15 = np.argmax(prediction_15, axis=1)[0]
                confidence_15 = prediction_15[0][predicted_label_15]

                predicted_label = np.argmax(prediction, axis=1)[0]
                confidence = prediction[0][predicted_label]

                if predicted_label_15 == words.index('아파트'):  # 아파트인 경우 model_15의 예측 사용
                    predicted_word = words[predicted_label_15]
                elif predicted_label == words.index('학교'):  # 학교인 경우 model의 예측 사용
                    predicted_word = words[predicted_label]
                else:
                    # 정확도가 높은 예측을 선택
                    if confidence_15 > confidence:
                        predicted_word = words[predicted_label_15]
                    else:
                        predicted_word = words[predicted_label]

            # 다음 예측을 위해 초기화
            landmark_history = []
            last_capture_time = current_time

        # 예측된 단어를 화면에 계속 표시
        if predicted_word:
            image_pil = Image.fromarray(image)
            draw = ImageDraw.Draw(image_pil)
            draw.text((200, 400), f'Prediction: {predicted_word}', font=font, fill=(255, 255, 255))
            image = np.array(image_pil)

        # 화면에 출력
        cv2.imshow('Sign Language Recognition', image)

        # 'q'를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
