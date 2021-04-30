class Patient:
    def __init__(self, name, age, exercises):
        self.name = name
        self.age = age
        if exercises is None:
            self.exercises = {}
        self.exercises = exercises

    def __str__(self):
        return "Name:" + self.name + ", Age:" + self.age + ", nr.of Exercises:" + len(self.exercises)
