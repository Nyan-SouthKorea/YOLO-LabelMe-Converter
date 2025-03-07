# YOLO-LabelMe 변환 모듈

## 개요
이 모듈은 YOLO 형식의 라벨 데이터를 LabelMe에서 사용할 수 있는 JSON 형식으로 변환하거나, 반대로 LabelMe JSON 라벨을 YOLO 형식의 TXT로 변환할 수 있도록 설계되었습니다. 또한, 이미지 크기를 스마트하게 조정하는 기능을 제공합니다.

## 기능 설명
### 1. YOLO to LabelMe 변환
YOLO 형식의 라벨 파일을 LabelMe에서 사용할 수 있도록 JSON 파일로 변환합니다.

- 입력 폴더 구조:
  ```
  dataset/
  ├── images/
  │   ├── image1.png
  │   ├── image2.png
  ├── labels/
  │   ├── image1.txt
  │   ├── image2.txt
  ```
- 출력 폴더 구조:
  ```
  dataset/
  ├── output_labelme/
  │   ├── image1.json
  │   ├── image2.json
  ```
- 실행 방법:
  ```bash
  python main.py
  ```
  실행 후 모드 선택에서 `1`을 입력하고, 데이터 경로를 입력하면 변환이 진행됩니다.

### 2. LabelMe to YOLO 변환
LabelMe JSON 라벨을 YOLO 형식의 TXT 파일로 변환합니다.

- 입력 폴더 구조:
  ```
  dataset/
  ├── images/
  │   ├── image1.png
  │   ├── image2.png
  ├── images/
  │   ├── image1.json
  │   ├── image2.json
  ```
- 출력 폴더 구조:
  ```
  dataset/
  ├── output_yolo/
  │   ├── image1.txt
  │   ├── image2.txt
  ```
- 실행 방법:
  ```bash
  python main.py
  ```
  실행 후 모드 선택에서 `2`를 입력하고, 데이터 경로를 입력하면 변환이 진행됩니다.

### 3. 이미지 스마트 리사이즈
입력된 이미지 파일의 크기를 비율을 유지하면서 최대 변의 크기가 지정한 값이 되도록 조정합니다.

- 실행 방법:
  ```bash
  python main.py
  ```
  실행 후 모드 선택에서 `3`을 입력하고, 리사이즈할 이미지의 최대 변 크기를 입력하면 변환이 진행됩니다.

## 주요 클래스 설명
### YOLO_to_LabelMe
- `convert(path)`: 지정된 경로에서 YOLO 라벨을 LabelMe JSON 형식으로 변환합니다.
- `_get_default_json()`: 기본 JSON 템플릿을 반환합니다.
- `_get_default_shape()`: 기본 shape 템플릿을 반환합니다.

### LabelMe_to_YOLO
- `convert(path)`: 지정된 경로에서 LabelMe JSON 라벨을 YOLO TXT 형식으로 변환합니다.
- `_draw_sample(goal_ea=-1)`: 변환된 YOLO 라벨을 이미지에 그려서 시각적으로 확인할 수 있도록 합니다.

### Image_smart_resize
- `convert(path)`: 지정된 경로에서 이미지의 크기를 자동으로 조정합니다.
- `_smart_resize(img, max_size)`: 최대 변의 길이를 유지하며 이미지 크기를 조정합니다.

## 필수 라이브러리 설치
이 모듈을 사용하려면 다음의 Python 라이브러리가 필요합니다:
```bash
pip install natsort opencv-python tqdm
```

## 실행 예제
```bash
python main.py
```
실행 후 변환 모드를 선택하고 데이터 경로를 입력하면 변환이 진행됩니다.

## 업데이트 로그
- **v1 (2025-03-05)**: 초기 개발 버전 배포

## 주의 사항
- YOLO와 LabelMe의 클래스 목록이 일치해야 합니다. 변환 전, 올바른 클래스 리스트를 입력했는지 확인하세요.
- LabelMe JSON 변환 시 좌표가 올바르게 변환되는지 확인하려면 샘플 이미지를 생성해 검토하는 것이 좋습니다.
- 이미지 리사이즈 기능을 사용할 때, 원본 이미지가 손실되지 않도록 백업 후 사용하세요.
