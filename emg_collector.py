from matplotlib import pyplot as plt
from collections import deque
from threading import Lock, Thread

import myo
import numpy as np
import datetime
import os

class EmgCollector(myo.DeviceListener):
  """
  Collects EMG data in a queue with *n* maximum number of elements.
  """

  def __init__(self, n):
    self.n = n
    self.lock = Lock()
    self.emg_data_queue = deque(maxlen=n)

  def get_emg_data(self):
    with self.lock:
      return list(self.emg_data_queue)

  # myo.DeviceListener

  def on_connected(self, event):
    event.device.stream_emg(True)

  def on_emg(self, event):
    # with self.lock:
    self.emg_data_queue.append((event.timestamp, event.emg))



data = []
def main():
    myo.init(os.getcwd() + '\\services\\myo64.dll')
    hub = myo.Hub()
    listener = EmgCollector(512)
    print("Hello")
    with hub.run_in_background(listener.on_event):
        start_time = datetime.datetime.now()
        while len(data) < 50:
            pass
        end_time = datetime.datetime.now()
        print("Latency:", (end_time - start_time)*1000, "ms")
        data.clear()



if __name__ == '__main__':
  main()
