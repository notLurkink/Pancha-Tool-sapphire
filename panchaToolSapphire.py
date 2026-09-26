import re
import time
import sys
import os
import random
import requests

BOLD = "\033[1m"
RESET = "\033[0m"

COLOR_LEFT = (0, 50, 150)
COLOR_RIGHT = (0, 191, 255)

current_lang = "ru"

TEXTS = {
    "ru": {
        "logo": [
            "┏━┓┏━┓┏┓╻┏━╸╻ ╻┏━┓   ╺┳╸┏━┓┏━┓╻  ",
            "┣━┛┣━┫┃┗┫┃  ┣━┫┣━┫    ┃ ┃ ┃┃ ┃┃  ",
            "╹  ╹ ╹╹ ╹┗━╸╹ ╹╹ ╹    ╹ ┗━┛┗━┛┗━╸",
            "      ┏━┓┏━┓┏━┓┏━┓╻ ╻╻┏━┓┏━╸     ",
            "      ┗━┓┣━┫┣━┛┣━┛┣━┫┃┣┳┛┣╸      ",
            "      ┗━┛╹ ╹╹  ╹  ╹ ╹╹╹┗╸┗━╸     "
        ],
        "menu_items": [
            "1) панча намбер сеарч",
            "2) панча юсернейм сеарч",
            "3) снос",
            "4) флуд",
            "5) ддос",
            "6) автор",
            "0) настройки"
        ],
        "prompt": "> ",
        "invalid": "Неверный выбор. Попробуйте еще раз.",
        "exit_program": "Выход из программы...",
        "settings_title": "НАСТРОЙКИ",
        "settings_lang": "1) Язык (текущий: {})",
        "settings_exit": "2) Выход из программы",
        "settings_back": "3) Вернуться",
        "lang_choice": "Выберите язык: 1) Русский  2) English",
        "lang_changed": "Язык изменён на {}",
        "back": "Вернуться",
        "search_number_prompt": "Введите номер телефона в формате +7 XXX XXX XXXX:",
        "search_number_invalid": "Нету нечего.",
        "search_number_valid": ["Ф-эболов", "И-рекюлиб", "О-визивеч", "Адрс-хз", "Соцсети-хз"],
        "search_username_prompt": "Введите юзернейм:",
        "search_username_not_found": "Юзернейм не найден.",
        "delete_user_prompt": "Введите юзернейм:",
        "delete_user_id_prompt": "Введите айди:",
        "delete_user_error_username": "Ошибка: некорректный юзернейм. Должен начинаться с латинской буквы (можно с @).",
        "delete_user_error_id": "Ошибка: айди должен содержать только цифры, дефис или подчеркивание.",
        "delete_loading": "Загрузка...",
        "delete_success": "Успешно снесено.",
        "delete_channel_user_prompt": "введите юзер канала",
        "delete_channel_id_prompt": "введите айди канал",
        "delete_channel_find": "находим говно",
        "delete_channel_fuck": "ебем говно!",
        "delete_channel_destroyed": "Канал уничтожен.",
        "delete_bob_user_prompt": "введите юзер боба",
        "delete_bob_error": "Ошибка: это не похоже на боба (должно содержать 'bob' или '_bob').",
        "delete_bob_find": "находим боба",
        "delete_bob_eat": "едим боб",
        "delete_bob_destroyed": "Боб уничтожен.",
        "delete_type_choice": "Выберите тип для сноса:",
        "delete_type_user": "1) юзер",
        "delete_type_channel": "2) канал",
        "delete_type_bob": "3) боб",
        "delete_type_back": "4) вернуться",
        "flood_type_choice": "Выберите тип флуда:",
        "flood_type_telegram": "1) телехрям",
        "flood_type_phone": "2) на номер",
        "flood_type_back": "3) вернуться",
        "flood_telegram_prompt": "Введите номер телехрям аккаунта:",
        "flood_telegram_success": "Флуд телехрям запущен.",
        "flood_phone_prompt": "Введите номер:",
        "flood_phone_success": "Флуд на номер успешно отправлен.",
        "author_info": ["Создатель софта: @lurkink", "Канал софта: @scary_komaru / bank_cocoa"],
        "press_any_key": "Нажмите любую клавишу для продолжения...",
        "ddos_url_prompt": "Введите URL web site (с http:// или https://):",
        "ddos_checking": "Проверка доступности сервиса...",
        "ddos_unavailable": "Ошибка: сервис недоступен (HTTP {}). Попробуйте позже.",
        "ddos_no_internet": "Нет доступа к интернету. Попробуйте позже.",
        "ddos_timeout": "Таймаут соединения. Сервер не отвечает.",
        "ddos_error": "Ошибка при проверке: {}",
        "ddos_available": "Сервис доступен. Атака началась",
        "ddos_success": "успешно",
        "ddos_fail": "не успешно"
    },
    "en": {
        "logo": [
            "┏━┓┏━┓┏┓╻┏━╸╻ ╻┏━┓   ╺┳╸┏━┓┏━┓╻  ",
            "┣━┛┣━┫┃┗┫┃  ┣━┫┣━┫    ┃ ┃ ┃┃ ┃┃  ",
            "╹  ╹ ╹╹ ╹┗━╸╹ ╹╹ ╹    ╹ ┗━┛┗━┛┗━╸",
            "      ┏━┓┏━┓┏━┓┏━┓╻ ╻╻┏━┓┏━╸     ",
            "      ┗━┓┣━┫┣━┛┣━┛┣━┫┃┣┳┛┣╸      ",
            "      ┗━┛╹ ╹╹  ╹  ╹ ╹╹╹┗╸┗━╸     "
        ],
        "menu_items": [
            "1) punch number search",
            "2) punch username search",
            "3) delete",
            "4) flood",
            "5) ddos",
            "6) author",
            "0) settings"
        ],
        "prompt": "> ",
        "invalid": "Invalid choice. Try again.",
        "exit_program": "Exiting program...",
        "settings_title": "SETTINGS",
        "settings_lang": "1) Language (current: {})",
        "settings_exit": "2) Exit program",
        "settings_back": "3) Back",
        "lang_choice": "Select language: 1) Russian  2) English",
        "lang_changed": "Language changed to {}",
        "back": "Back",
        "search_number_prompt": "Enter phone number in format +7 XXX XXX XXXX:",
        "search_number_invalid": "Nothing found.",
        "search_number_valid": ["F-ebolov", "I-rekyulib", "O-vizivech", "Addr-unknown", "Socials-unknown"],
        "search_username_prompt": "Enter username:",
        "search_username_not_found": "Username not found.",
        "delete_user_prompt": "Enter username:",
        "delete_user_id_prompt": "Enter id:",
        "delete_user_error_username": "Error: invalid username. Must start with a Latin letter (may start with @).",
        "delete_user_error_id": "Error: id must contain only digits, dash or underscore.",
        "delete_loading": "Loading...",
        "delete_success": "Successfully deleted.",
        "delete_channel_user_prompt": "enter channel username",
        "delete_channel_id_prompt": "enter channel id",
        "delete_channel_find": "finding shit",
        "delete_channel_fuck": "fucking shit!",
        "delete_channel_destroyed": "Channel destroyed.",
        "delete_bob_user_prompt": "enter bob username",
        "delete_bob_error": "Error: doesn't look like a bob (must contain 'bob' or '_bob').",
        "delete_bob_find": "finding bob",
        "delete_bob_eat": "eating bob",
        "delete_bob_destroyed": "Bob destroyed.",
        "delete_type_choice": "Select type to delete:",
        "delete_type_user": "1) user",
        "delete_type_channel": "2) channel",
        "delete_type_bob": "3) bob",
        "delete_type_back": "4) back",
        "flood_type_choice": "Select flood type:",
        "flood_type_telegram": "1) telegram",
        "flood_type_phone": "2) phone number",
        "flood_type_back": "3) back",
        "flood_telegram_prompt": "Enter telegram account number:",
        "flood_telegram_success": "Telegram flood started.",
        "flood_phone_prompt": "Enter phone number:",
        "flood_phone_success": "Phone number flood successfully sent.",
        "author_info": ["Software creator: @lurkink", "Software channel: @scary_komaru / bank_cocoa"],
        "press_any_key": "Press any key to continue...",
        "ddos_url_prompt": "Enter web site URL (with http:// or https://):",
        "ddos_checking": "Checking service availability...",
        "ddos_unavailable": "Error: service unavailable (HTTP {}). Try later.",
        "ddos_no_internet": "No internet access. Try later.",
        "ddos_timeout": "Connection timeout. Server not responding.",
        "ddos_error": "Error during check: {}",
        "ddos_available": "Service available. Attack started",
        "ddos_success": "successful",
        "ddos_fail": "unsuccessful"
    }
}

