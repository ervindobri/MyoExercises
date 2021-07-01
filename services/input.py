import time
from pynput.keyboard import Key, Controller
# Predefined input keys
from constants.variables import PREDEFINED_EXERCISES


class InputController:
    def __init__(self, input_map=None):
        print("Initializing input controller...")
        if input_map is None:
            input_map = {PREDEFINED_EXERCISES[0]}

        self.input_map = input_map
        self.keyboard = Controller()
        self.last_key = None

    def simulateKeyHold(self, key):
        if self.last_key is None:
            self.last_key = key
            self.keyboard.press(key)
        else:
            if self.last_key == key:
                print("Holding!")
                pass
            else:
                print("Not holding anymore.")
                self.keyboard.release(self.last_key)
                self.last_key = key
                self.keyboard.press(key)

    def simulateKeyWithInstantRelease(self, key):
        self.last_key = key
        self.keyboard.press(key)
        time.sleep(0.2)
        self.keyboard.release(key)

    def simulateKey(self, assigned_key):
        if assigned_key[1] is not None:
            # Hold the key
            if assigned_key[2] == True:
                self.simulateKeyHold(assigned_key[1])
            # press and release after delay
            else:
                self.simulateKeyWithInstantRelease(assigned_key[1])
        else:
            if self.last_key is not None:
                self.keyboard.release(self.last_key)
                self.last_key = None


    def startTest(self):
        self.keyboard.press(Key.space)
        self.keyboard.release(Key.space)
        print("Space pressed!")


if __name__ == '__main__':
    input_map = PREDEFINED_EXERCISES
    controller = InputController(input_map=input_map)
    controller.simulateKey(PREDEFINED_EXERCISES["R"])
