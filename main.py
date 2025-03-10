# 기본
import os
import json
import time
import random

# pip install 
from natsort import natsorted
import cv2
from tqdm import tqdm

# custom
from utils.bbox import Bbox
from utils.print import Print_manual
from utils.tools import name, class_list_request, is_img_file, is_label_file
from utils.draw import Draw
from utils.release import ReleaseNote

ReleaseNote()

# 모듈 개발
class YOLO_to_LabelMe:
    def __init__(self):
        '''
        YOLO 형식의 label을 LabelMe에서 호환되는 json으로 변경해줌
        '''
        self.output_folder = 'output_labelme'
        self.b = Bbox()
    
    def convert(self, path):
        # 폴더 생성
        os.makedirs(f'{path}/{self.output_folder}', exist_ok=True)

        # class_list 요청
        class_list = class_list_request()
        
        # for문 시작
        img_list = natsorted(os.listdir(f'{path}/images'))
        for img_name in tqdm(img_list, desc='레이블 생성 중...'):            
            try:
                # 이미지 유효성 확인
                if is_img_file(img_name) == False:
                    continue

                # 이미지 정보 취득
                img = cv2.imread(f'{path}/images/{img_name}')
                h, w, _ = img.shape

                # 레이블 읽기
                label_name = f'{name(img_name)}.txt'
                with open(f'{path}/labels/{label_name}', 'r', encoding='utf-8-sig') as f:
                    txt_split_by_enter = f.read().split('\n')
                # 맨 뒤 빈 텍스트 삭제 처리
                if txt_split_by_enter[-1] == '':
                    del txt_split_by_enter[-1]
                # json 형식 shape 생성
                shape_list = []
                for splited_txt in txt_split_by_enter:
                    class_no, b1, b2, b3, b4 = splited_txt.split(' ')
                    class_no, b1, b2, b3, b4 = int(class_no), float(b1), float(b2), float(b3), float(b4)
                    new_shape = self._get_default_shape()
                    # 레이블 이름 입력
                    new_shape['label'] = class_list[class_no]

                    # bbox 계산
                    x1, y1, x2, y2 = self.b.yolo_to_x1y1x2y2([b1, b2, b3, b4])
                    x1, y1, x2, y2 = self.b.bbox_nor_to_pix([x1, y1, x2, y2], w, h)
                    new_shape['points'] = [[x1,y1], [x2,y2]]
                    shape_list.append(new_shape)
            except Exception as e:
                print(f'{img_name}:{e}, 문제 class 번호:{class_no}')
                continue
                
            
            # json 필요 정보 기입
            default_json = self._get_default_json()
            default_json['imageHeight'] = h
            default_json['imageWidth'] = w
            default_json['shapes'] = shape_list
            default_json['imagePath'] = img_name

            # json 저장
            with open(f'{path}/{self.output_folder}/{name(img_name)}.json', 'w') as f:
                json.dump(default_json, f, indent=4)

    def _get_default_json(self):
        default_data = {'version':'5.7.0', 
                        'flags':{},
                        'shapes':[],
                        'imagePath':'',
                        'imageData':None,
                        'imageHeight':0,
                        'imageWidth':0}
        return default_data
    
    def _get_default_shape(self):
        default_shapes = {'label':'',
                          'points':[[0,0], [0,0]],
                          'group_id':None,
                          'description':'',
                          'shape_type':'rectangle',
                          'flags':{},
                          'mask':None}
        return default_shapes

