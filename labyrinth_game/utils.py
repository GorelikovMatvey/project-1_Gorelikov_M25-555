#!/usr/bin/env python3
import math

from labyrinth_game.constants import (
    COMMANDS,
    EVENT_PROBABILITY,
    EVENT_TYPES,
    TRAP_DAMAGE_THRESHOLD,
)


def describe_current_room(game_state):
    """
    Выводит описание текущей комнаты: название, описание,
    предметы, выходы и наличие загадки.
    """
    room_name = game_state['current_room']
    room = game_state['rooms'][room_name]
    print(f"\n== {room_name.upper()} ==")
    print(room['description'])
    if room['items']:
        print("Заметные предметы:", ", ".join(room['items']))
    if room['exits']:
        print("Выходы:", ", ".join(room['exits'].keys()))
    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state, get_input):
    """
    Позволяет игроку решить загадку в текущей комнате.
    При правильном ответе выдаёт награду в зависимости от комнаты.
    В trap_room при неверном ответе может сработать ловушка.
    """
    current_room = game_state['current_room']
    room = game_state['rooms'][current_room]
    if not room['puzzle']:
        print("Загадок здесь нет.")
        return
    question, answer = room['puzzle']
    print(question)
    user_answer = get_input("Ваш ответ: ")
    if user_answer.lower() in [answer.lower(), "десять"]:
        print("Правильно! Загадка решена.")
        room['puzzle'] = None
        if current_room == "hall":
            game_state['player_inventory'].append("treasure_key")
            print("Вы получили: treasure_key")
        elif current_room == "library":
            game_state['player_inventory'].append("rusty_key")
            print("Вы получили: rusty_key")
    else:
        print("Неверно. Попробуйте снова.")
        if current_room == "trap_room":
            trigger_trap(game_state)


def attempt_open_treasure(game_state, get_input):
    """
    Пытается открыть сундук с сокровищами.
    Игрок может использовать ключ или попытаться ввести код.
    Успех приводит к победе и завершению игры.
    """
    room = game_state['rooms'][game_state['current_room']]
    if "treasure_chest" not in room['items']:
        print("Сундук уже открыт или отсутствует.")
        return
    if "treasure_key" in game_state['player_inventory'] or "rusty_key" in \
            game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return
    choice = get_input("Сундук заперт. Ввести код? (да/нет) ")
    if choice.lower() == "да":
        code = get_input("Введите код: ")
        if room['puzzle'] and code in [room['puzzle'][1], "десять"]:
            print("Код верный! Сундук открыт, вы победили!")
            room['items'].remove("treasure_chest")
            game_state['game_over'] = True
        else:
            print("Код неверный.")
    else:
        print("Вы отступаете от сундука.")


def show_help():
    """
    Выводит список доступных команд игрока.
    """
    print("\nДоступные команды:")
    for cmd, desc in COMMANDS.items():
        print(f"  {cmd:<16} - {desc}")


def pseudo_random(seed, modulo):
    """
    Генератор псевдослучайных чисел на основе синуса.
    Возвращает число в диапазоне (0, modulo).
    """
    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(frac * modulo)


def trigger_trap(game_state):
    """
    Симулирует срабатывание ловушки.
    Если есть предметы в инвентаре — случайный предмет теряется.
    Если инвентарь пуст — шанс получить смертельный урон.
    """
    print("Ловушка активирована! Пол дрожит...")
    inventory = game_state['player_inventory']
    if inventory:
        idx = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        danger = pseudo_random(game_state['steps_taken'], 10)
        if danger < TRAP_DAMAGE_THRESHOLD:
            print("Пол провалился! Вы погибли.")
            game_state['game_over'] = True
        else:
            print("Вы чудом избежали гибели!")


def random_event(game_state):
    """
    Случайное событие, происходящее во время перемещения игрока.
    Может быть: находка монетки, испуг, срабатывание ловушки.
    """
    if pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY) == 0:
        event_type = pseudo_random(game_state['steps_taken'] + 1, EVENT_TYPES)
        if event_type == 0:
            print("Вы находите монетку на полу.")
            game_state['rooms'][game_state['current_room']]['items'].append(
                'coin')
        elif event_type == 1:
            print("Вы слышите шорох.")
            if "sword" in game_state['player_inventory']:
                print("Вы взмахиваете мечом и отпугиваете существо.")
        elif event_type == 2:
            if game_state['current_room'] == "trap_room" and "torch" not in \
                    game_state['player_inventory']:
                print("Темно и опасно... что-то активировалось!")
                trigger_trap(game_state)
