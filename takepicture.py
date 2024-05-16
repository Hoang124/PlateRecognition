import threading
import time
import cv2
import requests
import plateRecognization
distance=1000
plate=""
def takedistance():
    x = requests.get('http://192.168.220.31:5000/takedistance')
    return x.json()
class MyThread(threading.Thread):
    def __init__(self,name,counter,delay):
        threading.Thread.__init__(self)
        self.name=name
        self.counter=counter
        self.delay=delay
    def run(self):
        timeThread = 1
        while True: 
            if self.counter==1:
                global distance
                distance=takedistance()
                # if distance <= 20:
                #     timeThread = 0
                # else: timeThread = 1
                print(distance)
                time.sleep(self.delay)
            if self.counter==2:
                cam = cv2.VideoCapture('http://192.168.220.31:5000/video_feed')
                cv2.namedWindow("test")
                while True:
                    ret, frame = cam.read()
                    if not ret:
                        print("failed to grab frame")
                        break
                    cv2.imshow("test", frame)
                    k = cv2.waitKey(1)
                    if k%256 == 27:
                        print("Escape hit, closing...")
                        break
                    elif distance<=20 and timeThread == 1:
                        print("takepicture")
                        timeThread = 0
                        img_name = "picture.png"
                        cv2.imwrite(img_name, frame)
                        print("{} written!".format(img_name))
                        time.sleep(self.delay)
                        global plate
                        plate = plateRecognization.run()
                        if plate != '':
                            print(plate)
                        else: print("rong")
                        timeThread = 1
                cam.release()
                cv2.destroyAllWindows()
        # if self.counter==3:
        #     app = App()
        #     app.geometry("1000x600")
        #     app.title("Nhận diện biển số")
        #     app.mainloop()

def run():
    try:
        thread1=MyThread("Distance",1,5)
        thread2=MyThread("Camera",2,5)
        # thread3=MyThread("Gui", 3, 0)
        thread1.start()
        thread2.start()
        # thread3.start()
        
    except Exception as e:
        print(e)

run()

    



