#!/usr/bin/env python3
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state):
    """
    Выводит список предметов в инвентаре игрока или сообщает,
    что инвентарь пуст.
    """
    inventory = game_state['player_inventory']
    if inventory:
        print("Инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")


def get_input(prompt="> "):
    """
    Получает ввод пользователя с консоли.
    Возвращает введённую строку или команду 'quit' при выходе из игры.
    """
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    """
    Перемещает игрока в указанном направлении,
    если есть выход из текущей комнаты.
    Обновляет шаги, выводит описание новой комнаты
    и может вызвать случайное событие.
    """
    current_room = game_state['current_room']
    exits = game_state['rooms'][current_room]['exits']

    if direction in exits:
        next_room = exits[direction]
        if next_room == "treasure_room" and (
                "treasure_key" not in game_state['player_inventory']):
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return
        elif next_room == "treasure_room":
            print(
                "Вы используете найденный ключ,"
                " чтобы открыть путь в комнату сокровищ.")

        game_state['current_room'] = next_room
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    """
    Позволяет игроку поднять предмет из текущей комнаты
    и добавить его в инвентарь.
    """
    current_room = game_state['current_room']
    room = game_state['rooms'][current_room]

    if item_name in room['items']:
        room['items'].remove(item_name)
        game_state['player_inventory'].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    """
    Позволяет игроку поднять предмет из текущей комнаты
    и добавить его в инвентарь.
    """
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Факел осветил путь, стало светлее.")
    elif item_name == "sword":
        print("С мечом в руках вы чувствуете уверенность.")
    elif item_name == "bronze box":
        if "rusty_key" not in game_state['player_inventory']:
            print("Вы открыли бронзовую шкатулку и нашли ржавый ключ!")
            game_state['player_inventory'].append("rusty_key")
        else:
            print("Шкатулка пуста.")
    else:
        print("Вы не знаете, как использовать этот предмет.")
