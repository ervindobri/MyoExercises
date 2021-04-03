import threading
import time

from pynput.keyboard import Key, Controller

# Predefined input keys
from constants.variables import Exercise, PREDEFINED_EXERCISES


class InputController:
    def __init__(self, input_map=None):
        print("Initializing input controller...")
        if input_map is None:
            input_map = {PREDEFINED_EXERCISES["R"]}

        self.input_map = input_map
        self.keyboard = Controller()
        self.last_key = None

    def simulateKey(self, exercise):
        if exercise.assigned_key[1] is not None:
            if self.last_key is not None and self.last_key != exercise.assigned_key[1]:
                self.keyboard.release(self.last_key) 
            self.keyboard.press(exercise.assigned_key[1])
            self.last_key = exercise.assigned_key[1]
            # print(exercise.assigned_key[1], " - Key pressed successfully!")


    def startTest(self):
        self.keyboard.press(Key.space)
        self.keyboard.release(Key.space)
        print("Space pressed!")


if __name__ == '__main__':
    input_map = PREDEFINED_EXERCISES
    controller = InputController(input_map=input_map)
    controller.simulateKey(PREDEFINED_EXERCISES["R"])
