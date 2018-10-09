from task import Task, count
from json import load, dump


class Persister:
    def __init__(self, path):
        self.path = path

    def init_tasks(self):
        if not self.path.exists():
            return dict()

        with open(self.path, "r") as f:
            data = load(f)
            # Ensure new tasks get a unique id
            highest_id = max(data, key=lambda x: x["id"])["id"]
            Task.id_generator = count(highest_id + 1)

            return {task["id"]: Task.from_dict(task) for task in data}

    def persist(self, tasks):
        """Persists all tasks to a file"""

        with open(self.path, "w") as f:
            all_tasks = [task.to_dict() for task in tasks.values()]
            dump(all_tasks, f)
