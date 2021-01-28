from __future__ import print_function

from collections import deque
from threading import Lock
import matplotlib
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import regularizers
from keras.models import load_model
import myo
import time
import psutil
import os

# New Imports
import warnings

matplotlib.use("TkAgg")
myo.init('X:\\Sapientia-EMTE\\Szakmai Gyakorlat\\v2\\HIMO\\myo64.dll')
global data_array


# This class from Myo-python SDK listens to EMG signals from armband
class Listener(myo.DeviceListener):
    number_of_samples = 1000

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
            self.emg_data_queue.append(event.emg)

            if len(list(self.emg_data_queue)) >= self.n:
                data_array.append(list(self.emg_data_queue))
                self.emg_data_queue.clear()
                return False


# To check if myo process is running
class MyoService:
    proc_name = "Myo Connect.exe"
    path = 'C:\Program Files (x86)\Thalmic Labs\Myo Connect\Myo Connect.exe'

    def __init__(self):
        self.hub = myo.Hub()

    # Check if Myo Connect.exe process is running
    def check_if_process_running(self):
        try:
            for proc in psutil.process_iter():
                if proc.name() == 'Myo Connect.exe':
                    return True

            return False
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print(self.proc_name, " not running")

    # Restart myo connect.exe process if its not running
    def restart_process(self):
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == self.proc_name:
                proc.kill()
                # Wait a second
                time.sleep(1)

        while not self.check_if_process_running():
            os.startfile(self.path)
            time.sleep(1)
            while not self.check_if_process_running():
                pass

        print("MYO Process started")
        instructions = "MYO App started"
        return True


