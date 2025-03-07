import json

class Bbox:
    def x1y1x2y2_to_yolo(self, bbox):
        '''
        [x1, y1, x2, y2] -> [center x, center y, x width, y width] 변환
        bbox: [x1, y1, x2, y2]
        '''
        rnd = 5
        x1, y1, x2, y2 = bbox
        center_x = (x1+x2)/2
        center_y = (y1+y2)/2
        width = x2-x1
        height = y2-y1
        center_x, center_y, width, height = round(center_x, rnd), round(center_y, rnd), round(width, rnd), round(height, rnd)
        bbox = [center_x, center_y, width, height]
        return bbox

    def yolo_to_x1y1x2y2(self, bbox):
        '''
        [center x, center y, x width, y width] -> [x1, y1, x2, y2] 변환
        bbox: [center x, center y, x width, y width]
        '''
        center_x, center_y, width, height = bbox
        x1 = center_x - (width/2)
        y1 = center_y - (height/2)
        x2 = x1 + width
        y2 = y1 + height
        bbox = [x1, y1, x2, y2]
        return bbox

    def bbox_pix_to_nor(self, bbox, w, h):
        '''
        [x, y, x, y] 픽셀값 bbox를 0 ~ 1 정규화된 상태로 변환
        bbox: 입력되는 bbox
        w, h: 이미지 사이즈
        '''
        b1, b2, b3, b4 = bbox
        b1, b2, b3, b4 = b1/w, b2/h, b3/w, b4/h
        round_no = 5
        b1, b2, b3, b4 = round(b1, round_no), round(b2, round_no), round(b3, round_no), round(b4, round_no)
        return [b1, b2, b3, b4]

    def bbox_nor_to_pix(self, bbox, w, h):
        '''
        [x, y, x, y] 4개의 원소를 가진 리스트를 int -> f
        w, h: 이미지 사이즈
        '''
        b1, b2, b3, b4 = bbox
        b1, b2, b3, b4 = b1*w, b2*h, b3*w, b4*h
        b1, b2, b3, b4 = int(b1), int(b2), int(b3), int(b4)
        return [b1, b2, b3, b4]

    def write_label(self, bbox_list, label_path):
        '''
        [class_no, b1, b2, b3, b4] 형식의 YOLO label list를 txt로 저장
        '''
        with open(label_path, 'w') as f:
            f.write('')
            for i, bbox in enumerate(bbox_list):
                if i == len(bbox_list)-1: enter = ''
                else: enter = '\n'
                class_no, b1, b2, b3, b4 = bbox
                f.write(f'{class_no} {b1} {b2} {b3} {b4}{enter}')

    # YOLO 레이블 읽고 저장하기
    def read_label(self, label_path):
        '''
        txt로 된 YOLO label을 읽어서 bbox 형태로 반환
        label_path: 레이블 경로
        return: [[class_no, b1, b2, b3, b4], ...,]
        '''
        bbox_list = []
        with open(label_path, 'r', encoding='utf-8-sig') as f:
            full_txt = f.read()
        txt_list = full_txt.split('\n')
        if len(txt_list[-1]) == 0:
            del txt_list[-1]
        for txt in txt_list:
            class_no, b1, b2, b3, b4 = txt.split(' ')
            class_no, b1, b2, b3, b4 = int(class_no), float(b1), float(b2), float(b3), float(b4)
            b1, b2, b3, b4 = max(0,b1), max(0,b2), max(0,b3), max(0,b4)
            b1, b2, b3, b4 = min(1,b1), min(1,b2), min(1,b3), min(1,b4)
            bbox_list.append([class_no, b1, b2, b3, b4])
        return bbox_list
