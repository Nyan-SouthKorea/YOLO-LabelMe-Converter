class ReleaseNote:
    def __init__(self):
        release_note = '''
        [릴리즈 노트]
        250308_v1
        - 모든 파일명을 검사할 때 유효성 검사(시스템 파일 때문에 에러 나는 부분 방지)
            - 이미지 필터링 기준: png, jpg, jpeg, gif
            - 레이블 필터링 기준: txt, json
        - Tools 객체 말고 함수의 집합으로 변경. 모든 코드에서 glabal로 사용하는 것이 더 적합하다고 판단

        250307_v4
        - 좌우 플립 증강 모드 추가(4번)
        
        250305_v3
        - 이미지는 있는데 json이 없는 경우(레이블링 bbox가 없으면 생성 안됨) 비어있는 txt파일을 자동 생성 기능 추가

        250305_v2
        - LabelMe에서 bounding box의 x1과 x2 순서가 서로 다를 경우를 대비해 min, max 함수로 보정한 버전
        - 위 업데이트로 YOLO 레이블에서 -값이 나오는 것을 방지한다.

        250305_v1
        - 첫 개발 버전
        '''
        print(release_note)