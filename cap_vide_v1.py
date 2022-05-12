#data:2020.5.1
#author ding

import cv2
import queue
import datetime
import sys
import time
import threading
import csv
q=queue.Queue()



def get_camera (ip, radius = 300):
    """
    通过读取csv列表获取摄像机信息及圆半径的配置参数
    """
    filename = "model_data/camera_information.csv"
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        for row in reader:
            if ip == row[1].split("@")[1].split("/")[0]:
                camera_pos, camera_rtsp = row[0], row[1]
                camera_radius = int(row[2])
                camera_radius = int(row[2]) if camera_radius != 0 else radius

    return camera_pos, camera_rtsp, camera_radius


def Receive():
    print("start Reveive")
    cap = cv2.VideoCapture(camera_rtsp)
    ret, frame = cap.read()
    q.put(frame)
    count = 0
    while ret:
        ret, frame = cap.read()
        q.put(frame)
        count += 1
        if count == int(cap_num):
            cap.release()
            break

def Display():
     print("Start Displaying && capture .......")
     count = 0
     activate = True
     while activate:
         if q.empty() !=True:
            count += 1
            print("capture --> %s"%count)
            if count <int(cap_num):
               activate = True
               frame=q.get()
               out.write(frame)

            else:
               activate =False
               print("Video capture completed!")
               cap.release()
               out.release()
               cv2.destroyAllWindows()

         if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__=='__main__':
    global out
    global cap_num
    try:
        ip, cap_num= sys.argv[1:3]
    except Exception as err:
        print(sys.argv)
        print(err)
    camera_pos, camera_rtsp, camera_radius = get_camera("10.31.97.%s" % ip)
    print(camera_rtsp.split("@")[-1].split("/")[0])
    data = str(datetime.datetime.now()).split(" ")
    yy_mm_dd = data[0]
    hh_mm_ss = "_".join(str(data[1]).split(":"))
    save_path = yy_mm_dd + "_" + hh_mm_ss + "_" + camera_pos + ".mp4"

    cap = cv2.VideoCapture(camera_rtsp)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("width:", width, "height:", height)
    print("The program waits for 2 seconds, please confirm the message!")

    time.sleep(2)
    out = cv2.VideoWriter(save_path, fourcc, 25.0, (width, height))
    p1=threading.Thread(target=Receive)
    p2 = threading.Thread(target=Display)
    p1.start()
    p2.start()

