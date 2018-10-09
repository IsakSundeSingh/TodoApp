from task import Task
from persister import DiskPersister
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
        self.tasks = self.persister.load()
        self.commands = {
            'add': self.add_task,
            'do': self.do_task,
            'undo': self.undo_task,
            'print': lambda *args: [self.outputter(str(task)) for task in (self.tasks.values() or ["No tasks"])],
            'quit': lambda x: self.quit()
        }
        self.done = False

    def quit(self):
        self.done = True

    def show_usage(self, *args):
        self.outputter("""Usage:
    Add <text>  - Add a new tasks
    Print       - Show all tasks
    Do #        - Complete a task
    Undo #      - Undo a completed task
    Quit        - Quit the application""")

    def add_task(self, text):
        if not text:
            self.outputter("Cannot add empty task")
            return

        task = Task(" ".join(text))
        self.tasks[task.id] = task
        self.persister.store(self.tasks)
        self.outputter(str(task))

    def do_task(self, numbers):
        if not all(x.strip('#').isdigit() for x in numbers):
            self.outputter("Value must be a number")
            return

        for num in numbers:
            task = self.tasks[int(num.strip('#'))]
            self.outputter(f"Completed {task}")
            task.complete()

        self.persister.store(self.tasks)

    def undo_task(self, numbers):
        if not all(x.strip('#').isdigit() for x in numbers):
            self.outputter("Value must be a number")
            return

        for num in numbers:
            task = self.tasks[int(num.strip('#'))]
            task.uncomplete()
            self.outputter(f"Undid {task}")

        self.persister.store(self.tasks)

    def run(self):
        while not self.done:
            command = self.inputter("> ")
            if not command:
                self.show_usage()
                continue

            cmd, *args = command.split()

            self.commands.get(cmd.lower(), self.show_usage)(args)


if __name__ == "__main__":
    task_file = Path("tasks.json")
    Application(DiskPersister(task_file), input, print).run()