class ClassifyExercises:
    # region VARS
    number_of_samples = 1000
    _tiptoe_training_set = np.zeros((8, number_of_samples))
    _toe_crunches_training_set = np.zeros((8, number_of_samples))
    _rest_training_set = np.zeros((8, number_of_samples))

    Sensor1 = np.zeros((1, number_of_samples))
    Sensor2 = np.zeros((1, number_of_samples))
    Sensor3 = np.zeros((1, number_of_samples))
    Sensor4 = np.zeros((1, number_of_samples))
    Sensor5 = np.zeros((1, number_of_samples))
    Sensor6 = np.zeros((1, number_of_samples))
    Sensor7 = np.zeros((1, number_of_samples))
    Sensor8 = np.zeros((1, number_of_samples))

    validation_set = np.zeros((8, number_of_samples))
    training_set = np.zeros((8, number_of_samples))

    div = 50  # every 50 batch ( 1000/50 -> 20 data )
    averages = int(number_of_samples / div)

    tiptoe_averages = np.zeros((int(averages), 8))
    toe_crunches_averages = np.zeros((int(averages), 8))
    rest_averages = np.zeros((int(averages), 8))

    # Define number of exercises
    number_of_gestures = 3
    # data_array = []

    tiptoe_label = 0
    toe_crunches_label = 1
    rest_label = 2

    # Define current subject
    subject = ""
    prepare_array = []  # for storing mean values

    result_path = 'X:\\Sapientia-EMTE\\Szakmai Gyakorlat\\v2\\HIMO\\data\\results\\'
    proc_name = "Myo Connect.exe"

    listener = Listener(number_of_samples)
    myoService = MyoService()

    # endregion
    def __init__(self, subject):
        self.subject = subject
        print("init")

    def PrepareTrainingData(self):

        # This function kills Myo Connect.exe and restarts it to make sure it is running
        # Because sometimes the application does not run even when Myo Connect process is running
        # So i think its a good idea to just kill if its not running and restart it

        while not self.myoService.restart_process():
            pass

        # Wait for 3 seconds until Myo Connect.exe starts
        time.sleep(3)

        # Initialize the SDK of Myo Armband
        myo.init('X:\\Sapientia-EMTE\\Szakmai Gyakorlat\\v2\\HIMO\\myo64.dll')

        # region TIPTOE_DATA
        instructions = "Stand on your toes!"
        print(instructions)

        time.sleep(0.5)
        while True:
            try:
                # listener = Listener(self.number_of_samples)
                # input("Stand on your toes!")
                self.myoService.hub.run(self.listener.on_event, 20000)
                self._tiptoe_training_set = np.array((data_array[0]))
                data_array.clear()
                break
            except:
                while not self.myoService.restart_process():
                    pass
                # Wait for 3 seconds until Myo Connect.exe starts
                time.sleep(3)

        # Here we send the received number of samples making them a list of 1000 rows 8 columns
        # just how we need to feed to tensorflow
        # endregion

        # region TOE_CRUNCH_DATA
        instructions = "Tip toe data ready!"
        print(instructions)

        time.sleep(1)
        instructions = "Crunch your toes!"

        print(instructions)
        time.sleep(1)
        while True:
            try:
                # hub = myo.Hub()
                # listener = Listener(self.number_of_samples)
                # input("Crunch your toes!")
                self.myoService.hub.run(self.listener.on_event, 20000)
                self._toe_crunches_training_set = np.array((data_array[0]))
                data_array.clear()
                break
            except:
                while not self.myoService.restart_process():
                    pass
                # Wait for 3 seconds until Myo Connect.exe starts
                time.sleep(3)

        instructions = "Toe crunch data ready!"
        print(instructions)

        time.sleep(1)

        # endregion

        # region REST_DATA
        time.sleep(1)
        instructions = "Rest your foot!"

        print(instructions)
        time.sleep(1)
        while True:
            try:
                hub = myo.Hub()
                hub.run(self.listener.on_event, 20000)
                self._rest_training_set = np.array((data_array[0]))
                data_array.clear()
                break
            except:
                while not self.myoService.restart_process():
                    pass
                # Wait for 3 seconds until Myo Connect.exe starts
                time.sleep(3)

        instructions = "Rest data ready!"
        print(instructions)

        time.sleep(1)

        # endregion

        # region POSTPROCESS_DATA
        self.calculateMeanData()
        # endregion

    # This method is responsible for training EMG data
    def TrainEMG(self):
        labels = []
        print("Preprocess EMG data")

        # This division is to make the iterator for making labels run 20 times in inner loop and 3 times in outer loop
        # running total 60 times for 3 foot gestures
        samples = self.prepare_array.shape[0] / self.number_of_gestures
        print("Samples", samples)

        # Now we append all data in training label
        # We iterate to make 3 finger movement labels.
        for i in range(0, self.number_of_gestures):
            for j in range(0, int(samples)):
                labels.append(i)
        labels = np.asarray(labels)
        # print(labels, len(labels), type(labels))
        # print(conc_array.shape[0])

        permutation_function = np.random.permutation(self.prepare_array.shape[0])
        total_samples = self.prepare_array.shape[0]
        all_shuffled_data, all_shuffled_labels = np.zeros((total_samples, 8)), np.zeros((total_samples, 8))

        all_shuffled_data, all_shuffled_labels = self.prepare_array[permutation_function], labels[permutation_function]
        # print(all_shuffled_data.shape)
        # print(all_shuffled_labels.shape)

        number_of_training_samples = np.int(np.floor(0.8 * total_samples))
        train_data = np.zeros((number_of_training_samples, 8))
        train_labels = np.zeros((number_of_training_samples, 8))
        # print("TS ", number_of_training_samples, " S ", number_of_samples)
        number_of_validation_samples = np.int(total_samples - number_of_training_samples)
        train_data = all_shuffled_data[0:number_of_training_samples, :]
        train_labels = all_shuffled_labels[0:number_of_training_samples, ]
        print("Length of train data is ", train_data.shape)

        validation_data = all_shuffled_data[number_of_training_samples:total_samples, :]
        validation_labels = all_shuffled_labels[number_of_training_samples:total_samples, ]
        # print("Length of validation data is ", validation_data.shape, " validation labels is ",
        # validation_labels.shape)
        # print(train_data, train_labels)

        print("Building model...")
        instructions = "Building model..."
        model = keras.Sequential([
            # Input dimensions means input columns. Here we have 8 columns, one for each sensor
            keras.layers.Dense(8, activation=tf.nn.relu, input_dim=8, kernel_regularizer=regularizers.l2(0.1)),
            keras.layers.BatchNormalization(),
            keras.layers.Dense(self.number_of_gestures, activation=tf.nn.softmax)])

        adam_optimizer = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0,
                                               amsgrad=False)
        model.compile(optimizer=adam_optimizer,
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        print("Fitting training data to the model...")
        instructions = "Fitting training data to the model..."
        history = model.fit(train_data, train_labels, epochs=300, validation_data=(validation_data, validation_labels),
                            batch_size=16, verbose=0)

        print("Saving model for later...")
        save_path = self.result_path + self.subject + '_realistic_model.h5'
        model.save(save_path)

        print(model.input_shape)
        print(model.output_shape)

        instructions = "Training model successful!"
        print(instructions)

    def calculateMeanData(self):
        # Absolutes of foot gesture data
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            self._tiptoe_training_set = np.absolute(self._tiptoe_training_set)
            self._toe_crunches_training_set = np.absolute(self._toe_crunches_training_set)
            self._rest_training_set = np.absolute(self._rest_training_set)

            # Here we are calculating the mean values of all foot exercise data storing them as n/50 samples
            # because 50 batches of n samples is equal to n/50 averages
            for i in range(1, self.averages + 1):
                self.tiptoe_averages[i - 1, :] = np.mean(self._tiptoe_training_set[(i - 1) * self.div:i * self.div, :],
                                                         axis=0)
                self.toe_crunches_averages[i - 1, :] = np.mean(
                    self._toe_crunches_training_set[(i - 1) * self.div:i * self.div, :], axis=0)
                self.rest_averages[i - 1, :] = np.mean(self._rest_training_set[(i - 1) * self.div:i * self.div, :],
                                                       axis=0)

            # Here we stack all the data row wise
            # conc_array = np.concatenate([tiptoe_averages, heel_averages, toe_crunches_averages], axis=0)
            conc_array = np.concatenate([self.tiptoe_averages, self.toe_crunches_averages, self.rest_averages], axis=0)
            print(conc_array.shape)
        try:
            np.savetxt(self.result_path + self.subject + '.txt', conc_array, fmt='%i')
            instructions = "Saving training data successful!"
            print(instructions)
            self.prepare_array = conc_array

        except:
            instructions = "Saving training data failed!"
            print(instructions)
            pass

    def PredictGestures(self):
        # Initializing array for verification_averages
        validation_averages = np.zeros((int(self.averages), 8))
        model = load_model(self.result_path + self.subject + '_realistic_model.h5')

        # while not session_finished:
        try:
            print("Show a foot gesture and press ENTER to get its classification!")
            self.myoService.hub.run(self.listener.on_event, 1000)
            # Here we send the received number of samples making them a list of 1000 rows 8 columns
            validation_set = np.array((data_array[0]))
            data_array.clear()

        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            pass

        self.validation_set = np.absolute(self.validation_set)

        # We add one because iterator below starts from 1
        batches = int(self.number_of_samples / self.div) + 1
        for i in range(1, batches):
            validation_averages[i - 1, :] = np.mean(self.validation_set[(i - 1) * self.div:i * self.div, :], axis=0)

        validation_data = validation_averages
        print("Verification matrix shape is ", validation_data.shape)

        predictions = model.predict(validation_data, batch_size=16)
        predicted_value = np.argmax(predictions[0])
        if predicted_value == 0:
            print("Tiptoe stand")
        elif predicted_value == 1:
            print("Toe Crunches ")
        else:
            print("Rest gesture")


if __name__ == '__main__':
    dummy = ClassifyExercises("Ervin")
    dummy.PrepareTrainingData()
    dummy.TrainEMG()
    dummy.PredictGestures()
