from matplotlib import pyplot as plt
from collections import deque
from threading import Lock
import myo
import numpy as np


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
        with self.lock:
            self.emg_data_queue.append((event.timestamp, event.emg))


class Plot(object):

    def __init__(self, listener):
        self.n = listener.n
        self.listener = listener
        self.fig = plt.figure()
        self.axes = plt.axes()
        self.axes.set_ylim([-100, 100])
        # self.axes = [self.fig.add_subplot('81' + str(i)) for i in range(1, 2)]
        # [(ax for ax in self.axes]

        self.graphs = self.axes.plot(np.arange(self.n), np.zeros(self.n))[0]
        plt.ion()

    def update_plot(self):
        emg_data = self.listener.get_emg_data()
        emg_data = np.array([x[1] for x in emg_data]).T
        # emg_data  = np.absolute(emg_data)
        for data in emg_data:
            if len(data) < self.n:
                # Fill the left side with zeroes.
                data = np.concatenate([np.zeros(self.n - len(data)), data])
            self.graphs.set_ydata(data)
        plt.draw()

    def main(self):
        while True:
            self.update_plot()
            plt.pause(1.0 / 30)


def main():
    myo.init()
    hub = myo.Hub()
    listener = EmgCollector(512)
    with hub.run_in_background(listener.on_event):
        Plot(listener).main()


if __name__ == '__main__':
    main()
