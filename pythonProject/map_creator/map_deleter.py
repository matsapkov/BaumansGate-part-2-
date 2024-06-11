from database.map_database import Database
database = Database()


class MapDeleter:
    def __init__(self):
        pass

    def delete_map(self):

        search_name = input('Введите имя карты, которую вы хотите удалить...\n')

        database.delete_from(search_name)

        print(f'Удалена карта {search_name}')
