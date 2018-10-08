from task import Task, count_from
from json import dump, load
from pathlib import Path

# If imported input implicitly uses it and provides features from it
# such as history
try:
    import readline
except ModuleNotFoundError:
    pass


def show_usage(*args):
    print("""Usage:
    Add <text>  - Add a new tasks
    Print       - Show all tasks
    Do #        - Complete a task
    Undo #      - Undo a completed task
    Quit        - Quit the application
    """)


task_file = Path("tasks.json")


def init_tasks():
    if not task_file.exists():
        return dict()

    with open(task_file, "r") as f:
        data = load(f)
        # Ensure new tasks get a unique id
        highest_id = max(data, key=lambda x: x["id"])["id"]
        Task.id_generator = count_from(highest_id + 1)

        return {task["id"]: Task.from_dict(task) for task in data}


tasks = init_tasks()


def persist():
    """Persists all tasks to a file"""

    with open(task_file, "w") as f:
        all_tasks = [task.to_dict() for task in tasks.values()]

        dump(all_tasks, f)


def add_task(text):
    task = Task(" ".join(text))
    tasks[task.id] = task
    persist()
    print(task)


def do_task(numbers):
    for num in numbers:
        task = tasks[int(num)]
        task.complete()
        print(f"Completed {task}")

    persist()


def undo_task(numbers):
    for num in numbers:
        task = tasks[int(num)]
        task.uncomplete()
        print(f"Undid task {task}")

    persist()


commands = {
    'add': add_task,
    'do': do_task,
    'undo': undo_task,
    'print': lambda *args: [print(task) for task in (tasks.values() or ["No tasks"])],
    'quit': lambda x: quit()
}


while True:
    command = input("> ")
    if not command:
        show_usage()
        continue

    cmd, *args = command.split()

    commands.get(cmd.lower(), show_usage)(args)