class LabelMe_to_YOLO:
    def __init__(self):
        '''
        LabelMe에서 형식의 label을 YOLO txt 레이블로 변경해줌
        '''
        self.output_folder = 'output_yolo'
        self.b = Bbox()

    def convert(self, path):
        # 폴더 생성
        os.makedirs(f'{path}/{self.output_folder}', exist_ok=True)

        # class_list 요청
        self.class_list = class_list_request()

        # for문 시작
        print('변환 시작')
        for json_name in tqdm(os.listdir(path)):
            # json파일만 읽기
            if is_label_file(json_name) == False:
                continue
        
            # json 데이터 분석
            with open(f'{path}/{json_name}', 'r') as f:
                json_data = json.load(f)

            # bbox_list 생성
            shape_list = json_data['shapes']
            h, w = json_data['imageHeight'], json_data['imageWidth']
            bbox_list = []
            for shapes in shape_list:
                class_name = shapes['label']
                points_1, points_2 = shapes['points']
                x1, y1, x2, y2 = self._fix_bbox_order(points_1, points_2)
                x1, y1, x2, y2 = self.b.bbox_pix_to_nor([x1, y1, x2, y2], w, h)
                b1, b2, b3, b4 = self.b.x1y1x2y2_to_yolo([x1, y1, x2, y2])
                class_no = self.class_list.index(class_name)
                bbox_list.append([class_no, b1, b2, b3, b4])

            # YOLO 형식 txt 레이블 저장
            self.b.write_label(bbox_list, f'{path}/{self.output_folder}/{name(json_name)}.txt')

        # 이빨 빠진 빈 레이블 txt 생성
        self._make_empty_txt(path)
        
        # 샘플로 100장만 그리기
        input_command = input('그림 그리기를 원하면 엔터, 원하지 않으면 n를 입력하시오. 샘플로 그릴 이미지의 개수를 입력해도 됩니다.: ')
        if input_command == 'n' or input_command == 'N':
            pass
        elif input_command == '':
            self._draw_sample()
        else:
            # 숫자인지 검사
            try: 
                goal_ea = int(input_command)
                self._draw_sample(goal_ea)
            except:
                print('이상한 입력 감지됨. 프로그램 종료.')

    def _make_empty_txt(self, path):
        '''YOLO 레이블이 없는 것은 빈 텍스트를 만든다'''
        # 이미지 리스트 생성
        img_list = []
        for file_name in os.listdir(path):
            if is_img_file(file_name) == True:
                img_list.append(file_name)
        
        # 빈 레이블 생성
        for img_name in img_list:
            label_name = f'{name(img_name)}.txt'
            label_path = f'{path}/{self.output_folder}/{label_name}'
            if os.path.exists(label_path) == False:
                with open(label_path, 'w') as f:
                    f.write('')
            
    def _fix_bbox_order(self, points_1, points_2):
        '''LabelMe는 x1과 x2의 순서가 멋대로이다. 이 것을 바로잡아준다'''
        x_tmp1, y_tmp1 = points_1
        x_tmp2, y_tmp2 = points_2
        x1 = min(x_tmp1, x_tmp2)
        x2 = max(x_tmp1, x_tmp2)
        y1 = min(y_tmp1, y_tmp2)
        y2 = max(y_tmp1, y_tmp2)
        return x1, y1, x2, y2
        

    def _draw_sample(self, goal_ea=-1):
        '''최대 n장 까지만 샘플로 그려서 반환'''
        # 그리기 객체 선언
        d = Draw()

        # 폴더 생성
        os.makedirs(f'{path}/draw', exist_ok=True)

        # 이미지만 걸러내기
        file_list = os.listdir(path)
        img_list = []
        for file in file_list:
            if is_img_file(file) == True:
                img_list.append(file)
        
        # n장만 그리기 진행
        random.shuffle(img_list)
        print('지정된 개수 만큼 그리기 시작')
        # 샘플링
        if goal_ea == -1:
            pass
        else:
            img_list = img_list[:goal_ea]
        
        # 그리기
        for img_name in tqdm(img_list):
            label_name = f'{name(img_name)}.txt'
            d.draw(f'{path}/{img_name}', f'{path}/{self.output_folder}/{label_name}', f'{path}/draw/{img_name}', self.class_list)

