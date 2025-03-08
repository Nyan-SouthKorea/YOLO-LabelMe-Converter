import time

def name(file_name):
    '''확장자를 제거하고 반환'''
    len_file_format = len(file_name.split('.')[-1])
    only_name = file_name[:-(len_file_format+1)]
    return only_name

def class_list_request():
    print("class_list 예시: ['cable', 'carpet', 'etc']")
    input_txt = input('class_list를 입력하세요(예시를 정확히 지킬 것): ')
    try: tmp = input_txt.split('[')[-1].split(']')[0].split(', ')
    except: 
        print('class_list 입력을 잘 못 했습니다. 다시 시작하세요.')
        time.sleep(5)
        exit()

    class_list = []
    for class_name in tmp:
        class_list.append(class_name.replace("'", ''))
    return class_list

def is_img_file(img_name):
    '''본 파일명이 이미지인지 확인'''
    if img_name.split('.')[-1] in ['png', 'jpg', 'jpeg', 'gif']:
        return True
    else:
        return False

def is_label_file(label_name):
    '''본 파일명이 레이블인지 확인'''
    if label_name.split('.')[-1] in ['txt', 'json']:
        return True
    else:
        return False