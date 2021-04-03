from matplotlib import pyplot as plt
from collections import deque
from threading import Lock, Thread

import myo
import numpy as np
import datetime
import os
from constants.variables import streamed_data
import threading
import sys
import time

data = []
class EmgCollector(myo.DeviceListener):
  """
  Collects EMG data in a queue with *n* maximum number of elements.
  """

  def __init__(self, n):
    self.n = n
    self.lock = Lock()
    self.emg_data_queue = deque(maxlen=n)

  def on_connected(self, event):
    event.device.stream_emg(True)

  def on_emg(self, event):
    data.append(event.emg)



def main():
    print(sys.version_info)
    myo.init(os.getcwd() + '\\services\\myo64.dll')
    hub = myo.Hub()
    listener = EmgCollector(512)
    print("Hello")

    thread = threading.Thread(target=lambda:hub.run_forever(listener.on_event, 300))
    thread.start()
    average = 0.0
    counter = 0
    while counter < 50:
        start_time = datetime.datetime.now()

        while len(data) < 50:
            pass

        end_time = datetime.datetime.now()
        print("Latency:", (end_time - start_time).total_seconds()*1000, "ms")

        data.clear()
        counter+=1
        average += (end_time - start_time).total_seconds()*1000

    print("Average:", average/counter, "ms")
    hub.stop()
    thread.join()

if __name__ == '__main__':
  main()
