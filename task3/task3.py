import sys
from pathlib import Path


def parse_log_line(line: str) -> dict:
    # Розбиваємо сирий рядок логу на основні складові.
    parts = line.strip().split(maxsplit=3)
    if len(parts) != 4:
        # Якщо структура не відповідає очікуваному формату, повідомляємо про помилку.
        raise ValueError(f"Invalid log line format: {line.strip()}")

    date, time, level, message = parts
    # Повертаємо розібраний запис у зручному для подальшої обробки вигляді.
    return {"date": date, "time": time, "level": level.upper(), "message": message}


def load_logs(file_path: str) -> list:
    # У цей список збираємо всі коректно розібрані записи з файлу.
    logs = []

    try:
        # Відкриваємо файл логів у текстовому режимі з UTF-8 кодуванням.
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                # Пропускаємо порожні рядки у файлі логів.
                if not line.strip():
                    continue

                try:
                    # Додаємо до списку тільки ті рядки, які вдалося коректно розібрати.
                    logs.append(parse_log_line(line))
                except ValueError:
                    # Ігноруємо рядки з некоректним форматом.
                    continue
    except FileNotFoundError:
        # Окремо обробляємо ситуацію, коли вказаний файл не існує.
        print(f"File not found: {file_path}")
        return []
    except OSError as error:
        # Обробляємо інші помилки читання файлу.
        print(f"Error reading file '{file_path}': {error}")
        return []

    # Повертаємо всі завантажені та валідні записи.
    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    # Нормалізуємо рівень, щоб пошук не залежав від регістру введення.
    normalized_level = level.upper()
    # Відбираємо лише ті записи, що відповідають потрібному рівню логування.
    return list(filter(lambda log: log["level"] == normalized_level, logs))


def count_logs_by_level(logs: list) -> dict:
    # Зберігаємо базові рівні логування у фіксованому порядку для виводу.
    counts = {"INFO": 0, "DEBUG": 0, "ERROR": 0, "WARNING": 0}

    for log in logs:
        # Для кожного запису збільшуємо лічильник відповідного рівня.
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1

    # Повертаємо словник із підрахованою статистикою.
    return counts


def display_log_counts(counts: dict) -> None:
    # Виводимо заголовок простої текстової таблиці.
    print("Рівень логування | Кількість")
    print("-----------------|----------")

    for level, count in counts.items():
        # Форматуємо кожен рядок таблиці з вирівнюванням по ширині.
        print(f"{level:<16} | {count}")


def main() -> None:
    # Якщо аргументів немає, використовуємо файл logs.txt поруч зі скриптом.
    default_log_path = Path(__file__).with_name("logs.txt")

    # Підтримуємо два режими запуску:
    # 1) python task3.py
    # 2) python task3.py logs.txt [error]
    # 3) python task3.py error
    if len(sys.argv) == 1:
        file_path = str(default_log_path)
        log_level = None
    elif len(sys.argv) == 2:
        argument = sys.argv[1]

        # Якщо передано відомий рівень логування, використовуємо типовий logs.txt.
        if argument.upper() in {"INFO", "DEBUG", "ERROR", "WARNING"}:
            file_path = str(default_log_path)
            log_level = argument
        else:
            file_path = argument
            log_level = None
    else:
        # Якщо передано два аргументи, перший вважаємо шляхом, другий рівнем логування.
        file_path = sys.argv[1]
        log_level = sys.argv[2]

    # Завантажуємо записи з логу.
    logs = load_logs(file_path)
    if not logs:
        # Якщо файл не вдалося прочитати або записи відсутні, завершуємо роботу.
        return

    # Підраховуємо кількість записів за кожним рівнем і виводимо статистику.
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if log_level:
        # Додатково виводимо всі повідомлення вибраного рівня.
        filtered_logs = filter_logs_by_level(logs, log_level)
        print(f"\nДеталі логів для рівня '{log_level.upper()}':")

        for log in filtered_logs:
            # Для кожного відфільтрованого запису показуємо дату, час і текст повідомлення.
            print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    # Запускаємо CLI-логіку лише при прямому виконанні файлу.
    main()
