import cv2
import os
from datetime import datetime
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# 사진 저장 경로 설정
save_path = './captured_images/'
os.makedirs(save_path, exist_ok=True)

# 카메라 캡처 객체 생성
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Camera could not be opened!")
    exit()

# Google Drive 인증
gauth = GoogleAuth()
gauth.LoadClientConfigFile("C:/Users/dongc/Downloads/client_secret_999296973226-84926e83a8u0v304rhsahcluum8q149b.apps.googleusercontent.com.json")  # 클라이언트 ID JSON 파일 경로 지정
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# 구글 드라이브 폴더 ID
folder_id = '1p53RbFU6ZPfiZpdAHH8-6nHIxkZJMeMY'  # 여기에 실제 폴더 ID를 입력하세요.

def upload_to_drive(file_path):
    try:
        file_drive = drive.CreateFile({
            'title': os.path.basename(file_path),
            'parents': [{'id': folder_id}]
        })
        file_drive.SetContentFile(file_path)
        file_drive.Upload()
        print(f'{file_path} uploaded to Google Drive.')
        
        # 업로드 성공 시 로컬 파일 삭제
        os.remove(file_path)
        print(f'{file_path} deleted from local storage.')
    except Exception as e:
        print(f'Failed to upload {file_path} to Google Drive. Error: {e}')

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # 2초마다 사진 저장
        if int(time.time()) % 2 == 0:
            filename = datetime.now().strftime('%Y%m%d_%H%M%S') + '.jpg'
            file_path = os.path.join(save_path, filename)
            cv2.imwrite(file_path, frame)
            time.sleep(1)  # 파일이 중복으로 저장되는 문제 방지
            
            # 파일 저장 후 약간의 지연 시간 추가
            time.sleep(0.5)  # 0.5초 대기하여 파일이 완전히 저장되도록 함

            # 사진을 Google Drive에 업로드
            upload_to_drive(file_path)

finally:
    cap.release()
