import torch
import cv2
import numpy as np
# from skimage.filters import threshold_local
import imutils


model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/best.pt')

img = cv2.imread("D:\hoc_LT\python\PBL4_test\data_test\AQUA7_65169_checkout_2020-10-26-10-50uf0q3cMkeW.jpg")
# img = cv2.imread("D:\hoc_LT\python\PBL4_test\data_test\AQUA7_65169_checkout_2020-10-26-10-50uf0q3cMkeW.jpg")
#detect
detections = model(img)
# labels, cord = detections.xyxyn[0][: -1], detections.xyxyn[0][:,: -1]
# print(type(detections))
# detections.print()
# print(type(labels))
# print(cord)
results = detections.pandas().xyxy[0].to_dict(orient="records")
x = np.array(results)
for result in results:
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
        cv2.putText(img, name, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 1, (60, 255, 255), 1)
        table = img[y1:y2, x1:x2]

img_hsv = cv2.split(cv2.cvtColor(table, cv2.COLOR_BGR2HSV))[2]
blur = cv2.GaussianBlur(img,(5,5),0)
thresh = cv2.adaptiveThreshold(img_hsv,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)

# convert black pixel of digits to white pixel
cv2.imwrite("step2_2.png", thresh)
thresh = imutils.resize(thresh, width=400)
# thresh = cv2.medianBlur(thresh, 5)

# connected components analysis
# labels = measure.label(thresh, connectivity=2, background=0)

cv2.imshow("img", thresh)
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