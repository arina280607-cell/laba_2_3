from src.inbox.core import InboxApp
from src.sources.json import JSONTaskSource
from src.sources.stdin import StdinTaskSource
from src.inbox.queue import TaskQueue


def main():
    app = InboxApp()

    # позволяет объединять источники
    while True:
        print("\n--- Загрузка задач ---")
        print("1 - Добавить задачи из JSON")
        print("2 - Добавить задачи вручную (Stdin)")
        print("3 - Завершить загрузку и перейти к меню")

        load_choice = input("> ")

        if load_choice == "1":
            # задачи из файла добавятся в общий список app.tasks
            source = JSONTaskSource("tasks.jsonl")
            app.load_tasks(source)
            print("Задачи из файла добавлены в общую базу.")

        elif load_choice == "2":
            # задачи из консоли тоже добавятся в тот же список app.tasks
            source = StdinTaskSource()
            app.load_tasks(source)

        elif load_choice == "3":
            if not app.tasks:
                print("Сначала добавьте хотя бы одну задачу!")
                continue
            break
        else:
            print("Неверный выбор.")

    # 2. создаем одну очередь из всех накопленных задач
    queue = TaskQueue(app.tasks)

    # 3. основной цикл работы с объединенными данными
    while True:
        print(f"\n=== МЕНЮ (Всего задач в памяти: {len(queue)}) ===")
        print("1 - Показать всё (общий список)")
        print("2 - Фильтр: Только новые")
        print("3 - Фильтр: Приоритет (ввод числа)")
        print("0 - Выход")

        user_choice = input("> ")

        if user_choice == "1":
            for task in queue:
                print(task)

        elif user_choice == "2":
            for task in queue.filter_by_status("new"):
                print(task)

        elif user_choice == "3":
            try:
                p_level = int(input("Минимальный приоритет: "))
                for task in queue.filter_by_priority(p_level):
                    print(task)
            except ValueError:
                print("Ошибка: введите число!")

        elif user_choice == "0":
            break


if __name__ == "__main__":
    main()