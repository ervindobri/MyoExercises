from enum import Enum

from numpy.core.multiarray import zeros
global data_array
data_array = []

number_of_samples = 100  # change this
Sensor1 = zeros((1, number_of_samples))
Sensor2 = zeros((1, number_of_samples))
Sensor3 = zeros((1, number_of_samples))
Sensor4 = zeros((1, number_of_samples))
Sensor5 = zeros((1, number_of_samples))
Sensor6 = zeros((1, number_of_samples))
Sensor7 = zeros((1, number_of_samples))
Sensor8 = zeros((1, number_of_samples))

PROC_NAME = "Myo Connect.exe"
PROC_PATH = 'C:\\Program Files (x86)\\Thalmic Labs\\Myo Connect\\' + PROC_NAME

DATA_PATH = 'training_data\\'
MODEL_PATH = 'trained_model\\'


class Exercise(Enum):
    TIP_TOE = 1
    TOE_CRUNCH = 2
    TOES_UP = 3
    REST = 3
