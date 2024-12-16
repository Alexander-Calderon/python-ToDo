
import config.settings
from app.task.task_view import TaskManagerApp


def main():
    app = TaskManagerApp()
    app.run()


if __name__ == "__main__":
    main()


