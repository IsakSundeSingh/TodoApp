from unittest import main, TestCase
from task import Task


class TestTask(TestCase):
    def test_task_has_id(self):
        task = Task("Some data")
        self.assertGreaterEqual(task.id, 1)

    def test_tasks_have_unique_ids(self):
        task_1 = Task("Am I unique?")
        task_2 = Task("Am I unique?")
        self.assertNotEqual(task_1.id, task_2.id)

    def test_correct_string_representation(self):
        task_text = "Buy milk"
        task = Task(task_text)
        self.assertRegex(str(task), "#(\\d+) Buy milk")

    def test_raises_on_empty_task_text(self):
        with self.assertRaises(ValueError):
            Task("")

    def test_raises_on_invalid_text_type(self):
        with self.assertRaises(ValueError):
            Task({1, 2, 3})

    def test_new_tasks_are_not_completed(self):
        task = Task("Write good code")

        self.assertEqual(task.completed, False)

    def test_tasks_can_be_completed(self):
        task = Task("Complete this")
        task.complete()
        self.assertTrue(task.completed)

    def test_completed_tasks_can_be_undone(self):
        task = Task("Get a grip of your life!")
        task.complete()

        task.uncomplete()
        self.assertFalse(task.completed)

    def test_can_be_constructed_from_dict(self):
        data = {"id": 14, "text": "Well hello there", "completed": False}
        expected = Task(data["text"])
        expected.id = data["id"]
        expected.completed = data["completed"]

        task = Task.from_dict(data)

        self.assertEqual(task, expected)


if __name__ == "__main__":
    main()
