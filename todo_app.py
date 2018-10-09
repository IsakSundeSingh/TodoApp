from task import Task
from persister import Persister
from pathlib import Path

# If imported input implicitly uses it and provides features from it
# such as history
try:
    import readline
except ModuleNotFoundError:
    pass


class Application:
    def __init__(self, persister, inputter, outputter):
        self.persister = persister
        self.inputter = inputter
        self.outputter = outputter
        self.tasks = self.persister.init_tasks()
        self.commands = {
            'add': self.add_task,
            'do': self.do_task,
            'undo': self.undo_task,
            'print': lambda *args: [self.outputter(task) for task in (self.tasks.values() or ["No tasks"])],
            'quit': lambda x: quit()
        }

    def show_usage(self, *args):
        self.outputter("""Usage:
    Add <text>  - Add a new tasks
    Print       - Show all tasks
    Do #        - Complete a task
    Undo #      - Undo a completed task
    Quit        - Quit the application""")

    def add_task(self, text):
        task = Task(" ".join(text))
        self.tasks[task.id] = task
        self.persister.persist(self.tasks)
        self.outputter(task)

    def do_task(self, numbers):
        for num in numbers:
            task = self.tasks[int(num)]
            self.outputter(f"Completed {task}")
            task.complete()

        self.persister.persist(self.tasks)

    def undo_task(self, numbers):
        for num in numbers:
            task = self.tasks[int(num)]
            task.uncomplete()
            self.outputter(f"Undid task {task}")

        self.persister.persist(self.tasks)

    def run(self):
        while True:
            command = self.inputter("> ")
            if not command:
                self.show_usage()
                continue

            cmd, *args = command.split()

            self.commands.get(cmd.lower(), self.show_usage)(args)


if __name__ == "__main__":
    task_file = Path("tasks.json")
    Application(Persister(task_file), input, print).run()
