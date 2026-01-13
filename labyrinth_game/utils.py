"""Вспомогательные функции игры."""

import math

from labyrinth_game.constants import ROOMS


def pseudo_random(seed: int, modulo: int) -> int:
    """Детерминированный псевдослучайный генератор."""
    if modulo <= 0:
        return 0

    x = math.sin(seed * 12.9898) * 43758.5453
    return int((x - math.floor(x)) * modulo)


def trigger_trap(game_state: dict) -> None:
    """Срабатывание ловушки с негативными последствиями."""
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state.get("player_inventory", [])
    seed = game_state.get("steps", 0)

    if inventory:
        index = pseudo_random(seed, len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы потеряли предмет: {lost_item}!")
        return

    roll = pseudo_random(seed, 10)
    if roll < 3:
        print("Вы не смогли выбраться из ловушки. Игра окончена.")
        game_state["game_over"] = True
    else:
        print("Вам удалось избежать серьёзных последствий.")


def random_event(game_state: dict) -> None:
    """Случайное событие после перемещения."""
    seed = game_state.get("steps", 0)
    current_room = game_state.get("current_room")

    if pseudo_random(seed, 10) != 0:
        return

    event_type = pseudo_random(seed + 1, 3)

    if event_type == 0:
        print("Вы заметили блеск на полу и нашли монетку.")
        ROOMS[current_room].setdefault("items", []).append("coin")

    elif event_type == 1:
        print("В темноте что-то шевельнулось. Вам стало не по себе.")
        if "sword" in game_state.get("player_inventory", []):
            print("Вы крепче сжали меч, и шорохи стихли.")

    elif event_type == 2:
        if current_room == "trap_room" and "torch" not in game_state.get(
            "player_inventory", []
        ):
            print("Слишком темно... вы не заметили опасность!")
            trigger_trap(game_state)


def describe_current_room(game_state: dict) -> None:
    """Выводит описание текущей комнаты."""
    room = ROOMS[game_state["current_room"]]

    print(f"\n== {game_state['current_room'].upper()} ==")
    print(room["description"])

    if room["items"]:
        print("Заметные предметы:")
        for item in room["items"]:
            print(f"- {item}")

    print(f"Выходы: {', '.join(room['exits'].keys())}")

    if room["puzzle"]:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def _normalize_answer(answer: str) -> str:
    """Нормализация ответов игрока."""
    mapping = {
        "десять": "10",
        "10": "10",
    }
    return mapping.get(answer, answer)


def solve_puzzle(game_state: dict) -> None:
    """Решение загадки в текущей комнате."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    inventory = game_state["player_inventory"]

    if not room["puzzle"]:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room["puzzle"]
    correct = correct_answer.lower()

    print(question)

    trap_used = False

    while True:
        user_input = input("Ваш ответ: ").strip().lower()

        # 🔧 ФИКС БАГА: выход из режима solve
        if user_input in ("quit", "exit"):
            print("Вы прерываете решение загадки.")
            return

        user_answer = _normalize_answer(user_input)

        if user_answer == correct:
            print("Вы решили загадку!")

            if room_name == "hall":
                print("Вы почувствовали уверенность в своих знаниях.")
            elif room_name == "library":
                print("Вы узнали древнюю тайну.")
            elif room_name == "trap_room":
                print("Вы сумели избежать опасности.")

            game_state["puzzles_solved"] += 1

            if (
                game_state["puzzles_solved"] == 3
                and "treasure_key" not in inventory
            ):
                inventory.append("treasure_key")
                print("Вы получили ключ от сокровищницы!")

            room["puzzle"] = None
            return
        else:
            print("Неверно.")
            if room_name == "trap_room" and not trap_used:
                trap_used = True
                trigger_trap(game_state)
                if game_state.get("game_over"):
                    return
            else:
                print("Попробуйте снова.")


def attempt_open_treasure(game_state: dict) -> None:
    """Логика открытия сундука и победы."""
    room = ROOMS[game_state["current_room"]]
    inventory = game_state["player_inventory"]

    if "treasure_chest" not in room["items"]:
        print("Здесь нет сундука с сокровищами.")
        return

    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    if not room["puzzle"]:
        print("Сундук заперт, но подсказок для кода нет.")
        return

    question, correct_code = room["puzzle"]
    print(f"Подсказка: {question}")

    if input("Хотите попробовать ввести код? (да/нет): ").strip().lower() != "да":
        print("Вы отступаете от сундука.")
        return

    while True:
        if input("Введите код: ").strip().lower() == correct_code.lower():
            print("Код верный! Замок открывается.")
            room["items"].remove("treasure_chest")
            print("В сундуке сокровище! Вы победили!")
            game_state["game_over"] = True
            return
        else:
            print("Код неверный. Попробуйте снова.")



def show_help(commands: dict) -> None:
    """Показывает список доступных команд."""
    print("\nДоступные команды:")
    for command, description in commands.items():
        print(f"  {command.ljust(16)} {description}")