class Image_smart_resize:
    def convert(self, path):
        input_txt = input('이미지 한 변의 최대 사이즈를 입력하세요(미 입력시 default: 640): ')
        # 유효성 검사
        if input_txt == '':
            input_txt = 640
        try:
            input_size = int(input_txt)
        except:
            print('잘못된 값이 입력되었습니다. 다시 시작하세요')
            time.sleep(5)
            exit()
        
        # 새로운 폴더 생성
        output_folder = 'resized_output'
        os.makedirs(f'{path}/{output_folder}', exist_ok=True)

        # 이미지 불러오기
        file_list = os.listdir(path)
        img_list = []
        for file in file_list:
            if is_img_file(file) == True:
                img_list.append(file)
        
        # 리사이즈 진행 후 저장
        print('리사이즈 시작')
        for img_name in tqdm(img_list):
            img = cv2.imread(f'{path}/{img_name}')
            resized_img = self._smart_resize(img, input_size)
            cv2.imwrite(f'{path}/{output_folder}/{img_name}', resized_img)

    def _smart_resize(self, img, max_size=1280):
        '''
        최대 변의 길이를 맞추면서 비율을 유지하여 이미지 리사이즈
        img: cv2 이미지
        max_size: 최대 크기
        return: resize된 cv2 이미지 반환
        '''
        h, w, c = img.shape
        if w > h:
            img = cv2.resize(img, (max_size, int(h/w*max_size)))
        else:
            img = cv2.resize(img, (int(w/h*max_size), max_size))
        return img

class Auto_flip:
    '''
    좌/우 플립 증강을 해주는 모듈
    '''
    def __init__(self):
        self.b = Bbox()
        self.d = Draw()

    def run(self, path):
        # 플립 변환
        print('플립 증강 중...')
        for img_name in tqdm(os.listdir(f'{path}/images')):
            # 유효성 검사
            if is_img_file(img_name) == False:
                continue

            # 이미지 취득
            img = cv2.imread(f'{path}/images/{img_name}')
            # 이미지 플립
            flip_img = self._img_flip(img)

            # 레이블 취득
            label_name = f'{name(img_name)}.txt'
            bbox_list = self.b.read_label(f'{path}/labels/{label_name}')
            # 레이블 플립
            flip_bbox_list = self._bbox_flip(bbox_list)

            # 이미지 저장
            flip_name = f'{name(img_name)}_flip'
            cv2.imwrite(f'{path}/images/{flip_name}.png', flip_img)

            # 레이블 저장
            self.b.write_label(flip_bbox_list, f'{path}/labels/{flip_name}.txt')

        # 그리기
        print('그림을 그리기 위해 class_list를 요구합니다.')
        class_list = class_list_request()

        # 폴더 생성
        os.makedirs(f'{path}/draw_flip', exist_ok=True)

        # 진행
        print('원본 + 증강 이미지 그리는 중...')
        for img_name in tqdm(os.listdir(f'{path}/images')):  
            label_name = f'{name(img_name)}.txt'
            self.d.draw(f'{path}/images/{img_name}', f'{path}/labels/{label_name}', f'{path}/draw_flip/{img_name}', class_list)

    def _img_flip(self, img):
        return cv2.flip(img, 1)
    
    def _bbox_flip(self, bbox_list):
        flip_bbox_list = []
        for class_no, b1, b2, b3, b4 in bbox_list:
            x1, y1, x2, y2 = self.b.yolo_to_x1y1x2y2([b1, b2, b3, b4])
            new_x1 = 1 - x2
            new_x2 = 1 - x1
            b1, b2, b3, b4 = self.b.x1y1x2y2_to_yolo([new_x1, y1, new_x2, y2])
            flip_bbox_list.append([class_no, b1, b2, b3, b4])
        return flip_bbox_list


Print_manual()

# 모드 입력 받기
mode = input('모드를 선택하세요. 1: YOLO to LabelMe | 2: LabelMe to YOLO | 3: 이미지 스마트 리사이즈 | 4: 좌우 플립 증강 = ')
if not mode in ['1', '2', '3', '4']:
    print('모드를 잘 못 선택했습니다. 프로그램을 다시 실행하세요.')
    time.sleep(5)
    exit()

print(f'현재 디렉토리 상태: {os.listdir("./")}')
path = input('데이터 경로를 입력하세요: ')
if mode == '1':
    YOLO_to_LabelMe().convert(path)
elif mode == '2':
    LabelMe_to_YOLO().convert(path)
elif mode == '3':
    Image_smart_resize().convert(path)
elif mode == '4':
    Auto_flip().run(path)
else:
    print('이상한 입력값이 입력되었습니다. 프로그램이 종료됩니다.')
    time.sleep(5)