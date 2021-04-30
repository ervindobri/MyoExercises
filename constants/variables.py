import os
from enum import Enum

from numpy.core.multiarray import zeros
from pynput.keyboard import Key, KeyCode

from models.exercise import Exercise

data_array = []
streamed_data = []

number_of_samples = 500
validation_samples = 50


# Sensor1 = zeros((1, number_of_samples))
# Sensor2 = zeros((1, number_of_samples))
# Sensor3 = zeros((1, number_of_samples))
# Sensor4 = zeros((1, number_of_samples))
# Sensor5 = zeros((1, number_of_samples))
# Sensor6 = zeros((1, number_of_samples))
# Sensor7 = zeros((1, number_of_samples))
# Sensor8 = zeros((1, number_of_samples))


def change_sample_size(n):
    global number_of_samples, Sensor1, Sensor2, Sensor3, Sensor4, Sensor5, Sensor6, Sensor7, Sensor8
    number_of_samples = n
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

RESULT_PATH = os.getcwd() + '\\data\\results\\'
PATIENTS_PATH = os.getcwd() + '\\data\\patients\\'
FIGURES_PATH = os.getcwd() + '\\data\\figures\\'
FULL_MODEL_PATH = os.getcwd() + '\\data\\results\\trained_model\\'
DATA_PATH = 'training_data\\'
MODEL_PATH = 'trained_model\\'
MEASURED_PATH = 'measurements\\'
MAPPED_KEYS_PATH = os.getcwd() + '\\data\\results\\mapped_keys\\'
RESOURCES_PATH = os.getcwd() + '\\resources\\'
IMAGES_PATH = RESOURCES_PATH + 'images\\'
KEYS = {
    "UP": Key.up,
    "DOWN": Key.down,
    "LEFT": Key.left,
    "RIGHT": Key.right,
    "NONE": Key.menu
}

SUPPORTED_KEYS = {
    "UP": Key.up,
    "DOWN": Key.down,
    "LEFT": Key.left,
    "RIGHT": Key.right,
    "SPACE": Key.space,
    "W": KeyCode.from_char('w'),
    "A": KeyCode.from_char('a'),
    "S": KeyCode.from_char('s'),
    "D": KeyCode.from_char('d'),
}

# class Exercise(Enum):
#     TIP_TOE = 1
#     TOE_CRUNCH = 2
#     TOES_UP = 3
#     REST = 3

PREDEFINED_REPS = ['5', '10', '15']
PREDEFINED_EXERCISES = [
    Exercise(name="Tip Toe", code="TT", instruction="Stand on your toes!", assigned_key=("UP", KEYS["UP"])),
    Exercise(name="Toe Crunches", code="TC", instruction="Crunch your toes like a fist!",
             assigned_key=("LEFT", KEYS["LEFT"])),
    Exercise(name="Toes UP", code="UP", instruction="Move your toes up!", assigned_key=("RIGHT", KEYS["RIGHT"])),
    Exercise(name="Rest", code="R", instruction="Rest your feet...", assigned_key=("NONE", None)),
]
