from pynput.keyboard import Key


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

    def serialize(self):
        return {
            "name": self.name,
            "code": self.code,
            "instruction": self.instruction,
            "assigned_key": self.assigned_key[0],  # tuple ("UP", Key.up)
        }


