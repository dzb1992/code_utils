from mongoengine import *
import datetime

# 连接mongodb fs数据库
connect("fs", host="127.0.0.1", port=27017)
#connect("fs", host="10.143.12.6", port=27018)


# 表模型
class Video(Document):
    # 存储在fs video集合
    meta = {
        "collection": "video",
    }
    id = SequenceField(required=True, primary_key=True)
    algorithm = StringField(max_length=50, required=True)  # 算法名称
    filename = StringField(max_length=150, required=True)  # 文件名称
    event_started = DateTimeField()  # 事件时间
    event_started_addr = StringField(required=True)  # 事件地址
    event_addr_type = StringField(required=True)  # 事件类型
    event_name = StringField(required=True)  # 事件名称
    camera_location = StringField(required=False)  # 摄像头
    slice_video = FileField(required=True)  # 切片视频


def save_object(filepath):
    """
    :param filepath: 在算法脚本中调用该方法进行数据库存储操作，目前通过传参filepath视频切片保存本地的路径
                            文件名称           事件发生时间      事件地址 事件名称  切片名称
                    格式为:客机航班保障节点分析_2022-04-21 10:30:33_330_浦东机坪_aeroplane out.mp4
                    后期方便传参需要接收：algorithm、filename、event_started、event_started_addr
                    event_addr_type、event_name、slice_video等参数进行数据库存储操作
    :return: 返回算法保存本地的filepath路径，方便后面进行删除本地视频操作
    """
    filed_list = filepath.split('.')[0].split('_')
    algorithm = filed_list[0]
    filename = filepath
    event_started = datetime.datetime.strptime(filed_list[1], '%Y%m%d%H%M%S')
    event_started_addr = filed_list[2]
    event_addr_type = filed_list[3]
    event_name = filed_list[4]
    camera_location = filed_list[5]
    slice_video = open(filepath, 'rb')

    # 实例化对象进行数据库存储操作
    video = Video(filename=filename,
                  algorithm=algorithm,
                  event_started=event_started,
                  event_started_addr=event_started_addr,
                  event_addr_type=event_addr_type,
                  event_name=event_name,
                  camera_location=camera_location)
    video.slice_video.put(slice_video, content_type='video/mp4', filename=filename)
    slice_video.close()
    video.save()
    return filepath


# 以下是在算法脚本中开启线程进行本地视频到数据库存储

"""
from table import save_object
from concurrent.futures import ThreadPoolExecutor, as_completed, wait

...... 算法操作

out_writers[action_name_index_1].release()
# 保存本地的视频路径格式为  客机航班保障节点分析_2022-04-21 10:30:33_330_浦东机坪_aeroplane out.mp4
filepath = filepaths[0]
task1 = pool.submit(save_object, filepath)
all_task.append(task1)


#  删除保存本地视频操作
for future in as_completed(all_task):
    data = future.result()
    print(data)
    os.remove(data)

pool.shutdown()


print("Video Detection Done!")
capture.release()
yolo.close_session()

"""
