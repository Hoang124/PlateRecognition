from matplotlib.pyplot import table
import torch
import cv2
import numpy as np
import imutils
from imutils import perspective

model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/best.pt')

# img = cv2.imread("D:\hoc_LT\python\PBL4_test\data_test\AQUA7_65169_checkout_2020-10-26-10-50uf0q3cMkeW.jpg")
img = cv2.imread("D:\hoc_LT\python\PBL4_test2\data_test\AQUA7_66626_checkin_2020-11-1-11-19ipxCJRTEcI.jpg")
#detect
detections = model(img)
# labels, cord = detections.xyxyn[0][: -1], detections.xyxyn[0][:,: -1]
# print(type(detections))
# detections.print()
# print(type(labels))
# print(cord)
results = detections.pandas().xyxy[0].to_dict(orient="records")
print(results)
result = results[0]
confidence = result["confidence"]
name = result["name"]
clas = result["class"]
if clas == 15:
    x1 = int(result["xmin"])
    y1 = int(result["ymin"])
    x2 = int(result["xmax"])
    y2 = int(result["ymax"])
    print(x1, y1, x2, y2)

    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    # cv2.putText(img, name, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 1, (60, 255, 255), 1)
    pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype=np.float32)
    table = perspective.four_point_transform(img, pts)

img_hsv = cv2.split(cv2.cvtColor(table, cv2.COLOR_BGR2HSV))[2]
blur = cv2.GaussianBlur(img,(5,5),0)
thresh = cv2.adaptiveThreshold(img_hsv,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)

# convert black pixel of digits to white pixel
cv2.imwrite("step2_5.png", table)
thresh = imutils.resize(thresh, width=400)
# thresh = cv2.medianBlur(thresh, 5)

# connected components analysis
# labels = measure.label(thresh, connectivity=2, background=0)
output = cv2.connectedComponentsWithStats(thresh, 4, cv2.CV_32S)
number_labels = output[0]
labels = output[1]
stats = output[2]
centroids = output[3]


# Segment kí tự
kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
thre_mor = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel3)
cont, _  = cv2.findContours(thre_mor, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


plate_info = ""
cont_sort = sort_contours(cont)
print(type(cont_sort))

for c in sort_contours(cont):
    (x, y, w, h) = cv2.boundingRect(c)
    ratio = h/w
    if 1.5<=ratio<=3.5: # Chon cac contour dam bao ve ratio w/h
        if h/table.shape[0]>=0.6: # Chon cac contour cao tu 60% bien so tro len

            # Ve khung chu nhat quanh so
            cv2.rectangle(table, (x, y), (x + w, y + h), (0, 255, 0), 2)

table = imutils.resize(table, width=400)
cv2.imshow("img", table)
cv2.waitKey(0)
# class plateDetection:
#     def __init__(self, url, outfile):
#         self._URL = url
#         self.model = self.loadmodel()
#         self.classes = self.model.names
#         self.outfile = outfile
#         self.device = 'cpu'

#     def get_video_from_url(self):
#         play = pafy    
#     def loadmodel(self):
#         model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/best.pt')
#         return model
#     def frame_detection(self, frame):
#         self.model.to(self.device)
#         frame = [frame]
#         detections = self.model(frame)

#         results = detections.pandas().xyxy[0].to_dict(orient="records")