from takepicture import MyThread

if __name__ == '__main__':
    try:
        thread1=MyThread("Distance",1,7)
        thread2=MyThread("Camera",2,7)
        #thread3=MyThread("GUI",3,0)
        thread1.start()
        thread2.start()
        #thread3.start()
    except Exception as e:
        print(e)
