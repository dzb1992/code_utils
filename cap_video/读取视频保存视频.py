import numpy as np
import cv2

#大华
#user, pwd, ip, channel = "admin", "admin123", "192.168.102.65", 1
#input_st= "rtsp://%s:%s@%s/cam/realmonitor?channel=%d&subtype=0" % (user, pwd, ip, channel)
#海康
#input_st=""
input_st=""
cap = cv2.VideoCapture(input_st)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("width:",width, "height:", height)

#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (width, height))

while (cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:
    cv2.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  else:
    break
    
cap.release()
out.release()
cv2.destroyAllWindows()

