from src.inbox.core import InboxApp
from src.sources.json import JSONTaskSource
from src.sources.stdin import StdinTaskSource


def main():
    app = InboxApp()

    print("Выберите источник:")
    print("1 - JSON файл")
    print("2 - Ввод вручную")

    choice = input("> ")

    if choice == "1":
        source = JSONTaskSource("tasks.jsonl")
    elif choice == "2":
        source = StdinTaskSource()
    else:
        print("Неверный выбор")
        return

    app.load_tasks(source)
    app.show_tasks()