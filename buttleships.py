""" Условные обозначения в игре:
    * - корабль
    О - пустое поле
    X - попадание
    T - промах   """

import random

# Добавляем класс точек на игровом поле
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Добавляем класс корабля на игровом поле
class Ship:
    def __init__(self, size):
        self.size = size
        self.hits = 0

# Добавляем класс доски на игровом поле
class Board:
    def __init__(self):
        self.board = [['O' for _ in range(6)] for _ in range(6)]
        self.ships = [Ship(3), Ship(2), Ship(2), Ship(1), Ship(1), Ship(1), Ship(1)]

    def place_ships(self):
        for ship in self.ships:
            while True:
                x = random.randint(0, 5)
                y = random.randint(0, 5)
                if self.board[x][y] == 'O':
                    self.board[x][y] = '*'
                    if ship.size > 1:
                        orientation = random.choice(['horizontal', 'vertical'])
                        if orientation == 'horizontal':
                            if y + ship.size <= 6:
                                if all(self.board[x][y + i] == 'O' for i in range(ship.size)):
                                    for i in range(ship.size):
                                        self.board[x][y + i] = '*'
                                    break
                            else:
                                if x + ship.size <= 6:
                                    if all(self.board[x + i][y] == 'O' for i in range(ship.size)):
                                        for i in range(ship.size):
                                            self.board[x + i][y] = '*'
                                        break
                else:
                    break

    def print_boards(self):
        print(" Ваше поле: Поле противника:")
        print("  1 2 3 4 5 6     1 2 3 4 5 6")
        for i in range(6):
            print(f"{i+1} {' '.join(self.board[i])}   {i+1} {' '.join(['O' for _ in range(6)])}")

    def shot(self, dot):
        if self.board[dot.x][dot.y] == 'O':
            self.board[dot.x][dot.y] = 'T'
            return "Мимо!"
        elif self.board[dot.x][dot.y] == '*':
            self.board[dot.x][dot.y] = 'X'
            for ship in self.ships:
                if ship.hits < ship.size:
                    ship.hits += 1
                    if ship.hits == ship.size:
                        self.ships.remove(ship)
                        break
            return "Попадание!"
        elif self.board[dot.x][dot.y] == 'T' or self.board[dot.x][dot.y] == 'X':
            return "Уже стреляли сюда!"

# Добавляем класс игрока
class Player:
    def move(self):
        while True:
            try:
                x = int(input("Введите номер строки (от 1 до 6): ")) - 1
                y = int(input("Введите номер столбца (от 1 до 6): ")) - 1
                if x < 0 or x > 5 or y < 0 or y > 5:
                    raise ValueError("Ошибка! Введите число от 1 до 6.")
                return Dot(x, y)
            except ValueError:
                print("Ошибка! Введите число от 1 до 6.")

# Добавляем класс противника (компьютера)
class ComputerPlayer:
    def move(self):
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        return Dot(x, y)

# Добавляем класс игры, в котором указываем основную логику игры
class Game:
    def __init__(self):
        self.player_board = Board()
        self.enemy_board = Board()

    def print_boards(self):
        print(" Ваше поле   Поле противника")
        print("  1 2 3 4 5 6     1 2 3 4 5 6")
        for i in range(6):
            print(f"{i+1} {' '.join(self.player_board.board[i])}   {i+1} {' '.join(self.enemy_board.board[i])}")

    def move(self):
        while True:
            try:
                x = int(input("Введите номер строки (от 1 до 6): ")) - 1
                y = int(input("Введите номер столбца (от 1 до 6): ")) - 1
                if x < 0 or x > 5 or y < 0 or y > 5:
                    raise ValueError("Ошибка! Введите число от 1 до 6.")
                return x, y
            except ValueError:
                print("Ошибка! Введите число от 1 до 6.")

    def play(self):
        print("Добро пожаловать в игру Морской бой!")
        print("--------------------")
        print("Формат ввода: x y")
        print("x - номер строки (от 1 до 6)")
        print("y - номер столбца (от 1 до 6)")
        print("--------------------")
        self.player_board.place_ships()
        self.enemy_board.place_ships()
        self.print_boards()
        while True:
            print("--------------------")
            x, y = self.move()
            print("--------------------")
            if self.enemy_board.board[x][y] == 'O':
                self.enemy_board.board[x][y] = 'T'
                print("Мимо!")
            elif self.enemy_board.board[x][y] == '*':
                self.enemy_board.board[x][y] = 'X'
                print("Попадание!")
            elif self.enemy_board.board[x][y] == '•' or self.enemy_board.board[x][y] == 'X':
                print("Уже стреляли сюда!")
            self.print_boards()
            if not self.enemy_board.ships:
                print("Вы победили!")
                break
            computer_move = ComputerPlayer().move()
            result = self.player_board.shot(computer_move)
            print(f"Ход противника: {computer_move.x + 1} {computer_move.y + 1}")
            print(f"Результат хода противника: {result}")
            self.print_boards()
            if not self.player_board.ships:
                print("Вы проиграли!")
                break

game = Game()
game.play()