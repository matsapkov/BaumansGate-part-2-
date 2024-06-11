import pickle
from database.map_database import Database
database = Database()


class MapEditor:

    def find_map(self):

        search_name = input('Введите имя карты, которую вы хотите изменить...\n')

        data = database.return_map(search_name)[0]

        with open('map_creator/pickles/searched_pickle.pkl', 'wb') as f:
            f.write(data)

        with open('map_creator/pickles/searched_pickle.pkl', 'rb') as f:
            searched_map = pickle.load(f)

        print(f'Найдена карта {search_name}')
        searched_map.print_field()
        print(f'Препятствия на этой карте: {searched_map.obstacles}')
        searched_map.create_coordinates()
        searched_map.print_coordinates()
        return (searched_map, search_name)

    def change_map(self):
        returnings = self.find_map()
        map = returnings[0]
        NAME = returnings[1]
        map.fill_field()

        with open('map_creator/pickles/pickle.pkl', 'wb') as f:
            pickle.dump(map, f)

        with open('map_creator/pickles/pickle.pkl', 'rb') as f:
            DATA = f.read()
        print(DATA)
        print(type(DATA))
        database.update_table(DATA, NAME)