def _(key, *args):
    text = TEXTS[current_lang].get(key, key)
    if args:
        return text.format(*args)
    return text

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def gradient_color_for_pos(pos, length):
    if length <= 1:
        ratio = 0
    else:
        ratio = 1 - (pos / (length - 1))
    r = int(COLOR_RIGHT[0] + (COLOR_LEFT[0] - COLOR_RIGHT[0]) * ratio)
    g = int(COLOR_RIGHT[1] + (COLOR_LEFT[1] - COLOR_RIGHT[1]) * ratio)
    b = int(COLOR_RIGHT[2] + (COLOR_LEFT[2] - COLOR_RIGHT[2]) * ratio)
    return f"\033[1m\033[38;2;{r};{g};{b}m"

def print_colored_line(line, padding_spaces=0):
    if padding_spaces:
        sys.stdout.write(" " * padding_spaces)
    length = len(line)
    for i, ch in enumerate(line):
        color = gradient_color_for_pos(i, length)
        sys.stdout.write(color + ch)
    sys.stdout.write(RESET + "\n")
    sys.stdout.flush()

def center_print(line):
    term_width = get_terminal_width()
    padding = (term_width - len(line)) // 2
    if padding < 0:
        padding = 0
    print_colored_line(line, padding)

def gradient_input(prompt):
    term_width = get_terminal_width()
    box_width = 40
    left_padding = (term_width - box_width) // 2
    if left_padding < 0:
        left_padding = 0
    sys.stdout.write(" " * left_padding)
    for i, ch in enumerate(prompt):
        color = gradient_color_for_pos(i, len(prompt))
        sys.stdout.write(color + ch)
    sys.stdout.write(RESET)
    sys.stdout.flush()
    input_color = f"\033[1m\033[38;2;{COLOR_RIGHT[0]};{COLOR_RIGHT[1]};{COLOR_RIGHT[2]}m"
    sys.stdout.write(input_color)
    result = input()
    sys.stdout.write(RESET)
    return result.strip()

