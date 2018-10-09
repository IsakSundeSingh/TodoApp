from task import Task, count
from json import dump, load
from pathlib import Path

# If imported input implicitly uses it and provides features from it
# such as history
try:
    import readline
except ModuleNotFoundError:
    pass


class Application:
    def __init__(self):
        self.tasks = self.init_tasks()
        self.commands = {
            'add': self.add_task,
            'do': self.do_task,
            'undo': self.undo_task,
            'print': lambda *args: [print(task) for task in (self.tasks.values() or ["No tasks"])],
            'quit': lambda x: quit()
        }

    def init_tasks(self):
        if not task_file.exists():
            return dict()

        with open(task_file, "r") as f:
            data = load(f)
            # Ensure new tasks get a unique id
            highest_id = max(data, key=lambda x: x["id"])["id"]
            Task.id_generator = count(highest_id + 1)

            return {task["id"]: Task.from_dict(task) for task in data}

    def show_usage(self, *args):
        print("""Usage:
    Add <text>  - Add a new tasks
    Print       - Show all tasks
    Do #        - Complete a task
    Undo #      - Undo a completed task
    Quit        - Quit the application""")

    def persist(self):
        """Persists all tasks to a file"""

        with open(task_file, "w") as f:
            all_tasks = [task.to_dict() for task in self.tasks.values()]

            dump(all_tasks, f)

    def add_task(self, text):
        task = Task(" ".join(text))
        self.tasks[task.id] = task
        self.persist()
        print(task)

    def do_task(self, numbers):
        for num in numbers:
            task = self.tasks[int(num)]
            print(f"Completed {task}")
            task.complete()

        self.persist()

    def undo_task(self, numbers):
        for num in numbers:
            task = self.tasks[int(num)]
            task.uncomplete()
            print(f"Undid task {task}")

        self.persist()

    def run(self):
        while True:
            command = input("> ")
            if not command:
                self.show_usage()
                continue

            cmd, *args = command.split()

            self.commands.get(cmd.lower(), self.show_usage)(args)


if __name__ == "__main__":
    task_file = Path("tasks.json")
    Application().run()
