
def count(n):
    while True:
        yield n
        n += 1


id_generator = count(1)


class Task:
    def __init__(self, text):
        if not text or not isinstance(text, str):
            raise ValueError("Cannot create empty task")

        self.text = text
        self.id = next(id_generator)
        self.completed = False

    def __str__(self):
        return f"#{self.id} {self.text}"

    def complete(self):
        self.completed = True

    def uncomplete(self):
        self.completed = False

    @classmethod
    def from_dict(cls, dictionary):
        self = cls.__new__(cls)
        default = {"id": -1, "completed": False, "text": "Invalid"}
        self.__dict__ = {**default, **dictionary.copy()}
        return self

    def to_dict(self):
        return self.__dict__

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
