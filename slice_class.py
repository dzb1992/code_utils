# -*- coding: utf-8 -*-
"""
Time    : 2022/4/25 13:02
Author  : cong
"""

import threading
import datetime
import cv2


class MyThread(threading.Thread):
    def __init__(self, num, action_frame, frame, iter_frames, front_frames, action_name, out_writer, interval):
        threading.Thread.__init__(self)
        self.count = num
        self.action_frame = action_frame
        self.frame = frame
        self.iter_frames = iter_frames
        self.front_frames = front_frames
        self.action_name = action_name
        self.out_writer = out_writer
        self.interval = interval

    def run(self):
        for i in list(self.iter_frames.keys()):
            if self.action_frame - 20 * self.interval < i <= self.action_frame and i not in list(self.front_frames.keys()):
                self.front_frames[i] = self.iter_frames[i]
                self.out_writer.write(self.iter_frames[i])
        if self.action_frame < self.count <= self.action_frame + 20 * self.interval:
            self.out_writer.write(self.frame)
        if self.count == self.action_frame + 21 * self.interval:
            self.out_writer.release()