from __future__ import print_function

import datetime
from collections import deque
from enum import Enum
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
import matplotlib.pyplot as plt

import tensorflow_addons as tfa

# New Imports
import warnings
import datetime as dt
import pickle

from typeguard import typechecked

matplotlib.use("TkAgg")
myo.init(os.getcwd() + '\\myo64.dll')

global data_array
data_array = []

number_of_samples = 100  # change this
Sensor1 = np.zeros((1, number_of_samples))
Sensor2 = np.zeros((1, number_of_samples))
Sensor3 = np.zeros((1, number_of_samples))
Sensor4 = np.zeros((1, number_of_samples))
Sensor5 = np.zeros((1, number_of_samples))
Sensor6 = np.zeros((1, number_of_samples))
Sensor7 = np.zeros((1, number_of_samples))
Sensor8 = np.zeros((1, number_of_samples))


class Exercise(Enum):
    TIP_TOE = 1
    TOE_CRUNCH = 2
    TOES_UP = 3
    REST = 3


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
            self.emg_data_queue.append(event.emg)

            if len(list(self.emg_data_queue)) >= number_of_samples:
                data_array.append(list(self.emg_data_queue))
                self.emg_data_queue.clear()
                return False


# To check if myo process is running
class MyoService:
    proc_name = "Myo Connect.exe"
    path = 'C:\\Program Files (x86)\\Thalmic Labs\\Myo Connect\\Myo Connect.exe'

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
            # while not self.check_if_process_running():
            #     pass

        print("MYO Process started")
        instructions = "MYO App started"
        return True


