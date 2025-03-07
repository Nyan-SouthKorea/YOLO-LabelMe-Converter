import cv2

class Draw:
    def draw(self, img_path, label_path, write_path, class_list):
        '''
        YOLO 형식의 데이터셋 그려서 저장
        img_path: 이미지 경로
        label_path: 레이블 경로
        write_path: 이미지 저장 경로
        '''
        color, thick, txt_size = [0,0,255], 2, 1
        # 이미지 읽기
        if isinstance(img_path, str):
            img = cv2.imread(img_path)
        else:
            img = img_path
        img = self.smart_resize(img)
        h, w, c = img.shape
        # 레이블 읽기
        with open(label_path, 'r', encoding='utf-8-sig') as f:
            full_txt = f.read()
        txt_list = full_txt.split('\n')
        # 마지막 엔터 있을 시 제거
        if len(txt_list[-1]) == 0:
            del txt_list[-1]
        # 그리기
        for txt in txt_list:
            class_no, b1, b2, b3, b4 = txt.split(' ')
            class_no, b1, b2, b3, b4 = int(class_no), float(b1), float(b2), float(b3), float(b4)
            class_name = class_list[class_no]
            # pixel 형식으로 변환
            pixel_bbox_nor = self.yolo_to_x1y1x2y2([b1, b2, b3, b4])
            pixel_bbox = self.bbox_nor_to_pix(pixel_bbox_nor, w, h)
            x1, y1, x2, y2 = pixel_bbox
            cv2.rectangle(img, (x1,y1), (x2,y2), color, thick)
            cv2.putText(img, class_name, (x1,y2-3), cv2.FONT_HERSHEY_SIMPLEX, txt_size, color, thick)
        cv2.imwrite(write_path, img)

    def smart_resize(self, img, max_size=1280):
        '''
        최대 변의 길이를 맞추면서 비율을 유지하여 이미지 리사이즈
        img: cv2 이미지
        max_size: 최대 크기
        return: resize된 cv2 이미지 반환
        '''
        h, w, c = img.shape
        if h <= max_size and w <= max_size:
            return img
        if w > h:
            img = cv2.resize(img, (max_size, int(h/w*max_size)))
        else:
            img = cv2.resize(img, (int(w/h*max_size), max_size))
        return img

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

    def bbox_nor_to_pix(self, bbox, w, h):
        '''
        [x, y, x, y] 4개의 원소를 가진 리스트를 int -> f
        w, h: 이미지 사이즈
        '''
        b1, b2, b3, b4 = bbox
        b1, b2, b3, b4 = b1*w, b2*h, b3*w, b4*h
        b1, b2, b3, b4 = int(b1), int(b2), int(b3), int(b4)
        return [b1, b2, b3, b4]

