import cv2
import queue
import time
import threading
q=queue.Queue()

input_st="rtsp://"
cap = cv2.VideoCapture(input_st)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("width:",width, "height:", height)

out = cv2.VideoWriter('./cap.avi', fourcc, 25.0, (width, height))
def Receive():
    print("start Reveive")
    cap = cv2.VideoCapture(input_st)
    ret, frame = cap.read()
    q.put(frame)
    while ret:
        ret, frame = cap.read()
        q.put(frame)
 
 
def Display():
     print("Start Displaying")
     while True:
         if q.empty() !=True:
            frame=q.get()
            out.write(frame)
            #cv2.imshow("frame1", frame)
         if cv2.waitKey(1) & 0xFF == ord('q'):
                break
 
if __name__=='__main__':
    p1=threading.Thread(target=Receive)
    p2 = threading.Thread(target=Display)
    p1.start()
    p2.start()