class ClassifyExercises:
    # region VARS

    # Define current subject
    subject = ""
    prepare_array = np.array([])  # for storing mean values

    result_path = os.getcwd() + '\\data\\results\\'
    proc_name = "Myo Connect.exe"

    # endregion
    @typechecked
    def __init__(self,
                 subject: str = 'Subject_Name',
                 nr_of_samples: int = 1000,
                 nr_of_gestures: int = 3,
                 exercise_labels=None,
                 batch_size: int = 50,
                 training_batch_size: int = 32,
                 ):

        if exercise_labels is None:
            all_labels = ["Tip Toe", "Toe Crunches", "Left Lean", "Right Lean", "Rest"]

        self.training_batch_size = training_batch_size
        self.number_of_gestures = nr_of_gestures

        # tiptoe_label = 0
        # toe_crunches_label = 1
        # left_lean_label = 2
        # right_lean_label = 3
        # rest_label = 4
        self.exercise_labels = exercise_labels

        self.div = batch_size  # every 50 batch ( 1000/50 -> 20 data )
        self.averages = int(nr_of_samples / batch_size)

        self.all_training_set = {}
        self.all_averages = []

        for i in range(0, nr_of_gestures):
            self.all_training_set[i] = np.zeros((8, number_of_samples))
            self.all_averages.append(np.zeros((int(self.averages), 8)))

        self.training_data_path = 'training_data\\'
        self.trained_model_path = 'trained_model\\'
        self.subject = subject
        self.number_of_samples = nr_of_samples

        # self._tiptoe_training_set = np.zeros((8, number_of_samples))
        # self._toe_crunches_training_set = np.zeros((8, number_of_samples))
        # self._rest_training_set = np.zeros((8, number_of_samples))

        self.validation_set = np.zeros((8, number_of_samples))
        self.training_set = np.zeros((8, number_of_samples))

        # self.tiptoe_averages = np.zeros((int(self.averages), 8))
        # self.toe_crunches_averages = np.zeros((int(self.averages), 8))
        # self.rest_averages = np.zeros((int(self.averages), 8))

        self.listener = Listener(number_of_samples)
        self.myoService = MyoService()
        print("init")

    def PrepareTrainingData(self):
        # global data_array
        # This function kills Myo Connect.exe and restarts it to make sure it is running
        # Because sometimes the application does not run even when Myo Connect process is running
        # So i think its a good idea to just kill if its not running and restart it

        while not self.myoService.restart_process():
            pass

        # Wait for 3 seconds until Myo Connect.exe starts
        time.sleep(3)

        # Initialize the SDK of Myo Armband
        myo.init(os.getcwd() + '\\myo64.dll')

        for x in range(0, self.number_of_gestures):
            time.sleep(1)
            instructions = self.exercise_labels[x]
            print("Recording - ", instructions)
            time.sleep(1)
            while True:
                try:
                    hub = myo.Hub()
                    listener = Listener(self.number_of_samples)
                    hub.run(listener.on_event, 20000)
                    self.all_training_set[x] = np.array((data_array[0]))
                    data_array.clear()
                    break
                except Exception as e:
                    print(e)
                    while not self.myoService.restart_process():
                        pass
                    # Wait for 3 seconds until Myo Connect.exe starts
                    time.sleep(3)

            instructions = self.exercise_labels[x]
            print(instructions, "data ready")

            time.sleep(1)
        # region POSTPROCESS_DATA
        self.calculateMeanData()
        # endregion

    # This method is responsible for training EMG data
    def TrainEMG(self):
        labels = []
        print("Preprocess EMG data")

        # This division is to make the iterator for making labels run 20 times in inner loop and 3 times in outer loop
        # running total 60 times for 3 foot gestures
        if self.prepare_array.size == 0:
            print("Loading data from disk!")
            self.prepare_array = np.loadtxt(self.result_path + self.training_data_path + self.subject + '.txt')

        samples = self.prepare_array.shape[0] / self.number_of_gestures

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
        tqdm_callback = tfa.callbacks.TQDMProgressBar(
            show_epoch_progress=False,
            leave_overall_progress=False,
            leave_epoch_progress=False
        )
        history = model.fit(train_data, train_labels, epochs=300, validation_data=(validation_data, validation_labels),
                            batch_size=self.training_batch_size, verbose=0, callbacks=[tqdm_callback])

        print("Saving model for later...")
        save_path = self.result_path + self.trained_model_path + self.subject + '_realistic_model.h5'
        model.save(save_path)

        filepath = self.result_path + self.trained_model_path + self.subject + '-dump.dmp'
        # os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as file_pi:
            pickle.dump(history.history, file_pi)

        # print(model.input_shape)
        # print(model.output_shape)

        instructions = "Training model successful!"
        print(instructions)

    def calculateMeanData(self):
        # Absolutes of foot gesture data
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            for x in range(0, self.number_of_gestures):
                self.all_training_set[x] = np.absolute(self.all_training_set[x])
            # self._tiptoe_training_set = np.absolute(self._tiptoe_training_set)
            # self._toe_crunches_training_set = np.absolute(self._toe_crunches_training_set)
            # self._rest_training_set = np.absolute(self._rest_training_set)

            # Here we are calculating the mean values of all foot exercise data storing them as n/50 samples
            # because 50 batches of n samples is equal to n/50 averages
            for i in range(1, self.averages + 1):
                for x in range(0, self.number_of_gestures):
                    self.all_averages[x][i - 1, :] = np.mean(
                        self.all_training_set[x][(i - 1) * self.div:i * self.div, :], axis=0)

                # self.tiptoe_averages[i - 1, :] = np.mean(self._tiptoe_training_set[(i - 1) * self.div:i * self.div, :],
                #                                          axis=0)
                # self.toe_crunches_averages[i - 1, :] = np.mean(self._toe_crunches_training_set[(i - 1) * self.div:i * self.div, :], axis=0)
                # self.rest_averages[i - 1, :] = np.mean(self._rest_training_set[(i - 1) * self.div:i * self.div, :],
                #                                        axis=0)

            # Here we stack all the data row wise
            conc_array = np.concatenate(self.all_averages, axis=0)
        try:
            np.savetxt(self.result_path + self.training_data_path + self.subject + '.txt', conc_array, fmt='%i')
            instructions = "Saving training data successful!"
            print(instructions)
            self.prepare_array = conc_array

        except Exception as e:
            print(e)
            instructions = "Saving training data failed!"
            print(instructions)

    # This function plots results for validation and training data for a certain subject
    def DisplayResults(self):
        try:
            filepath = self.result_path + self.trained_model_path + self.subject + '-dump.dmp'
            print(filepath)
            history = pickle.load(open(filepath, "rb"))
            print("Model load successful")
        except:
            print("No such model exists! Please try again.")
            return

        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        # Here we display the training and test loss for model
        ax1.plot(history['accuracy'])
        ax1.plot(history['val_accuracy'])
        ax1.set_title('model accuracy')
        ax1.set_ylim((0, 1.05))
        # ax1.c('accuracy')
        ax1.set_xlabel('epoch')
        ax1.legend(['train', 'test'], loc='lower right')
        # ax1.show()
        # summarize history for loss
        ax2.plot(history['loss'])
        ax2.plot(history['val_loss'])
        ax2.set_title('model loss')
        ax2.set_xlabel('loss')
        ax2.set_xlabel('epoch')
        ax2.legend(['train', 'test'], loc='upper right')
        # print(result_path + str(dt.datetime.now()) + '-' + name + '-result')
        fig = plt.gcf()
        try:
            save_file = (dt.datetime.now()).strftime("%Y-%m-%d-%H+%M+%S") + '=' + self.subject + '=result.png'
            plt.savefig(os.getcwd() + '\\data\\figures\\' + save_file, bbox_inches='tight')
            print(save_file + " :figure saved successfully!")
            # Plot after saving to avoid a weird tkinter exception
            plt.interactive(False)
            plt.show()
            # plt.close()
        except Exception as e:
            print(e)
            pass

    def PredictGestures(self, number_of_samples: int = number_of_samples):
        # Initializing array for verification_averages
        validation_averages = np.zeros((int(self.averages), 8))

        model = load_model(self.result_path + self.trained_model_path + self.subject + '_realistic_model.h5')
        start_time = 0
        hub = myo.Hub()
        average = 0.0
        counter = 100
        while counter > 0:
            start_time = datetime.datetime.now()
            # region PREDICT
            try:

                # print("Show a foot gesture and press ENTER to get its classification!")

                listener = Listener(number_of_samples)
                hub.run(listener.on_event, 20000)  # 1000 * 20 = 20000 for enough samples
                # Here we send the received number of samples making them a list of 1000 rows 8 columns
                self.validation_set = np.array((data_array[0]))
                data_array.clear()
            except Exception as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                pass

            self.validation_set = np.absolute(self.validation_set)
            # print(self.validation_set.shape)

            # We add one because iterator below starts from 1
            batches = int(self.number_of_samples / self.div) + 1
            for i in range(1, batches):
                validation_averages[i - 1, :] = np.mean(self.validation_set[(i - 1) * self.div:i * self.div, :], axis=0)

            validation_data = validation_averages
            # print("Verification matrix shape is ", validation_data.shape)

            predictions = model.predict(validation_data, batch_size=self.training_batch_size)
            predicted_value = np.argmax(predictions[0])
            # endregion
            end_time = datetime.datetime.now()
            execution_time = (end_time - start_time).total_seconds() * 1000
            average += execution_time
            print(execution_time)
            print(self.exercise_labels[predicted_value])
            time.sleep(.5)
            counter -= 1
        average = average / 100
        print(average)
        # pause


class CustomCallback(keras.callbacks.Callback):

    def on_epoch_begin(self, epoch, logs=None):
        # keys = list(logs.keys())
        # print("Start epoch {} of training; got log keys: {}".format(epoch, keys))
        # print("Start epoch {} of training; counter: {}".format(epoch, epoch_counter))
        pass

    def on_epoch_end(self, epoch, logs=None):
        global epoch_counterpi
        # keys = list(logs.keys())
        epoch_counter = epoch + 1
        # print("End epoch {} of training; got log keys: {}".format(epoch, epoch_counter))


if __name__ == '__main__':
    # Exercises:
    # 1. tip toe standing
    # 2. toe crunches
    # 3. toe stand - TOO similar to toe crunches
    # 4. toes UP
    # 5. rest

    dummy = ClassifyExercises(
        subject="Ervin",
        nr_of_samples=number_of_samples,
        nr_of_gestures=4,
        exercise_labels=["Tip Toe", "Toe Crunches", "Toes UP", "Rest"],
        batch_size=50,
        training_batch_size=16
    )
    # dummy.PrepareTrainingData()
    # dummy.TrainEMG()
    # dummy.DisplayResults()
    dummy.PredictGestures()
