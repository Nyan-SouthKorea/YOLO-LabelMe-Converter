class Print_manual:
    def __init__(self):
        # 기본 매뉴얼 출력
        inform_print = '''
        2025-03-05 v1
        YOLO와 LabelME 간의 데이터 형식으로 서로 Switch 할 수 있다.

        YOLO 형식의 데이터셋 경로:
            ㄴ images
                1.png
            ㄴ labels
                1.txt

        LabelMe 형식의 데이터셋 경로:
            ㄴ images
                1.png
                1.json

        변경 실행 시, 데이터셋 폴더와 같은 경로에 output이라는 폴더가 새로 생성되고 그 안에 레이블들이 새로 저장된다.
        '''
        print(inform_print)