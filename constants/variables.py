import os
from enum import Enum

from numpy.core.multiarray import zeros
from pynput.keyboard import Key

global data_array, streamed_data
data_array = []
streamed_data = []

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

RESULT_PATH = os.getcwd() + '\\data\\results\\'
FIGURES_PATH = os.getcwd() + '\\data\\figures\\'

DATA_PATH = 'training_data\\'
MODEL_PATH = 'trained_model\\'
MAPPED_KEYS_PATH = 'data\\results\\mapped_keys'
KEYS = {
    "UP": Key.up,
    "DOWN": Key.down,
    "LEFT": Key.left,
    "RIGHT": Key.right,
}


class Exercise:
    def __init__(self,
                 name: str = "Exercise",
                 code: str = "EX",  # abbreviation of exercise name
                 instruction: str = "Do this, do that!",
                 assigned_key: Key = Key.space):
        self.name = name
        self.code = code
        self.instruction = instruction
        self.assigned_key = assigned_key


# class Exercise(Enum):
#     TIP_TOE = 1
#     TOE_CRUNCH = 2
#     TOES_UP = 3
#     REST = 3

PREDEFINED_EXERCISES = {
    "TT": Exercise(name="Tip Toe", code="TT", instruction="Stand on your toes!", assigned_key=("UP", KEYS["UP"])),
    "TC": Exercise(name="Toe Crunches", code="TC", instruction="Crunch your toes like a fist!",
                   assigned_key=("LEFT", KEYS["LEFT"])),
    "UP": Exercise(name="Toes UP", code="UP", instruction="Move your toes up!", assigned_key=("RIGHT", KEYS["RIGHT"])),
    "R": Exercise(name="Rest", code="R", instruction="Rest your feet...", assigned_key=("DOWN", KEYS["DOWN"])),
}
