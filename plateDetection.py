from matplotlib.pyplot import table
import torch
import cv2
import numpy as np
import imutils
from imutils import perspective


class plateDetection:
    # client_socket = None
    # last_received_message = None
    def __init__(self, url, outfile):
        self._URL = url
        self.model = self.loadmodel()
        self.classes = self.model.names
        self.outfile = outfile
        self.device = 'cpu'
        # self.inititalize_socket()

    def setUrl(self, url):
        self._URL = url

    def get_video_from_url(self):
        play = play

    def loadmodel(self):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/best.pt')
        return model

    def frame_detection(self, frame):
        self.model.to(self.device)
        detections = self.model(frame)
        if detections:
            results = detections.pandas().xyxy[0].to_dict(orient="records")
            if not results:
                return False
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
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                # cv2.putText(img, name, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 1, (60, 255, 255), 1)
                pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype=np.float32)
                table = perspective.four_point_transform(frame, pts)
                cv2.imwrite(self.outfile, table)
            return True
        else: return False

    # def inititalize_socket(self):
    #     self.client_socket = socket.Socket(socket.AF_INET,socket.SOCK_STREAM)
    #     remote_ip =  "127.0.0.1"
    #     remote_port = 10319
    #     self.client_socket.connect((remote_ip,remote_port))
    
    # def send_message(self,text):
    #     data = "license" + text
    #     message = data.encode("utf-8")
    #     self.client_socket.send(message)
    #     print("send",data)
    #     return "break"