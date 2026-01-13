"""Действия игрока."""

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room


def show_inventory(game_state: dict) -> None:
    """Показывает инвентарь игрока."""
    inventory = game_state["player_inventory"]

    if not inventory:
        print("Инвентарь пуст.")
        return

    print("Ваш инвентарь:")
    for item in inventory:
        print(f"- {item}")


def get_input(prompt: str = "> ") -> str:
    """Безопасно получает ввод от пользователя."""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state: dict, direction: str) -> None:
    """Перемещает игрока в указанном направлении."""
    current_room = game_state["current_room"]
    exits = ROOMS[current_room]["exits"]

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    new_room = exits[direction]
    game_state["current_room"] = new_room
    game_state["steps_taken"] += 1

    describe_current_room(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    """Позволяет игроку взять предмет из комнаты."""
    current_room = game_state["current_room"]
    room_items = ROOMS[current_room]["items"]

    if item_name in room_items:
        game_state["player_inventory"].append(item_name)
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state: dict, item_name: str) -> None:
    """Использует предмет из инвентаря игрока."""
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Вы зажигаете факел. Вокруг становится светлее.")
        return

    if item_name == "sword":
        print("Вы крепко сжимаете меч. Вы чувствуете уверенность.")
        return

    if item_name == "bronze_box":
        if "rusty_key" not in inventory:
            inventory.append("rusty_key")
            print("Вы открыли бронзовую шкатулку и нашли rusty_key!")
        else:
            print("Шкатулка пуста.")
        return

    print("Вы не знаете, как использовать этот предмет.")

