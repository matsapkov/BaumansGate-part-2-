from database.map_database import Database
from map_creator.create_map import MapCreator
from map_creator.map_deleter import MapDeleter
from map_creator.map_editor import MapEditor

database = Database()
print("\nДобро пожаловать в редактор карт Bauman's Gate! Выберите действие: ")
print('1. Создание новой карты')
print('2. Удаление уже существующей карты')
print('3. Изменение существующей карты')

choice = input()

if choice == '1':
    size = int(input('Введите размер игрового поля X на X:  '))
    map_creator = MapCreator(size)
    map_creator.fill_field()
    map_creator.create_coordinates()
    map_creator.print_field()
    map_creator.print_coordinates()
    map_creator.save_map()
    print(f'Препятствия на созданной карте: {map_creator.obstacles}')
elif choice == '2':
    map_deleter = MapDeleter()
    map_deleter.delete_map()
elif choice == '3':
    map_editor = MapEditor()
    map_editor.find_map()
    map_editor.change_map()
else:
    print('Invalid input!')

