from collections import deque
from threading import Lock
import myo
import time
import psutil
import os

from constants.variables import data_array, number_of_samples, PROC_NAME, PROC_PATH, streamed_data

myo.init('X:\\Sapientia-EMTE\\DiplomaWork\\Service\\myo64.dll')


# This class from Myo-python SDK listens to EMG signals from armband
class Listener(myo.DeviceListener):

    def __init__(self, n):
        self.n = n
        self.lock = Lock()
        self.emg_data_queue = deque(maxlen=n)

    def on_connected(self, event):
        print("Myo Connected")
        event.device.stream_emg(True)

    def get_emg_data(self):
        with self.lock:
            print("Locked")  # Ignore this

    def on_emg(self, event):
        with self.lock:
            print(event.emg)
            self.emg_data_queue.append(event.emg)

            if len(list(self.emg_data_queue)) >= number_of_samples:
                data_array.append(list(self.emg_data_queue))
                self.emg_data_queue.clear()
                return False


class ForeverListener(myo.DeviceListener):
    def __init__(self, n):
        self.n = n
        self.lock = Lock()
        self.emg_data_queue = deque(maxlen=n)
        self._stop_requested = False

    def on_connected(self, event):
        print("Myo Connected")
        event.device.stream_emg(True)

    def get_emg_data(self):
        with self.lock:
            print("Locked")  # Ignore this

    def stop(self):
        with self.lock:
            self._stop_requested = True

    def on_emg(self, event):
        with self.lock:
            streamed_data.append(event.emg)


# To check if myo process is running
class MyoService:

    def __init__(self):
        self.hub = myo.Hub()

    # Check if Myo Connect.exe process is running
    def check_if_process_running(self):
        try:
            for proc in psutil.process_iter():
                if proc.name() == PROC_NAME:
                    return True

            return False
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print(PROC_NAME, " not running")

    # Restart myo connect.exe process if its not running
    def restart_process(self):
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == PROC_NAME:
                proc.kill()
                # Wait a second
                time.sleep(1)

        while not self.check_if_process_running():
            os.startfile(PROC_PATH)
            time.sleep(1)
            # while not self.check_if_process_running():
            #     pass

        print("MYO Process started")
        instructions = "MYO App started"
        return True
