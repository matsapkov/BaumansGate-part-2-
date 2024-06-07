#редактор карт для Bauman's Gate
#нужно уметь создавать карту

from map_creator.map_obstacle import Obstacle
from database.map_database import Database
import pickle
import random
database = Database()

class MapCreator:
    SIZE = 0
    game_field = [[]]
    coordinates = {}
    sub_game_field = [[]]
    #obstacles = []

    def __init__(self, size):
        self.SIZE = size
        self.game_field = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.sub_game_field = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.create_coordinates()
        self.obstacles = []

    def create_coordinates(self):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(self.SIZE):
            self.coordinates[i] = {}
            for j in range(self.SIZE):
                self.coordinates[i][j] = f'{letters[j]}{i}'

    def fill_field(self):
        print(
            'Приступаем к созданию карты! Помните, первая линия и у противника, и у вас должна оставаться свободной '
            'от препятствий')

        for i in range(1, self.SIZE - 1):
            for j in range(self.SIZE):  # заполняем все клетки поля обычными клетками
                self.game_field[i][j] = '*'
                self.sub_game_field[i][j] = '*'
        for j in range(self.SIZE):
            self.game_field[0][j] = '*'
            self.game_field[self.SIZE - 1][j] = '*'
            self.sub_game_field[0][j] = '*'
            self.sub_game_field[self.SIZE - 1][j] = '*'

        print('Отлично! Карта создана, однако на ней нет препятствий.\n'
              '1.   Создать препятствия\n'
              '2.   Заполнить карту случайными базовыми препятствиями')
        choice = input()

        if choice == '1':
            print('Вы можете создать три вида препятствий. Пожалуйста, укажите для ваших препятствий параметры')
            for i in range(3):
                print('Введите символ препятствия, штраф для пеших, кавалеристов и лучников')
                sign = input('Символ: ')
                foot_penalty = int(input('Штраф для пеших: '))
                cavalry_penalty = int(input('Штраф для кавалеристов: '))
                shooting_penalty = int(input('Штраф для лучников: '))
                obstacle = Obstacle(sign, foot_penalty, cavalry_penalty, shooting_penalty)
                self.obstacles.append(obstacle)
            self.print_field()
            self.print_coordinates()
            self.place_obstacles(self.obstacles)
        elif choice == '2':
            obstacle_probability = [0.1, 0.2, 0.3]
            for i in range(1, self.SIZE - 1):
                for j in range(self.SIZE):
                    rand = random.random()
                    if rand < obstacle_probability[0]:
                        self.game_field[i][j] = '^'  # дерево
                        self.sub_game_field[i][j] = '^'
                    elif rand < obstacle_probability[1]:
                        self.game_field[i][j] = '#'  # болото
                        self.sub_game_field[i][j] = '#'
                    elif rand < obstacle_probability[2]:
                        self.game_field[i][j] = '{'  # холм
                        self.sub_game_field[i][j] = '{'
                    else:
                        self.game_field[i][j] = '*'  # обычная равнина
                        self.sub_game_field[i][j] = '*'
        else:
            print('Invalid choice!')

    def save_map(self):
        with open('map_creator/pickles/pickle.pkl', 'wb') as f:
            pickle.dump(self, f)
        file_path = 'map_creator/pickles/pickle.pkl'
        database.insert_into(file_path)

    def place_obstacles(self, obstacles):
        for obstacle in obstacles:
            while True:
                coord = input(f'Введите координаты для размещения препятствия {obstacle.symbol} (или "done" для завершения): ')
                if coord.lower() == 'done':
                    break
                if self.validate_coordinate(coord):
                    x, y = self.convert_coordinate(coord)
                    if self.game_field[x][y] == '*':
                        self.game_field[x][y] = obstacle.symbol
                        self.sub_game_field[x][y] = obstacle.symbol
                    else:
                        print('Клетка уже занята. Пожалуйста, выберите другую клетку.')
                else:
                    print('Некорректные координаты. Пожалуйста, введите координаты снова.')


    def validate_coordinate(self, coord):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if len(coord) < 2 or not coord[0].isalpha() or not coord[1:].isdigit():
            return False
        letter = coord[0].upper()
        number = int(coord[1:])
        if letter not in letters[:self.SIZE] or number < 0 or number >= self.SIZE:
            return False
        return True

    def convert_coordinate(self, coord):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        letter = coord[0].upper()
        number = int(coord[1:])
        x = number
        y = letters.index(letter)
        return x, y

    def print_field(self):
        for row in self.game_field:
            print(' '.join(map(str, row)))

    def print_coordinates(self):
        for i in range(self.SIZE):
            for j in range( self.SIZE):
                print(self.coordinates[i][j], end='\t')
            print()