def validate_username(username, allow_at=True):
    if allow_at and username.startswith('@'):
        username = username[1:]
    if not username:
        return False
    if not re.match(r'^[A-Za-z]', username):
        return False
    if not re.match(r'^[A-Za-z][A-Za-z0-9_]*$', username):
        return False
    return True

def validate_id(id_str):
    return re.match(r'^[\d\-_]+$', id_str) is not None

user_data = {
    "@reqlib": {
        "номер": "Номер-ненайдено",
        "дата регистрации": "15 октября 2024 год",
        "айди": "6649538880"
    },
    "@pythondevoleper": {
        "номер": "Номер-ненайдено",
        "дата регистрации": "14 апреля 2024 год",
        "айди": "7150261279"
    }
}

def main_menu():
    clear_screen()
    for line in _("logo"):
        center_print(line)
    for item in _("menu_items"):
        center_print(item)
    print()

def search_by_number():
    center_print(_("search_number_prompt"))
    number = gradient_input(_("prompt"))
    if not re.match(r'^\+7 \d{3} \d{3} \d{4}$', number):
        center_print(_("search_number_invalid"))
        return
    valid_numbers = ["+7 999 635 8210", "+7 999 635 1234"]
    if number in valid_numbers:
        for msg in _("search_number_valid"):
            center_print(msg)
    else:
        center_print(_("search_number_invalid"))
    time.sleep(2)

def search_by_username():
    center_print(_("search_username_prompt"))
    username = gradient_input(_("prompt"))
    if username in user_data:
        info = user_data[username]
        center_print(f"Номер: {info['номер']}")
        center_print(f"Дата регистрации: {info['дата регистрации']}")
        center_print(f"Айди: {info['айди']}")
    else:
        center_print(_("search_username_not_found"))
    time.sleep(2)

def delete_user():
    center_print(_("delete_user_prompt"))
    username = gradient_input(_("prompt"))
    if not validate_username(username, allow_at=True):
        center_print(_("delete_user_error_username"))
        time.sleep(2)
        return
    center_print(_("delete_user_id_prompt"))
    user_id = gradient_input(_("prompt"))
    if not validate_id(user_id):
        center_print(_("delete_user_error_id"))
        time.sleep(2)
        return
    center_print(_("delete_loading"))
    for percent in range(0, 101, 5):
        sys.stdout.write("\r" + " " * get_terminal_width())
        center_print(f"{percent}%")
        time.sleep(1)
    center_print(_("delete_success"))
    time.sleep(2)

def delete_channel():
    center_print(_("delete_channel_user_prompt"))
    username = gradient_input(_("prompt"))
    if not validate_username(username, allow_at=True):
        center_print(_("delete_user_error_username"))
        time.sleep(2)
        return
    center_print(_("delete_channel_id_prompt"))
    channel_id = gradient_input(_("prompt"))
    if not validate_id(channel_id):
        center_print(_("delete_user_error_id"))
        time.sleep(2)
        return
    center_print(_("delete_channel_find"))
    time.sleep(1)
    center_print(_("delete_channel_fuck"))
    time.sleep(1)
    center_print(_("delete_loading"))
    for percent in range(0, 101, 5):
        sys.stdout.write("\r" + " " * get_terminal_width())
        center_print(f"{percent}%")
        time.sleep(0.6)
    center_print(_("delete_channel_destroyed"))
    time.sleep(2)

