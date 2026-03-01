
USAGE = (                              # текст з інструкцією для користувача які є команди
    "Commands:\n"
    "  hello\n"
    "  add <name> <phone>\n"
    "  change <name> <new_phone>\n"
    "  phone <name>\n"
    "  all\n"
    "  close | exit\n"
)


def input_error(func):  # декоратор для обробки типових помилок введення користувача
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            # Помилка виникає, коли для команди не вистачає імені або номера телефону.
            return "Give me name and phone please."
        except KeyError:
            # Повертаємо повідомлення, якщо контакт не знайдено у словнику.
            return "Contact not found."
        except IndexError:
            # Помилка виникає, коли команда очікує ім'я, але користувач його не ввів.
            return "Enter user name."
       
            # !Додав ексепшн для обробки будь-яких інших непередбачених помилок, щоб бот не падав і повертав зрозуміле повідомлення.
        except Exception as e:           
            return f"An unexpected error occurred: {e}"

    return inner


def parse_input(user_input: str) -> tuple[str, list[str]]: # робимо функцію яка буде парсити введену користувачем команду і її аргументи, повертаючи їх у вигляді кортежу (команда, список аргументів)
    
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args


@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str: # функція яка додає контакт до словника, приймаючи список аргументів і словник контактів, повертаючи рядок з результатом операції
    # Очікуємо рівно два аргументи: ім'я та номер; інакше виникне ValueError.
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str: # функція яка змінює номер телефону існуючого контакту, приймаючи список аргументів і словник контактів, повертаючи рядок з результатом операції
    # Очікуємо ім'я контакту і новий номер телефону.
    name, new_phone = args
    if name not in contacts:
        # Явно викликаємо KeyError, щоб декоратор повернув зрозуміле повідомлення.
        raise KeyError
    contacts[name] = new_phone
    return "Contact updated."


@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str: # функція яка показує номер телефону для заданого контакту, приймаючи список аргументів і словник контактів, повертаючи рядок з результатом операції
    # Беремо перший аргумент як ім'я; якщо його немає, виникне IndexError.
    name = args[0]
    # Якщо контакту з таким ім'ям немає, звернення до словника викличе KeyError.
    return contacts[name]


@input_error
def show_all(contacts: dict[str, str]) -> str: # функція яка показує всі контакти і їх номери телефону, приймаючи словник контактів, повертаючи рядок з результатом операції
    if not contacts:
        return "No contacts saved."
    # Виводимо у відсортованому вигляді для зручності
    lines = [f"{name}: {phone}" for name, phone in sorted(contacts.items(), key=lambda x: x[0].lower())]
    return "\n".join(lines)


def main() -> None: # головна функція яка запускає бота, ініціалізуючи словник контактів і обробляючи введені користувачем команди у циклі, викликаючи відповідні функції для кожної команди і виводячи результат
    contacts: dict[str, str] = {}

    print("Welcome to the assistant bot!")
    print(USAGE)

    #! Створюємо словник для швидкого вибору функції на основі команди, щоб уникнути довгого ланцюга if-elif.
    commands = { 
        "add": lambda args: add_contact(args, contacts),
        "change": lambda args: change_contact(args, contacts),
        "phone": lambda args: show_phone(args, contacts),
        "all": lambda args: show_all(contacts),
    }

    
    while True: # нескінченний цикл для обробки команд користувача
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command in commands:
            print(commands[command](args))
        
        else:
            print("Invalid command.")


if __name__ == "__main__": # запускаємо головну функцію, якщо цей файл виконується як основний
       main()



