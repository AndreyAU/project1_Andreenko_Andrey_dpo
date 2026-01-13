#!/usr/bin/env python3
"""Точка входа в игру."""

from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    describe_current_room,
    solve_puzzle,
    attempt_open_treasure,
    show_help,
)
from labyrinth_game.constants import ROOMS


def process_command(game_state: dict, command: str) -> None:
    """Обрабатывает команду пользователя."""
    if not command:
        return

    command = command.strip()
    parts = command.split()
    action = parts[0]

    if action == "look":
        describe_current_room(game_state)
        return

    if action == "go":
        if len(parts) < 2:
            print("Укажите направление.")
        else:
            move_player(game_state, parts[1])
        return

    if action == "take":
        if len(parts) < 2:
            print("Укажите, что взять.")
        else:
            # запрет на взятие сундука
            if parts[1] == "treasure_chest":
                print("Вы не можете поднять сундук, он слишком тяжелый.")
            else:
                take_item(game_state, parts[1])
        return

    if action == "use":
        if len(parts) < 2:
            print("Укажите, что использовать.")
        else:
            use_item(game_state, parts[1])
        return

    if action == "solve":
        current_room = game_state["current_room"]
        if current_room == "treasure_room":
            attempt_open_treasure(game_state)
        else:
            solve_puzzle(game_state)
        return

    if action == "help":
        show_help()
        return

    if action in ("inventory", "inv"):
        show_inventory(game_state)
        return

    if action in ("quit", "exit"):
        print("Игра завершена.")
        game_state["game_over"] = True
        return

    print("Неизвестная команда.")


def main() -> None:
    """Запуск игры."""
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,      # счётчик шагов
        "puzzles_solved": 0,   # счётчик решённых загадок
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input("> ")
        process_command(game_state, command)


if __name__ == "__main__":
    main()

