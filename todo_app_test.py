from unittest import main, TestCase, skip
from persister import Persister
from task import Task
from todo_app import Application


class MockPersister:
    def __init__(self, data):
        self.data = data
        self.stored = []

    def load(self):
        return self.data

    def store(self, tasks):
        task_dicts = [task.to_dict() for task in tasks.values()]
        self.stored.extend(task_dicts)


class TestApplication(TestCase):
    def setUp(self):
        self.inputs = []
        self.outputs = []

        self.data = {}

        self.persister = MockPersister(self.data)

        def inputter(*args):
            if self.inputs:
                return self.inputs.pop(0)
            return "quit"

        def outputter(format, *args):
            self.outputs.append(format % args)

        self.inputter = inputter
        self.outputter = outputter

    def test_can_add_tasks(self):
        task_text = "Some new task"
        self.inputs = [f"Add {task_text}"]
        app = Application(self.persister, self.inputter, self.outputter)

        app.run()

        self.assertRegex(self.outputs[0], f"#(\\d+) {task_text}")
        self.assertEqual(len(self.data), 1)
        self.assertEqual(task_text, self.persister.stored[0]["text"])

    def test_can_do_tasks(self):
        task_data = {"id": 1, "text": "Run tests", "completed": False}
        expected = {**task_data, "completed": True}
        task = Task.from_dict(task_data)
        self.data.update({task.id: task})
        self.inputs = ["Do 1"]
        app = Application(self.persister, self.inputter, self.outputter)

        app.run()

        self.assertEqual(f"Completed #1 {task.text}", self.outputs[0])
        self.assertEqual(expected, self.persister.stored[0])

    def test_can_undo_tasks(self):
        expected = {"id": 1, "text": "Run tests", "completed": False}
        task = Task.from_dict(expected)
        self.data.update({task.id: task})
        self.inputs = ["Do 1", "Undo 1"]
        app = Application(self.persister, self.inputter, self.outputter)

        app.run()

        self.assertEqual(f"Undid #1 {task.text}", self.outputs[1])
        self.assertEqual(expected, self.persister.stored[1])

    def test_cannot_add_empty_task(self):
        expected = "Cannot add empty task"
        self.inputs = ["add"]
        app = Application(self.persister, self.inputter, self.outputter)

        app.run()

        self.assertEqual(expected, self.outputs[0])

    def test_can_do_and_undo_with_and_without_hashtag(self):
        expected = [
            "Completed #1 Test stuff",
            "Undid #1 Test stuff",
            "Completed #1 Test stuff",
            "Undid #1 Test stuff"
        ]
        task = Task.from_dict({"id": 1, "text": "Test stuff", "completed": False})
        self.data.update({task.id: task})
        self.inputs = ["do 1", "undo #1", "do #1", "undo 1"]
        app = Application(self.persister, self.inputter, self.outputter)

        app.run()

        self.assertEqual(expected, self.outputs)


if __name__ == "__main__":
    main()
