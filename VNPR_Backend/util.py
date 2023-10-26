import easyocr
import string
from thefuzz import process


char_to_int = { 'A':'4','B':'8','C':'6','D':'0','E':'3','F':'7','G':'6','H':'8','I':'1','J':'1','L':'1','M':'0','N':'0',
                 'O':'0','P':'8','Q':'0','S':'5','T':'7','U':'0','V':'4','W':'0','X':'4','Y':'4','Z':'2'
                 }

int_to_char = {'0':'O','1':'I','2':'Z','3':'B','4':'A','5':'S','6':'C','7':'T','8':'B','9':'B'}

state_code = ['AP','AR','AS','BR','CG','DL','GA','GJ','HR','HP','JK','JH','KA','KL','LD','MP','MH','MN','ML','MZ',
              'NL','OD','PY','PB','RJ','SK','TN','TS','TR','UP','UK','WB','AN','CH','DN','DD','LA','OT']
# state_code = ['UP','DL','HR','UK','MH','GJ']
# reader = easyocr.Reader(['en'], gpu=False)

def post_processing_text(text1):
    text1="".join(filter(str.isalnum,text1))
    text=[]
    for i in range(len(text1)):
        if text1[i].isalpha():
            text.append(text1[i].upper())
        else:
            text.append(text1[i])
    # if len(text)<9:
    #     return None
    try:
        if text[0].isnumeric():
            text[0] = int_to_char[text[0]]
    except:
        pass
    try:
        if text[1].isnumeric():
            text[1] = int_to_char[text[1]]
    except:
        pass
    try:
        if not text[2].isnumeric():
            text[2] = char_to_int[text[2]]
    except:
        pass
    try:
        if not text[3].isnumeric():
            text[3] = char_to_int[text[3]]
    except:
        pass
    try:
        if text[4].isnumeric():
            text[4] = int_to_char[text[4]]
    except:
        pass
    try:
        if text[5].isnumeric():
            text[5] = int_to_char[text[5]]
    except:
        pass
    try:
        if not text[-4].isnumeric():
            text[-4] = char_to_int[text[-4]]
    except:
        pass
    try:
        if not text[-3].isnumeric():
            text[-3] = char_to_int[text[-3]]
    except:
        pass
    try:
        if not text[-2].isnumeric():
            text[-2] = char_to_int[text[-2]]
    except:
        pass
    try:
        if not text[-1].isnumeric():
            text[-1] = char_to_int[text[-1]]
    except:
        pass
    try:
        p = process.extract(text[0]+text[1],state_code)[0][0]
        if p:
            text[0] = p[0]
            text[1] = p[1]
    except:
        pass
    res=""
    try:
        for i in text:
            res+=i
    except:
        pass
    return res
    
        

def read_license_plate(license_plate_crop,reader):
    detections = reader.readtext(license_plate_crop)
    res=''
    sc=0
    for detection in detections:
        bbox,text,score = detection
        res=res+text
        sc=max(sc,score)
        text = text.upper().replace(' ','')
    # return post_processing_text(res),res
    return res,sc
    # return None, None


def get_car(license_plate, vehicle_track_ids):
    x1, y1, x2, y2, score, class_id = license_plate

    foundIt = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]

        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return vehicle_track_ids[car_indx]

    return -1, -1, -1, -1, -1