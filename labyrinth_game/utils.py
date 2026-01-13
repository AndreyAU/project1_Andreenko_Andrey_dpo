"""Вспомогательные функции игры."""

from labyrinth_game.constants import ROOMS


def describe_current_room(game_state: dict) -> None:
    """Выводит описание текущей комнаты."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room["description"])

    if room["items"]:
        print("Заметные предметы:")
        for item in room["items"]:
            print(f"- {item}")

    exits = ", ".join(room["exits"].keys())
    print(f"Выходы: {exits}")

    if room["puzzle"]:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state: dict) -> None:
    """Решение загадки в текущей комнате."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    inventory = game_state["player_inventory"]

    if not room["puzzle"]:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room["puzzle"]
    correct_answer = correct_answer.lower()

    print(question)

    while True:
        user_answer = input("Ваш ответ: ").strip().lower()

        if user_answer == correct_answer:
            print("Вы решили загадку!")
            print("Вы получили награду за решение загадки.")

            # увеличиваем счётчик решённых загадок
            game_state["puzzles_solved"] += 1

            # если решены все загадки — выдаём ключ
            if (
                game_state["puzzles_solved"] == 3
                and "treasure_key" not in inventory
            ):
                inventory.append("treasure_key")
                print("Вы получили ключ от сокровищницы!")

            # убираем загадку
            room["puzzle"] = None
            break
        else:
            print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state: dict) -> None:
    """Логика открытия сундука и победы."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    inventory = game_state["player_inventory"]

    if "treasure_chest" not in room["items"]:
        print("Здесь нет сундука с сокровищами.")
        return

    # основной путь — через ключ
    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    # альтернативный путь — через код
    if not room["puzzle"]:
        print("Сундук заперт, но подсказок для кода нет.")
        return

    question, correct_code = room["puzzle"]
    correct_code = correct_code.lower()

    print(f"Подсказка: {question}")

    choice = input("Хотите попробовать ввести код? (да/нет): ").strip().lower()

    if choice != "да":
        print("Вы отступаете от сундука.")
        return

    while True:
        user_code = input("Введите код: ").strip().lower()

        if user_code == correct_code:
            print("Код верный! Замок открывается.")
            room["items"].remove("treasure_chest")
            print("В сундуке сокровище! Вы победили!")
            game_state["game_over"] = True
            break
        else:
            print("Код неверный. Попробуйте снова.")


def show_help() -> None:
    """Показывает список доступных команд."""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - решить загадку или открыть сундук")
    print("  help            - показать это сообщение")
    print("  quit            - выйти из игры")

