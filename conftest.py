import pytest
from settings import valid_email, valid_password
from api import PetFriends
from datetime import datetime

pf=PetFriends()

@pytest.fixture()
def get_auth_key():
    """Метод делает запрос к API сервера по валидному еmail и валидному паролю, и возвращает ответ в формате JSON,
    # который содержит уникальный ключ. """
    status, auth_key = pf.get_api_key (valid_email, valid_password)
    return  auth_key

@pytest.fixture(autouse=True)
def delta_time():
    start_time=datetime.now()
    yield
    end_time= datetime.now()
    print(f"\n Время прохождение теста составляет:{end_time-start_time}")

@pytest.fixture(autouse=True)
def request_fixture(request):
    if 'pets' or 'pet'  in request.function.__name__:
        print(f"\nЗапущен тест из сьюта Дом Питомца: {request.function.__name__}")

# @pytest.fixture(autouse=True)
# def delete_data_for_tests():
#     print ('После прохождения теста, тестовые данные будут удалены с сервера')
#     yield
#     status,result = pf.get_list_of_pets(get_auth_key['key'], "my_pets")
#     while len(result['pets']) > 0:
#         pet_id = result['pets'][0]['id']
#         pf.delete_pet(get_auth_key['key'], pet_id)
#         status, myPets = pf.get_list_of_pets(get_auth_key['key'], "my_pets")
#         print('Тестовые данные удалены')



