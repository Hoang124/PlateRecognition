import os
from re import M
import cv2
from tensorflow import keras
import numpy as np
import imutils
from imutils import perspective
from plateDetection import plateDetection
import socket
import threading

# client_socket = None
# last_received_message = None

# def inititalize_socket():
#         print("socket on")
#         client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#         remote_ip =  "127.0.0.1"
#         remote_port = 10319
#         client_socket.connect((remote_ip,remote_port))

# print

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
remote_ip =  "127.0.0.1"
remote_port = 10319
client_socket.connect((remote_ip,remote_port))

def plateRe(input):
    img = cv2.imread(input)
    # img = cv2.GaussianBlur(img,(5, 5), 0)
    # img = cv2.medianBlur (img, 5)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray = cv2.equalizeHist(gray)
    # ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # thresh = cv2.bitwise_not(thresh)
    thresh = cv2.adaptiveThreshold(gray,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 12)
    # cv2.imshow('img', thresh)
    # cv2.waitKey(0)
    cv2.imwrite('plateGray.png', thresh)
    data_detect = []
    output = cv2.connectedComponentsWithStats(thresh, 4, cv2.CV_32S)
    (number_labels, labels, stats, centroids) = output
    for i in range(0, number_labels):
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        (cX, cY) = centroids[i]
        aspectRatio = w/h
        heightRatio = h/thresh.shape[0]
        solidity = area/float(w*h)
        if 0.2 < aspectRatio < 1.0 and heightRatio > 0.3 and solidity > 0.1:
            output = img.copy()
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
            # cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)
            componentMask = (labels == i).astype("uint8") * 255
            # show our output image and connected component mask
            # cv2.imshow('img', output)
            # cv2.imshow('img', componentMask)
            # split image
            kq = componentMask[y:y + h, x:x + w]
            kq = cv2.resize(kq, (30,60))
            kq = np.array(kq)
            kq = kq.reshape(60, 30, 1)
            data_detect.append(kq)
            # cv2.imshow('img1',kq)
            # cv2.waitKey(0)
    # Alpha = {0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M',
    #           23: 'N', 24: 'P', 25: 'Q', 26: 'R', 27: 'S', 28: 'T', 29: 'U', 30: 'V', 31: 'W', 32: 'X', 33: 'Y', 34: 'Z'}
    Alpha = {0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'K', 19: 'L', 20: 'M',
              21: 'N', 22: 'P', 23: 'R', 24: 'S', 25: 'T', 26: 'U', 27: 'V', 28: 'X', 29: 'Y', 30: 'Z'}

    model = keras.models.load_model('modelChuSo1.h5')

    plate_info = ""
    for i in data_detect:
        # dự đoán với tập dữ liệu test
        data_i = i.reshape(-1, 60, 30, 1)
        results = model.predict(data_i)
        #lấy phần tử có giá trị lớn nhất 
        result = int(results.argmax(axis=-1))
        plate_info += Alpha[result]
    return plate_info

def run():
    # url = r'C:\Users\ACER\Downloads\plate1.png'
    # inititalize_socket()
    url = 'picture.png'
    if not os.path.exists(url):
        print('1')
        send_message(' ')
    else:
        print('2')
        frame = cv2.imread(url)
        outfile = 'plate.png'
        plate = plateDetection(url, outfile)
        check = plate.frame_detection(frame)
        if not check: 
            send_message(' ')
        else:
            plateOut = ''
            plateOut = plateRe(outfile)
            if plateOut == '':
                print("sai qua roi ahihi")
            else: print(plateOut)
            if plateOut != '':
                send_message(plateOut)
            # if os.path.exists(url):
            #     os.remove(url)
            if os.path.exists(outfile):
                os.remove(outfile)

    # try:
    #     thread1=MyThread("Distance",1,3)
    #     thread2=MyThread("Camera",2,3)
    #     thread1.start()
    #     thread2.start()
        
    # except Exception as e:
    #     print(e)
    # url = 'D:\hoc_LT\python\PBL4_test2\data_test\AQUA7_68783_checkin_2020-11-1-13-40ww85ttaNPw.jpg'
    # url = r'C:\Users\ACER\Downloads\288814390_413002523889411_2539760408172404152_n.jpg'
    
    # test
    # for i in range(7, 17):
    #     url = 'C:\\Users\\ACER\\Downloads\\{}.jpg'.format(i)
    #     # url = 'opencv_frame.png'
    #     frame = cv2.imread(url)
    #     outfile = "plate_frame" + str(i) + ".jpg"
    #     # outfile = 'opencv_frame.png'
    #     plate = plateDetection(url, outfile)
    #     plate.frame_detection(frame)
    #     plateRe(outfile)
    # 
    # url = r'C:\Users\ACER\Downloads\plate1.png'
    # frame = cv2.imread(url)
    # outfile = 'opencv_frame.png'
    # plate = plateDetection(url, outfile)
    # check = plate.frame_detection(frame)
    # if check: 
    #     print("Dung")
    # else: print("sai")
    # plateRe(outfile)

    # bo vao def __init

    
def send_message(text):
    print("socket on")
    print("text",text,client_socket)
    data = "license:" + text
    message = data.encode("utf-8")
    client_socket.send(message)
    print("send",data)
    return "break"
