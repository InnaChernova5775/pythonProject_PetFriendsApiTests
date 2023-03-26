import pytest
from conftest import pf
def generate_string(n):
   return "x" * n

def russian_chars():
   return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

# Здесь мы взяли 20 популярных китайских иероглифов
def chinese_chars():
   return '的一是不了人我在有他这为之大来以个中上们'

def special_chars():
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


@pytest.mark.api
@pytest.mark.get
@pytest.mark.parametrize("filter",
                        ['', 'my_pets'],
                        ids=['empty string', 'only my pets'])
def test_get_all_pets(get_auth_key, filter):
    status, result = pf.get_list_of_pets(get_auth_key['key'],filter)
    assert status == 200
    assert len(result['pets']) > 0

pytest.mark.xfail(reason="БАГ!!! в реализации АPI") # ожидаемый ответ статус:400, получаем актуальный статус:500.
@pytest.mark.parametrize("filter",
                         [generate_string(255),generate_string(1001),russian_chars(),
                            russian_chars().upper(),chinese_chars(),special_chars(),123],
                          ids=['255 symbols','more than 1000 symbols','russian','RUSSIAN','chinese','specials','digit'])
def test_get_all_pets_negative_filter(get_auth_key, filter):
    status, result = pf.get_list_of_pets(get_auth_key['key'],filter)
    assert status == 400
#БАГ! Ожидаемый статус:400, актуальный статус: 500


@pytest.mark.api
@pytest.mark.post
def test_post_add_new_pets_with_pet_photo(get_auth_key, name='Бимбо', animal_type='лабрадор', age='2', pet_photo='images/Bimbo.jpg'):
    status, result = pf.add_new_pet(get_auth_key['key'], name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

@pytest.mark.api
@pytest.mark.delete
def test_successful_deletion_pet_with_valid_pet_id(get_auth_key):
    _, myPets = pf.get_list_of_pets(get_auth_key['key'], filter="my_pets")
    if len(myPets['pets']) == 0:
        pf.add_new_pet(get_auth_key['key'], name='Бимбо', animal_type='лабрадор', age='2', pet_photo='images/Bimbo.jpg')
        _, myPets = pf.get_list_of_pets(get_auth_key['key'], filter="my_pets")
    pet_id = myPets['pets'][0]['id']
    status, result = pf.delete_pet(get_auth_key['key'], pet_id)
    _, myPets = pf.get_list_of_pets(get_auth_key['key'], "my_pets")
    assert status == 200
    assert pet_id not in myPets.values()

@pytest.mark.api
@pytest.mark.put
def test_successful_update_info_pet(get_auth_key, name='Ричи', animal_type='сенбернар', age='3'):
    _, myPets = pf.get_list_of_pets(get_auth_key['key'], filter="my_pets")
    if len (myPets['pets']) > 0:
        status, result = pf.update_info_pet(get_auth_key['key'], myPets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    elif len(myPets['pets']) == 0:
        pf.add_new_pet(get_auth_key['key'], name='Бимбо', animal_type='лабрадор', age='2', pet_photo='images/Bimbo.jpg')
        _, myPets = pf.get_list_of_pets(get_auth_key['key'], filter="my_pets")
        status, result = pf.update_info_pet(get_auth_key['key'], myPets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

@pytest.mark.api
@pytest.mark.post
def test_create_new_pets_without_photo(get_auth_key, name='Матроскин', animal_type='кот', age=4):
    status, result = pf.greate_pet_simple(get_auth_key['key'], name, animal_type, age)
    assert status == 200
    assert result['name'] == name

@pytest.mark.api
@pytest.mark.post
def test_add_pet_photo_for_pet_id(get_auth_key, pet_photo='images/Cat.jpg'):
    _, my_pet = pf.greate_pet_simple(get_auth_key['key'], name='Севастьян', animal_type='кот', age=3)
    _, myPets = pf.get_list_of_pets(get_auth_key['key'], filter="my_pets")
    pet_id = myPets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(get_auth_key['key'], pet_id, pet_photo)
    assert status == 200

@pytest.mark.api
@pytest.mark.mult
def test_multytest_pets(get_auth_key, name='Бимбо', animal_type='лабрадор', age='2', pet_photo='images/Bimbo.jpg'):
    status, result = pf.add_new_pet(get_auth_key['key'], name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    print(result)

    _, myPets = pf.get_list_of_pets(get_auth_key['key'], filter="my_pets")
    status, result = pf.update_info_pet(get_auth_key['key'], myPets['pets'][0]['id'], name='Айрис',
                                                 animal_type='сенбернар', age='1')
    assert status == 200
    assert result['name'] == 'Айрис'
    print(result)

    status, result = pf.delete_pet(get_auth_key['key'], myPets['pets'][0]['id'])
    assert status == 200
    assert myPets['pets'][0]['id'] not in myPets.values()
    print(result)

    status, result = pf.greate_pet_simple(get_auth_key['key'], name='Мартин', animal_type='золотистый ретривер', age=2)
    assert status == 200
    assert result['name'] == 'Мартин'
    print(result)

    _, MyPets = pf.get_list_of_pets(get_auth_key['key'], filter="my_pets")
    status, result = pf.add_photo_of_pet(get_auth_key['key'], MyPets['pets'][0]['id'], 'images/Dog.jpg')
    assert status == 200
    print(result)

@pytest.mark.xfail(reason="БАГ!!! в реализации АPI") # ожидаемый ответ статус:400, получаем актуальный статус:200.
def test_create_new_pet_with_invalid_param(get_auth_key, name='', animal_type='', age=''):
    status, result = pf.greate_pet_simple(get_auth_key['key'], name, animal_type, age)
    assert status == 400
# #БАГ!!!Новый питомец с некорректными параметрами появляется на сайте

@pytest.mark.xfail(reason="БАГ!!! в реализации АPI") # ожидаемый ответ статус:400, получаем актуальный статус:200.
def test_create_new_pet_with_invalid_age(get_auth_key, name='Матроскин', animal_type='кот', age=2000):
    status, result = pf.greate_pet_simple(get_auth_key['key'], name, animal_type, age)
    assert status == 400
# БАГ!!!Новый питомец с некорректными параметрами появляется на сайте

@pytest.mark.xfail(reason="БАГ!!! в реализации АPI") # ожидаемый ответ статус:400, получаем актуальный статус:200.
def test_create_new_pet_with_invalid_type_name(get_auth_key, name='', animal_type='кот', age=4):
    status, result = pf.greate_pet_simple(get_auth_key['key'], name, animal_type, age)
    assert status == 400
 # БАГ!!!Новый питомец с некорректными параметрами появляется на сайте

@pytest.mark.xfail(reason="БАГ!!! в реализации АPI") # ожидаемый ответ статус:400, получаем актуальный статус:200.
def test_create_new_pet_with_invalid_type_name2(get_auth_key, name= '@@@@@$$$$', animal_type='кот', age=4):
    status, result =pf.greate_pet_simple(get_auth_key['key'], name, animal_type, age)
    assert status == 400
# БАГ!!!Новый питомец с некорректными параметрами появляется на сайте

@pytest.mark.xfail(reason="БАГ!!! в реализации АPI") # ожидаемый ответ статус:400, получаем актуальный статус:200.
def test_create_new_pet_with_invalid_type_animal_type(get_auth_key, name='Феликс', animal_type='',age=4):
    status, result = pf.greate_pet_simple(get_auth_key['key'], name, animal_type, age)
    assert status == 400
# БАГ!!!Новый питомец с некорректными параметрами появляется на сайте

