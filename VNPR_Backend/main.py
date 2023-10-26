# Importing the libraries
import cv2
from ultralytics import YOLO
import util
import numpy as np
import db
import imutils
import datetime
from matplotlib import pyplot as plt
# from sort import *
# Loading models

model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('./model/best.pt')

# load video
vehicles = [2,3,5,7]

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	# return the ordered coordinates
	return rect


def four_points_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped


def getContours(img, orig):
    biggest = np.array([])
    maxArea = 0

    # _, contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            cv2.drawContours(orig, cnt, -1, (255, 0, 0), 3)
            min_rect = cv2.minAreaRect(cnt)
            approx = cv2.boxPoints(min_rect).astype(int)
            approx = approx[:,np.newaxis,:]
            # peri = cv2.arcLength(cnt, True)
            # approx = cv2.approxPolyDP(cnt,0.02*peri, True)
            if area > maxArea and len(approx) == 4:
            # if area > maxArea:
                biggest = approx
                maxArea = area
                break
    return biggest, orig


def align_license_plate(src_img,is_Visualize=False):
    kernel = np.ones((3,3))
    imgGray = cv2.cvtColor(src_img, cv2.COLOR_RGB2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,150,200)
    imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
    imgThres = cv2.erode(imgDial,kernel,iterations=2)
    imgContour = src_img.copy()
    
    
    
    biggest, contour_img = getContours(imgThres, imgContour)
    # print(biggest)
    if len(biggest) ==0:
        return None
    biggest = np.squeeze(biggest)
    # print(biggest)

    # Visualize if biggest is correct or not
    # imgWarped = src_img.copy()
    # cv2.drawContours(imgWarped, [biggest], 0, (255, 0, 0), 4)

    imgWarped = four_points_transform(src_img, biggest)
    if is_Visualize:
        titles = ['original', 'Blur', 'Canny', 'Dialte', 'Threshold', 'Contours', "Warped" ]
        images = [src_img,  imgBlur, imgCanny, imgDial, imgThres, contour_img, imgWarped]
        
        for i in range(7):
            plt.subplot(3, 3, i+1), plt.imshow(images[i], 'gray')
            plt.title(titles[i])
        
        plt.show()
    return imgWarped

def detect_license_plate(path, collection,reader):
    img = False
    try:
        frame = cv2.imread(path)
        print(frame.shape)
        img=True
    except:
        img = False
    if not img:
        cap = cv2.VideoCapture(path)
        result = {}
        # read frames
        frame_number = -1
        ret = True
        x=0
        y=0
        while ret:
            ret =False
            frame_number+=1
            ret,frame= cap.read()
            if frame_number==0:
                (x,y,_) = frame.shape
                y=int(0.5*y)
            if ret and frame_number%5==0:
                try:
                    results = model.track(frame, persist=True)
                    cars = results[0].boxes.data.tolist()
                    track_ids = results[0].boxes.id.int().cpu().tolist()
                    print(track_ids)
                    for i in range (len(cars)):
                        xcar1, ycar1, xcar2, ycar2, track_id, score,object_id = cars[i]
                        if object_id in vehicles:
                            car = frame[int(ycar1):int(ycar2), int(xcar1):int(xcar2),:]
                            license_plates = license_plate_detector(car)[0].boxes.data.tolist()
                            if len(license_plates)!=0:
                                x1,y1,x2,y2,score,class_id = license_plates[0]
                                x1r = int(xcar1 + x1)
                                y1r = int(ycar1 + y1)
                                x2r = int(x1r + (x2 - x1))
                                y2r = int(y1r + (y2 - y1))
                                if y1r<y or track_ids[i] in result:
                                    continue
                                license_plate_crop_ = car[int(y1):int(y2), int(x1):int(x2),:]
                                thresh_img = align_license_plate(src_img=license_plate_crop_)
                                if thresh_img is None:
                                    continue
                                # thresh_img = imutils.rotate(license_plate_crop_, -30)
                                # license_plate_crop = align_license_plate(src_img=license_plate_crop_)
                                # thresh_img =test.preprocess_license_plate(license_plate_crop,is_visualize_steps=True)
                                license_plate_text , _ = util.read_license_plate(thresh_img,reader)
                                if license_plate_text and license_plate_text!="" and len(license_plate_text)>4:
                                    print("Predictions\n\n")
                                    print(track_ids[i],license_plate_text)
                                    license_plate_text = str(license_plate_text)
                                    if track_ids[i] not in result:
                                        temp = datetime.datetime.now().strftime("%H:%M:%S %B %d, %Y")
                                        result[track_ids[i]] = [license_plate_text,temp]
                                        db.insertIntoDatabase(license_plate_text,temp)
                except Exception as e:
                    print(e)
                    
        # print("Results\n\n\n\n\n")   
        # print(result)
        # Log into db
        # for i in result:
        #     # print(result[i])
        #     db.insertIntoDatabase(result[i][0],result[i][1])
        return [result[i] for i in result]
    if img:
        frame = cv2.imread(path)
        result = {}
        x,y,_ = frame.shape
        y=int(0.55*y)
        license_plates = license_plate_detector(frame)[0].boxes.data.tolist()
        for i in range (len(license_plates)):
                x1,y1,x2,y2,score,class_id = license_plates[i]
                license_plate_crop_ = frame[int(y1):int(y2), int(x1):int(x2),:]
                thresh_img = license_plate_crop_
                try:
                    thresh_img = align_license_plate(src_img=license_plate_crop_)
                    if thresh_img is None:
                        continue
                except:
                    pass
                license_plate_text , _ = util.read_license_plate(thresh_img,reader)
                temp = datetime.datetime.now().strftime("%H:%M:%S %B %d, %Y")
                result[i] = [license_plate_text,temp]
        # Log into db
        for i in result:
            db.insertIntoDatabase(result[i][0],result[i][1])
        var = True
        return [result[i] for i in result]

