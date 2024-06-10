import pytest
import io
import pickle
from unittest.mock import patch
from pythonProject.map_creator.create_map import MapCreator
from pythonProject.database.map_database import Database
from pythonProject.main import main

database = Database()

def get_from_db():
    data = database.return_map('ТестовоеСозданиеКарты')[0]

    with open('map_creator/pickles/searched_pickle.pkl', 'wb') as f:
        f.write(data)

    with open('map_creator/pickles/searched_pickle.pkl', 'rb') as f:
        searched_map = pickle.load(f)

        return searched_map


@pytest.fixture(scope='function', autouse=False)
def prepare_map_creator():
    main_ = main()
    return main_


def test_map_creation(prepare_map_creator):
    fake_inputs = ['1', '6', '2', 'ТестовоеСозданиеКарты']
    with patch('builtins.input', side_effect=fake_inputs):
        prepare_map_creator.run()

    if get_from_db():
        print('Tast passed!')
        assert True
    else:
        assert False


def test_obstacles(prepare_map_creator):
    fake_inputs = ['1', '6', '1', '$', '1', '2', '3', '%', '1', '2', '3', '£', '1', '2', '3', 'A1', 'done', 'A2', 'done', 'A3', 'done', 'ТестовоеСозданиеКарты']
    with patch('builtins.input', side_effect=fake_inputs):
        prepare_map_creator.run()

    if get_from_db():
        print('Tast passed!')
        assert True
    else:
        assert False


def test_map_editor(prepare_map_creator):
    fake_inputs1 = ['1', '6', '1', '$', '1', '2', '3', '%', '1', '2', '3', '£', '1', '2', '3', 'A1', 'done', 'A2', 'done', 'A3', 'done', 'ТестовоеСозданиеКарты']
    fake_inputs2 = ['3', 'ТестовоеСозданиеКарты', '2']
    with patch('builtins.input', side_effect=fake_inputs1):
        prepare_map_creator.run()
    with patch('builtins.input', side_effect=fake_inputs2):
        result = prepare_map_creator.run()

    assert result is None