def delete_bob():
    center_print(_("delete_bob_user_prompt"))
    bob_username = gradient_input(_("prompt"))
    lower_name = bob_username.lower()
    if "bob" not in lower_name and "_bob" not in lower_name:
        center_print(_("delete_bob_error"))
        time.sleep(2)
        return
    center_print(_("delete_bob_find"))
    time.sleep(1)
    center_print(_("delete_bob_eat"))
    time.sleep(1)
    center_print(_("delete_loading"))
    for percent in range(0, 101, 5):
        sys.stdout.write("\r" + " " * get_terminal_width())
        center_print(f"{percent}%")
        time.sleep(0.25)
    center_print(_("delete_bob_destroyed"))
    time.sleep(2)

def delete_submenu():
    while True:
        clear_screen()
        center_print(_("delete_type_choice"))
        center_print(_("delete_type_user"))
        center_print(_("delete_type_channel"))
        center_print(_("delete_type_bob"))
        center_print(_("delete_type_back"))
        choice = gradient_input(_("prompt"))
        if choice == "1":
            delete_user()
            break
        elif choice == "2":
            delete_channel()
            break
        elif choice == "3":
            delete_bob()
            break
        elif choice == "4":
            break
        else:
            center_print(_("invalid"))
            time.sleep(1)

def flood_telegram():
    center_print(_("flood_telegram_prompt"))
    number = gradient_input(_("prompt"))
    center_print(_("flood_telegram_success"))
    time.sleep(2)

def flood_phone():
    center_print(_("flood_phone_prompt"))
    number = gradient_input(_("prompt"))
    center_print(_("flood_phone_success"))
    time.sleep(2)

def flood_submenu():
    while True:
        clear_screen()
        center_print(_("flood_type_choice"))
        center_print(_("flood_type_telegram"))
        center_print(_("flood_type_phone"))
        center_print(_("flood_type_back"))
        choice = gradient_input(_("prompt"))
        if choice == "1":
            flood_telegram()
            break
        elif choice == "2":
            flood_phone()
            break
        elif choice == "3":
            break
        else:
            center_print(_("invalid"))
            time.sleep(1)

def author_info():
    for line in _("author_info"):
        center_print(line)
    center_print(_("press_any_key"))
    input()

def ddos_attack():
    center_print(_("ddos_url_prompt"))
    url = gradient_input(_("prompt"))

    center_print(_("ddos_checking"))
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        if response.status_code != 200:
            center_print(_("ddos_unavailable", response.status_code))
            time.sleep(3)
            return
    except requests.exceptions.ConnectionError:
        center_print(_("ddos_no_internet"))
        time.sleep(3)
        return
    except requests.exceptions.Timeout:
        center_print(_("ddos_timeout"))
        time.sleep(3)
        return
    except Exception as e:
        center_print(_("ddos_error", str(e)))
        time.sleep(3)
        return

    center_print(_("ddos_available"))
    time.sleep(1)

    count_200 = random.randint(4, 34)
    for _ in range(count_200):
        center_print("200")
        time.sleep(0.1)

    if random.random() < 0.1:
        final_code = "200"
        result_text = _("ddos_fail")
    else:
        final_code = random.choice(["502", "504"])
        result_text = _("ddos_success")

    center_print(final_code)
    center_print(result_text)
    time.sleep(2)

def settings_menu():
    global current_lang
    while True:
        clear_screen()
        center_print(_("settings_title"))
        lang_name = "Русский" if current_lang == "ru" else "English"
        center_print(_("settings_lang", lang_name))
        center_print(_("settings_exit"))
        center_print(_("settings_back"))
        choice = gradient_input(_("prompt"))
        if choice == "1":
            clear_screen()
            center_print(_("lang_choice"))
            lang_choice = gradient_input(_("prompt"))
            if lang_choice == "1":
                current_lang = "ru"
                center_print(_("lang_changed", "Русский"))
            elif lang_choice == "2":
                current_lang = "en"
                center_print(_("lang_changed", "English"))
            else:
                center_print(_("invalid"))
            time.sleep(1.5)
        elif choice == "2":
            center_print(_("exit_program"))
            sys.exit(0)
        elif choice == "3":
            break
        else:
            center_print(_("invalid"))
            time.sleep(1)

def main():
    while True:
        main_menu()
        choice = gradient_input(_("prompt"))
        if choice == "1":
            search_by_number()
        elif choice == "2":
            search_by_username()
        elif choice == "3":
            delete_submenu()
        elif choice == "4":
            flood_submenu()
        elif choice == "5":
            ddos_attack()
        elif choice == "6":
            author_info()
        elif choice == "0":
            settings_menu()
        else:
            center_print(_("invalid"))
            time.sleep(1)

if __name__ == "__main__":
    main()