#!/usr/bin/env python3
from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command_line):
    """
    Обрабатывает введённую пользователем команду
    и вызывает соответствующее действие.
    Поддерживает перемещение, просмотр комнаты,
    работу с предметами, решение загадок,
    управление инвентарём и завершение игры.
    """
    parts = command_line.split()
    if not parts:
        return

    command = parts[0]
    args = ' '.join(parts[1:])
    directions = ["north", "south", "east", "west"]
    if command in directions:
        move_player(game_state, command)
        return

    match command:
        case "look":
            describe_current_room(game_state)
        case "go":
            if args:
                move_player(game_state, args)
        case "take":
            if args:
                take_item(game_state, args)
        case "use":
            if args:
                if (args == "treasure_chest" and
                        game_state['current_room'] == "treasure_room"):
                    attempt_open_treasure(game_state, get_input)
                else:
                    use_item(game_state, args)
        case "inventory":
            show_inventory(game_state)
        case "solve":
            if game_state['current_room'] == "treasure_room":
                attempt_open_treasure(game_state, get_input)
            else:
                solve_puzzle(game_state, get_input)
        case "quit" | "exit":
            game_state['game_over'] = True
        case "help":
            show_help()
        case _:
            print("Неизвестная команда.")


def main():
    """
    Точка входа в игру.
    Инициализирует состояние игры и запускает основной игровой цикл,
    в котором игрок вводит команды до тех пор,
    пока игра не будет завершена.
    """
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0,
        'rooms': ROOMS
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input("> ")
        process_command(game_state, command)


if __name__ == "__main__":
    main()
