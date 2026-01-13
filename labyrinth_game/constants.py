# labyrinth_game/constants.py

COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "north/south/east/west": "перейти без команды go",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "решить загадку или открыть сундук",
    "help": "показать список команд",
    "quit": "выйти из игры",
}

ROOMS = {
    "entrance": {
        "description": (
            "Вы в темном входе лабиринта. "
            "Стены покрыты мхом. "
            "На полу лежит старый факел."
        ),
        "exits": {"north": "hall", "east": "trap_room"},
        "items": ["torch"],
        "puzzle": None,
    },
    "hall": {
        "description": (
            "Большой зал с эхом. "
            "По центру стоит пьедестал с запечатанным сундуком."
        ),
        "exits": {
            "south": "entrance",
            "west": "library",
            "north": "treasure_room",
            "east": "storage",
        },
        "items": [],
        "puzzle": (
            'На пьедестале надпись: "Назовите число, которое идет после девяти".',
            "10",
        ),
    },
    "trap_room": {
        "description": (
            "Комната с хитрой плиточной поломкой. "
            "На стене видна надпись: «Осторожно — ловушка»."
        ),
        "exits": {"west": "entrance"},
        "items": ["rusty_key"],
        "puzzle": (
            "Два брюшка, четыре ушка.",
            "подушка",
        ),
    },
    "library": {
        "description": "Пыльная библиотека. На полках старые свитки.",
        "exits": {"east": "hall", "north": "armory"},
        "items": ["ancient_book"],
        "puzzle": (
            "Кто на себе свой дом носит?",
            "улитка",
        ),
    },
    "armory": {
        "description": (
            "Старая оружейная комната. "
            "На стене висит меч, рядом — бронзовая шкатулка."
        ),
        "exits": {"south": "library", "east": "hidden_corridor"},
        "items": ["sword", "bronze_box"],
        "puzzle": None,
    },
    "treasure_room": {
        "description": "Комната с большим сундуком. Дверь заперта — нужен особый ключ.",
        "exits": {"south": "hall"},
        "items": ["treasure_chest"],
        "puzzle": (
            "Введите код (подсказка: 2 * 5 = ?)",
            "10",
        ),
    },
    "storage": {
        "description": "Небольшая кладовая. В углах валяются старые ящики.",
        "exits": {"west": "hall"},
        "items": ["old_rope"],
        "puzzle": None,
    },
    "hidden_corridor": {
        "description": "Узкий скрытый коридор. Здесь тихо и пыльно.",
        "exits": {"west": "armory"},
        "items": [],
        "puzzle": None,
    },
}

