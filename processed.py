import pandas as pd
import numpy as np

# CSV 파일 불러오기
file_path = 'processed_output/normalized_kindergarten_data.csv'  # 변경할 CSV 파일 경로
data = pd.read_csv(file_path)

# 프레임 번호 제거 및 Numpy 배열로 변환
coordinates = data.drop(columns=['frame']).values

# 라벨링 (예: "유치원"이라는 문자열 라벨)
label = '유치원'  # 변경할 라벨
labels = np.array([[label]] * coordinates.shape[0], dtype=object)

# 데이터와 라벨 합치기
labeled_data = np.hstack((coordinates, labels))

# npy 파일로 저장
output_file = 'npy/kindergarten_data_with_string_label.npy'  # 변경할 npy 파일 경로
np.save(output_file, labeled_data, allow_pickle=True)

print(f"Data saved to {output_file}")