from pynput.keyboard import Key, Controller

# Predefined input keys
from constants.variables import Exercise

up = Key.up
down = Key.down
left = Key.left
right = Key.rightpip


class InputController:
    def __init__(self, input_map=None):
        print("Initializing input controller...")
        if input_map is None:
            input_map = {Exercise.REST: down}

        self.input_map = input_map
        self.keyboard = Controller()

    def simulateKey(self, exercise: Exercise):
        if exercise not in self.input_map.keys():
            print("Exercise not in input map!")
        key = self.input_map[exercise]
        self.keyboard.press(key)
        self.keyboard.release(key)
        print(key, " - Key pressed successfully!")


if __name__ == '__main__':
    input_map = {
        Exercise.TIP_TOE: up,
        Exercise.TOE_CRUNCH: left,
        Exercise.TOES_UP: right,
        Exercise.REST: down,
    }
    controller = InputController(input_map=input_map)
    controller.simulateKey(Exercise.REST)
