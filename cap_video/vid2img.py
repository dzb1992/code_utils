# -*- coding=utf-8 -*-
import cv2
import datetime
cap_list = []
def cap_pic():
    i = 0
    #动态测试
    cap = cv2.VideoCapture("result_4.mp4")
    frames_num=cap.get(7)
    print("total:%s "%frames_num)
    # cap = cv2.VideoCapture(0)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    videoWriter = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
    frames_num=cap.get(7)
    ret, frame = cap.read()

    i = 0

    activate = True
    while activate:
        i += 1
        ret, frame = cap.read()
        cv2.imshow("capture", frame)
        if i % 6 == 0:
            cv2.imwrite("qqq/%s.jpg" % i, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            videoWriter.write(frame)
        cv2.waitKey(fps)
        
        
        #if i < 10:
        #    activate = True
        #else:
        #    activate = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print("*"*50)
    print("开始测试：")
    cap_pic()
