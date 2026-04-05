from src.inbox.core import InboxApp
from src.sources.json import JSONTaskSource
from src.sources.stdin import StdinTaskSource


def main():
    app = InboxApp() #Новый пустой экземпляр класса с self.tasks = []
    #Переменная теперь хранит ссылку на созданный объект
    print("Выберите источник:")
    print("1 - JSON файл")
    print("2 - Ввод вручную")

    choice = input("> ")#Ждем ввод пользователя

    if choice == "1":
        source = JSONTaskSource("tasks.jsonl")#Создаёт источник, читающий файл
    elif choice == "2":
        source = StdinTaskSource()#Создаёт источник для ручного ввода
    else:
        print("Неверный выбор")
        return

    app.load_tasks(source)#Загружает задачи в приложение, наполняет self.tasks
    app.show_tasks()