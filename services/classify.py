import json
import threading
from os import listdir
from os.path import isfile, join

import myo
import numpy as np
from tensorflow.keras.activations import softmax, relu
from tensorflow import keras
from keras import regularizers
from keras.models import load_model
import matplotlib.pyplot as plt
# from tensorflow_addons.callbacks.tqdm_progress_bar import TQDMProgressBar

# New Imports
import warnings
import time
import datetime as dt
import pickle

from tensorflow_addons.callbacks import TQDMProgressBar

from constants.variables import data_array, DATA_PATH, MODEL_PATH, streamed_data, \
    PREDEFINED_EXERCISES, RESULT_PATH, FIGURES_PATH, MEASURED_PATH, validation_samples, \
    PATIENTS_PATH, number_of_samples, FULL_MODEL_PATH
from models.patient import Patient
from services.firestore import FirestoreDatabase
from services.myo_helpers import Listener, MyoService, ForeverListener, PredictListener

from services.input import InputController

# matplotlib.use('Qt5Agg')
epoch_counter = 0


class ClassifyExercises:
    def __init__(self,
                 subject: str = None,
                 age: int = 0,
                 exercises=None,
                 epochs: int = 300,
                 batch_size: int = 25,
                 training_batch_size: int = 32,
                 input_controller: InputController = None, ):

        self.firestore = FirestoreDatabase()
        self.subject = subject
        self.age = age

        if exercises is None:
            self.exercises = []

        self.exercises = exercises
        self.number_of_gestures = len(self.exercises)
        self.epoch_counter = 0

        if input_controller is None:
            self.input_controller = InputController()

        self.epochs = epochs
        self.training_batch_size = training_batch_size

        ''' batch_size '''
        self.div = batch_size  # every 50 batch ( 1000/50 -> 20 data )

        self.averages = int(number_of_samples / batch_size)
        self.validation_averages = int(validation_samples / (batch_size / 10))
        self.all_training_set = {}
        self.all_averages = []

        for i in range(0, self.number_of_gestures):
            self.all_training_set[i] = np.zeros((8, number_of_samples))
            self.all_averages.append(np.zeros((int(self.averages), 8)))

        self.validation_set = np.zeros((8, number_of_samples))
        self.training_set = np.zeros((8, number_of_samples))

        self.listener = Listener(number_of_samples)
        self.myoService = MyoService()
        self.hub = myo.Hub()

    def PrepareTrainingData(self):
        # This function kills Myo Connect.exe and restarts it to make sure it is running
        while not self.myoService.restart_process():
            pass

        # Wait for 3 seconds until Myo Connect.exe starts
        time.sleep(3)
        for x in range(0, len(self.exercises)):
            # Take current exercise from dict.
            exercise = self.exercises[x]
            # Log current instructions
            instructions = exercise.instruction
            print("Instructions: ", instructions)
            time.sleep(0.5)
            while True:
                try:
                    hub = myo.Hub()
                    listener = Listener(number_of_samples)
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

            print(exercise.name, "data ready")
            time.sleep(1)

        self.hub.stop()

        result_array = self.CalculateAllMeanData()
        self.SaveProcessedData(result_array)

    def UpdateExerciseList(self, itemsTextList):
        new_exercises = []
        self.all_training_set = {}
        self.all_averages = []
        for x in range(len(itemsTextList)):
            exercise = next(ex for ex in PREDEFINED_EXERCISES if ex.name == itemsTextList[x])
            new_exercises.append(exercise)
            self.all_training_set[x] = np.zeros((8, number_of_samples))
            self.all_averages.append(np.zeros((int(self.averages), 8)))

        print("New exercises:", len(new_exercises))
        self.exercises = new_exercises
        self.number_of_gestures = len(new_exercises)

    def RecordExercise(self, exercise_name):
        hub = myo.Hub()
        exercise = self.exercises[0]
        index = 0
        result = 0
        for ex in self.exercises:
            if ex.name == exercise_name:
                exercise = ex
                index = self.exercises.index(ex)

        print("Exercise name:", exercise.name, ", index: ", index)
        try:
            listener = Listener(number_of_samples)
            hub.run(listener.on_event, 3000)
            current_training_set = np.array((data_array[0]))
            print(current_training_set)
            data_array.clear()
            print(exercise.name, "data ready")
            result_array = self.CalculateMeanData(current_training_set)
            self.all_averages[index] = result_array
            result = 1
        except Exception as e:
            print(e)
            result = 0

        self.hub.stop()
        return result
        # self.SaveProcessedData(result_array)

    # This method is responsible for training EMG data - requirements: loading back .txt data,
    def TrainEMG(self):
        labels = []

        print("Loading data from disk!")
        prepare_array = np.loadtxt(RESULT_PATH + DATA_PATH + self.subject + '-' + str(self.age) + '.txt')

        # This division is to make the iterator for making labels run 20 times in inner loop and 3 times in outer loop
        # running total 60 times for 3 foot gestures
        samples = 20
        self.number_of_gestures = int(prepare_array.shape[0] / samples)
        print("Preprocess EMG data of ", self.subject, "with ", samples, " samples per", self.number_of_gestures,
              "exercise, training data with a nr. of ",
              self.training_batch_size, "batch size, for a total of ", self.epochs, "epochs.")

        # Now we append all data in training label
        # We iterate to make 3 finger movement labels.
        for i in range(0, self.number_of_gestures):
            for j in range(0, int(samples)):
                labels.append(i)
        labels = np.asarray(labels)
        print("Labels: ", labels, len(labels), type(labels))
        # print(conc_array.shape[0])

        permutation_function = np.random.permutation(prepare_array.shape[0])
        total_samples = prepare_array.shape[0]
        all_shuffled_data, all_shuffled_labels = np.zeros((total_samples, 8)), np.zeros((total_samples, 8))

        all_shuffled_data, all_shuffled_labels = prepare_array[permutation_function], labels[permutation_function]
        # print(all_shuffled_data.shape)
        # print(all_shuffled_labels.shape)

        number_of_training_samples = int(np.floor(0.8 * total_samples))
        number_of_validation_samples = int(total_samples - number_of_training_samples)

        # train_data = np.zeros((number_of_training_samples, 8))
        # train_labels = np.zeros((number_of_training_samples, 8))

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
            keras.layers.Dense(8, activation=relu, input_dim=8, kernel_regularizer=regularizers.l2(0.1)),
            keras.layers.BatchNormalization(),
            keras.layers.Dense(self.number_of_gestures, activation=softmax)])

        adam_optimizer = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0,
                                               amsgrad=False)
        model.compile(
            optimizer=adam_optimizer,
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

        print("Fitting training data to the model...")
        tqdm_callback = TQDMProgressBar(
            show_epoch_progress=False,
            leave_overall_progress=False,
            leave_epoch_progress=False
        )
        history = model.fit(train_data, train_labels, epochs=self.epochs,
                            validation_data=(validation_data, validation_labels),
                            batch_size=self.training_batch_size, verbose=0, callbacks=[tqdm_callback])

        instructions = "Training model successful!"
        print(instructions)

        save_path = RESULT_PATH + MODEL_PATH + self.subject + '-' + str(self.age) + '_model.h5'
        model.save(save_path)
        print("Saving model for later...")

        self.SaveModelHistory(history)

    def SaveModelHistory(self, history):
        filepath = RESULT_PATH + MODEL_PATH + self.subject + '-' + str(self.age) + '.history'
        with open(filepath, 'wb') as file_pi:
            pickle.dump(history.history, file_pi)

    def CalculateMeanData(self, data):
        training_set = np.absolute(data)
        current_average = np.zeros((int(self.averages), 8))
        for i in range(1, self.averages + 1):
            current_average[i - 1, :] = np.mean(training_set[(i - 1) * self.div:i * self.div, :], axis=0)

        return current_average

    def CalculateAllMeanData(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            # Calculate Absolutes of foot gesture data - every EXERCISE set -> tiptoe, toe crunches, rest. etc...
            for x in range(0, self.number_of_gestures):
                self.all_training_set[x] = np.absolute(self.all_training_set[x])

            # Here we are calculating the mean values of all foot exercise data storing them as n/50 samples
            # because 50 batches of n samples is equal to n/50 averages
            for i in range(1, self.averages + 1):
                for x in range(0, self.number_of_gestures):
                    print("Gesture:", x, " - Mean: ")
                    self.all_averages[x][i - 1, :] = np.mean(
                        self.all_training_set[x][(i - 1) * self.div:i * self.div, :], axis=0)

            # Here we stack all the data row wise
            conc_array = np.concatenate(self.all_averages, axis=0)
            return conc_array

    def DataAvailable(self):
        if self.subject is not None:
            files = [f for f in listdir(RESULT_PATH + DATA_PATH) if isfile(join(RESULT_PATH + DATA_PATH, f))]
            if self.subject + '-' + str(self.age) + '.txt' in files:
                print("Data available!")
                return True
        print("No data!")
        return False

    def SaveProcessedData(self, array=None):
        try:
            print("Trying  to save data...")
            if array is None:
                array = np.concatenate(self.all_averages, axis=0)
            with open(PATIENTS_PATH + self.subject + '-' + str(self.age) + '.json', 'w') as f:
                exercises = [x.code for x in self.exercises]
                content = {
                    "Name": self.subject,
                    "Age": self.age,
                    "Exercises": exercises
                }
                json.dump(content, f)
                f.close()
            np.savetxt(RESULT_PATH + DATA_PATH + self.subject + '-' + str(self.age) + '.txt', array, fmt='%i')
            instructions = "Saving training data successful!"
            print(instructions)
            # self.prepare_array = array

        except Exception as e:
            print(e)
            instructions = "Saving training data failed!"
            print(instructions)

    def SavePatientData(self):
        exercises = dict((ex.code, ex.assigned_key[0]) for ex in self.exercises)
        patient = Patient(
            self.subject,
            self.age,
            exercises
        )
        self.firestore.set_patient_data(patient)

    # This function plots results for validation and training data for a certain subject
    def DisplayResults(self):
        try:
            filepath = RESULT_PATH + MODEL_PATH + self.subject + '-' + str(self.age) + '.history'
            print(filepath)
            history = pickle.load(open(filepath, "rb"))
            print("Model load successful")
        except FileNotFoundError:
            print("No such model! Please check name and/or age.")
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

        try:
            # self.savePlot(plt)
            # Plot after saving to avoid a weird tkinter exception
            plt.interactive(False)
            plt.show()
        except Exception as e:
            print(e)
            pass

    def savePlot(self, plot):
        save_file = self.subject + '_' + (dt.datetime.now()).strftime("%Y-%m-%d-%H+%M+%S") + '_train.png'
        plot.savefig(FIGURES_PATH + save_file, bbox_inches='tight')
        print(save_file + " :figure saved successfully!")

    def PredictGestures(self):
        # Initializing array for verification_averages
        validation_averages = np.zeros((int(self.averages), 8))

        model = load_model(RESULT_PATH + MODEL_PATH + self.subject + '-' + str(self.age) + '_model.h5')
        hub = myo.Hub()
        average = 0.0
        counter = 100

        print("Predicting gestures with ", validation_samples, "nr. of samples.")
        while counter > 0:
            start_time = dt.datetime.now()
            # region PREDICT
            try:
                # print("Show a foot gesture and press ENTER to get its classification!")
                listener = Listener(validation_samples)
                hub.run(listener.on_event, 1000)  # 1000 * 20 = 20000 for enough samples
                # Here we send the received number of samples making them a list of 1000 rows 8 columns
                self.validation_set = np.array((data_array[0]))
                data_array.clear()
                print(self.validation_set.shape)
            except Exception as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                pass

            self.validation_set = np.absolute(self.validation_set)
            # print(self.validation_set.shape)

            # We add one because iterator below starts from 1
            batches = int(validation_samples / self.div) + 1
            for i in range(1, batches):
                validation_averages[i - 1, :] = np.mean(self.validation_set[(i - 1) * self.div:i * self.div, :], axis=0)

            validation_data = validation_averages
            # print("Verification matrix shape is ", validation_data.shape)

            predictions = model.predict(validation_data, batch_size=self.training_batch_size)
            predicted_value = np.argmax(predictions[0])
            # endregion
            end_time = dt.datetime.now()
            execution_time = (end_time - start_time).total_seconds() * 1000
            average += execution_time
            print(list(self.exercises.values())[predicted_value].name)
            time.sleep(.5)
            counter -= 1
        average = average / 100
        print(average)
        # pause

    def LoadModel(self):
        self.model = load_model(FULL_MODEL_PATH + self.subject + '-' + str(self.age) + '_model.h5')

    def calculate_validated_data(self, current_data):
        validation_averages = np.zeros((int(self.validation_averages), 8))
        self.validation_set = np.array(current_data)
        self.validation_set = np.absolute(self.validation_set)
        # We add one because iterator below starts from 1
        batches = int(validation_samples / self.div) + 1  # 50/25 => 2+1 = 3
        for i in range(1, batches):
            validation_averages[i - 1, :] = np.mean(self.validation_set[(i - 1) * self.div:i * self.div, :],
                                                    axis=0)

        return validation_averages

    def Predict(self):
        listener = PredictListener(validation_samples)
        self.hub.run(listener.on_event, 500)
        while len(streamed_data) < validation_samples:
            pass

        current_data = streamed_data[-validation_samples:]  # get last nr_of_samples elements from list
        validation_data = self.calculate_validated_data(current_data)
        predictions = self.model.predict(validation_data, batch_size=self.training_batch_size)
        predicted_value = np.argmax(predictions[0])
        streamed_data.clear()
        return predicted_value, self.exercises[predicted_value].name

    def PressKey(self, predicted_value):
        self.input_controller.simulateKeyWithInstantRelease(self.exercises[predicted_value])
        print("Pressed key:", self.exercises[predicted_value].name)

    def TestPredict(self, reps=50, exercise_index=0):
        import keyboard
        validation_averages = np.zeros((int(self.averages), 8))
        model = load_model(RESULT_PATH + MODEL_PATH + self.subject + '-' + str(self.age) + '_model.h5')

        average = 0.0
        correct_predictions = 0
        predict_average = 0.0
        # Current exercise
        exercise = list(self.exercises.values())[exercise_index]
        measured = {}

        listener = ForeverListener(number_of_samples)

        thread = threading.Thread(target=lambda: self.hub.run_forever(listener.on_event, 100))
        thread.start()

        print("Recording", exercise.name)
        print("------------------------")
        count = 0
        while count < reps + 1:
            try:
                key = input('Press a key')
                streamed_data.clear()
                start_time = time.time()

                if keyboard.is_pressed("s"):
                    break
                if key == "b":

                    # region STUFF

                    while len(streamed_data) < number_of_samples:
                        pass

                    predict_start_time = time.time()
                    current_data = streamed_data[-number_of_samples:]  # get last nr_of_samples elements from list
                    self.validation_set = np.array(current_data)
                    self.validation_set = np.absolute(self.validation_set)

                    # We add one because iterator below starts from 1
                    batches = int(number_of_samples / self.div) + 1
                    for i in range(1, batches):
                        validation_averages[i - 1, :] = np.mean(self.validation_set[(i - 1) * self.div:i * self.div, :],
                                                                axis=0)

                    validation_data = validation_averages
                    predictions = model.predict(validation_data, batch_size=validation_data.shape[1])
                    predicted_value = np.argmax(predictions[0])
                    end_time = time.time()
                    predict_execution_time = (end_time - predict_start_time) * 1000
                    execution_time = (end_time - start_time) * 1000
                    print("Predicted exercise:", list(self.exercises.values())[predicted_value].name,
                          " Prediction time: ", predict_execution_time, "ms, from total execution time: ",
                          execution_time, "ms")

                    if count > 0:
                        measured[count] = execution_time
                        average += execution_time
                        predict_average += predict_execution_time
                        if exercise == list(self.exercises.values())[predicted_value]:
                            correct_predictions += 1
                        # endregion
                    count += 1

            except Exception as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                pass

        print("Stopping hub & joining thread.")

        self.hub.stop()
        thread.join()
        measured["Average"] = average / reps
        measured["Prediction Average"] = predict_average / reps
        measured["Accuracy"] = correct_predictions / reps
        print("Average:", measured["Average"])
        print("Prediction Average:", measured["Prediction Average"])
        print("Accuracy per", reps, ": ", measured["Accuracy"] * 100, "%")
        print("Saving measured data...")
        self.SaveMeasurement(exercise, measured)

    def SaveMeasurement(self, exercise, content):
        import json
        print("file:", MEASURED_PATH + self.subject + '-' + exercise.code + '-' + (dt.datetime.now()).strftime(
            "%Y-%m-%d-%H+%M+%S"))
        with open(RESULT_PATH + MEASURED_PATH + self.subject + '-' + exercise.code + '-' + (dt.datetime.now()).strftime(
                "%Y-%m-%d-%H+%M+%S") + '.json', "w") as f:
            json.dump(content, f)
            f.close()
