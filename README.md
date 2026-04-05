## Лабораторная работа №2: Модель задачи: дескрипторы и @property

## Цель работы
Освоить управление доступом к атрибутам и защиту 
инвариантов доменной модели с 
использованием дескрипторов и property.
## Структура проекта
<pre>
lab1/
├── src/                               # Исходный код
│   ├── cli/                           # Модуль командной строки
│   │   ├── __init__.py
│   │   └── cli.py                     # CLI интерфейс
│   ├── contracts/                      # Контракты и протоколы
│   │   ├── __init__.py
│   │   ├── task_source.py              # Протокол TaskSource
│   │   └── tasks.py                    # Модель Task
│   ├── inbox/                          # Ядро приложения
│   │   ├── __init__.py
│   │   └── core.py                      # InboxApp
│   ├── sources/                         # Источники задач
│   │   ├── __init__.py
│   │   ├── json.py                       # JSONL источник
│   │   ├── repository.py                 # Реестр источников
│   │   └── stdin.py                      # STDIN источник
│   ├── __init__.py
│   ├── __main__.py                       # Точка входа
│   └── constants.py                       # Константы
├── tests/                                 # Unit тесты
│   └── test.py                            # Тесты
├── tasks.jsonl                            # Пример данных
├── .gitignore                              # git ignore файл
├── .pre-commit-config.yaml                  # Настройки pre-commit
├── README.md                                # Описание проекта
├── report.pdf                               # Отчет (пустой, для вставки)
├── pyproject.toml                           # Зависимости проекта
└── uv.lock                                  # Фиксация зависимостей
</pre>


### Реализованные требования

#### 1. Дескрипторы для валидации
- **PositiveInt** — data descriptor для положительных целых чисел (id, priority)
- **StatusDescriptor** — data descriptor для валидации статуса задачи

#### 2. Property для вычисляемых свойств
- **created_at** — property только для чтения (время создания)
- **is_ready** — вычисляемое свойство (готовность к выполнению)

#### 3. Защита инвариантов
- ID всегда положительный (>0)
- Приоритет всегда положительный (>0)
- Статус только из {new, in_progress, done}
- created_at неизменяем после создания

#### 4. Чистый публичный API
Пользователь имеет доступ только к:
- `id`, `priority`, `status`, `description` 
- `created_at`, `is_ready` — только чтение


### В рамках работы реализованы:

- Протокол источника задач с runtime-проверкой

- Два типа источников: файловый (JSONL) и потоковый (STDIN)

- Реестр источников для расширения функциональности без изменения существующего кода

- CLI интерфейс для взаимодействия с системой

### Основной функционал
1. Контракты и протоколы (src/contracts/)
2. Источники задач (src/sources/)
3. Ядро приложения (src/inbox/core.py)
4. CLI интерфейс (src/cli/cli.py)
### Структура модулей
- src/constants.py
- src/__main__.py
- tests/test.py
### Установка и запуск
#### Требования
Python 3.11 или выше
Библиотеки: typer, pytest, pytest-cov (для тестов)
в терминале запускаем
python
>>> from src.contracts.tasks import Task
>>> task = Task(id=1, description="Тест", priority=5, status="new")
>>> task.is_ready
True
>>> task.status = "in_progress"
>>> task.is_ready
False