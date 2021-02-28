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

    def simulateKey(self, exercise: Exercise):
        if exercise not in self.input_map.keys():
            print("Exercise not in input map!")

        key = self.input_map[exercise]
        self.keyboard.press(key)
        self.keyboard.release(key)
        print(key, " - Key pressed successfully!")

    def startTest(self):
        self.keyboard.press(Key.space)
        self.keyboard.release(Key.space)
        print("Space pressed!")


if __name__ == '__main__':
    input_map = PREDEFINED_EXERCISES
    controller = InputController(input_map=input_map)
    controller.simulateKey(PREDEFINED_EXERCISES["R"])
