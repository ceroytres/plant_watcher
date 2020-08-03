import time
import datetime
from threading import Thread
from collections import deque
import serial

import pandas as pd
import plotly.experess as px


class SerialLinePlot(object):

    def __init__(self, port: int, baudrate: int, window_size: int):

        self.port = port
        self.baudrate = baudrate
        self.window_size = window_size
        self.serial = serial.Serial(port, baudrate)
        self.data_queue = deque([(datetime.datetime.now(), 0)] * self.window_size)
        self.active = True
        self.received = False
        self.thread = None

    def create_thread(self):
        
        if self.thread is None:
            self.thread = Thread(target=self.backgroundThread)
            self.thread.start()
            # Block till we start receiving values
            while self.received != True:
                time.sleep(0.1)

    def plot(self, **kwargs):
        fig = px.line(self.data, **kwargs)
        return fig


    def backgroundThread(self):    # retrieve data
        time.sleep(1.0)  # give some buffer time for retrieving data
        self.serial.reset_input_buffer()
        while (self.active):
            self.serial.readinto(raw_data)
            self.rawData = (datetime.datetime.now(), raw_data)
            self.received = True

    def close():

        self.thread.join()
        self.serial.close()
