from itertools import count


class Task:
    id_generator = count(1)

    def __init__(self, text):
        if not text or not isinstance(text, str):
            raise ValueError("Cannot create empty task")

        self.text = text
        self.id = next(self.id_generator)
        self.completed = False

    def __str__(self):
        if self.completed:
            text = '\u0336' + '\u0336'.join(self.text)
            return f"#{self.id} {text}"

        return f"#{self.id} {self.text}"

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def complete(self):
        self.completed = True

    def uncomplete(self):
        self.completed = False

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, dictionary):
        self = cls.__new__(cls)
        default = {"id": -1, "completed": False, "text": "Invalid"}
        self.__dict__ = {**default, **dictionary.copy()}
        return self
