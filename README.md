### > 2024 1st Semester OpenSourceProgramming Team Project
### > TEAM NAME : 수어 업고 튀어
### > PROJECT NAME : 모두를 위한 실시간 수어-텍스트 변환 통역 서비스(SeouL)
> 
## 👪 팀원
>
>|박다은|**팀장**, UI|
>
>|박윤서|UI|
>
>|정채리|인공지능 모델|
>
>|한은정|웹캠|

***

# SeouL은?

수어는 영어로 Sign Language입니다. 앞의 두 철자인 s,l을 가지고 대한민국의 수도이자 전 세계적으로 유명한 도시인 서울을 떠올릴 수 있도록 SeouL이라는 이름을 붙였습니다.
서울처럼 전세계 사람이 SeouL을 알고 쓸 수 있었으면 좋겠다는 바람을 담은 이름입니다.


## Github 구조

```
train_videos
├── cam
│   ├── face+body+2hands : 표정, 전신, 두 손을 인식해서 캠에 관절들을 띄우는 코드
│   └── only 2hands(blue, yellow) : 두 손의 관절들을 인식해서 캠에 띄우는 코드
├── model
│   └── my_lstm_model.h5 : 전처리된 데이터를 학습시킨 모델
├── 전처리
│   ├── changecsv.py : 원본 영상(video)데이터를 csv파일 형태로 변환시키는 코드
│   ├── learn.py : AI 학습 모델
│   └── processed.py : csv형태의 파일을 npy형태로 변환시켜 라벨링 하는 코드
└── image.py : 학습된 모델을 가지고 캠을 띄우는 코드

```
## 인공지능, 어떻게 사용했을까요?

>![Google Mediapipe](https://github.com/onesilver04/SeouL/assets/141193305/bb47481d-3ddf-43c0-905b-2a710dcf3e23)
>
>저희 팀은 Google의 MediaPipe라는 비전 AI 오픈 소스 프레임워크를 사용했어요.
실시간 비주얼 컴퓨팅 처리 및 해석에 매우 용이한 프레임워크에요.

이 프레임워크를 활용해서 손의 21개의 관절좌표(랜드마크)를 추출했어요.

그 후, 저희는 학습 데이터를 처리했어요. 길을 물어보거나 방향 등을 농인분들이 설명하기 쉬우려면 큰 건물들이 주로 사용될 것을 예상하고
(병원, 약국, 아파트, 학교, 유치원) 총 5가지의 수화에 대해 학습했어요.

## Requirements
* Anaconda 가상환경 활성화
* Install google mediapipe:
  ```shell
  pip install mediapipe opencv-python
  ```
* python version은 3.9가 적당함
  
# SeouL 데모

!!!실행결과 동영상 or 사진 첨부!!!

# 후기

이번 프로젝트는 팀원들에게 정말 새로운 경험이었어요.
기존에 하던 것이 아닌 새로운 기술을 접하고 경험하는 것이기에 팀원 모두가 많이 배워갈 수 있는 기회였던 거 같아요.

후기쓰기~~~~
감사합니다 :)
