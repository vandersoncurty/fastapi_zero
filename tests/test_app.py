from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_root_deve_retornar_hello_world(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'securepassword',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@example.com',
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [user_schema],
    }


def test_update_user(client, user):
    response = client.put(
        '/users/1/',
        json={
            'username': 'janedoe',
            'email': 'janedoe@example.com',
            'password': 'securepassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'janedoe',
        'email': 'janedoe@example.com',
    }


def test_update_error_user_not_found(client):
    response = client.put(
        '/users/999/',
        json={
            'username': 'nonexistent',
            'email': 'nonexistent@example.com',
            'password': 'securepassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1/')
    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'User deleted'}


def test_delete_error_user_not_found(client):
    response = client.delete('/users/999/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_error_user_not_found(client):
    response = client.get('/users/999/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user_by_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_update_integrity_error(client, user):
    # Criando um registro para "fausto"
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user.username das fixture para fausto
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already registered'}


def test_create_user_conflict_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'bob',  # mesmo username da fixture 'user'
            'email': 'different@example.com',
            'password': 'anotherpassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already registered'}


def test_create_user_conflict_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'differentusername',
            'email': 'bob@example.com',  # mesmo email da fixture 'user'
            'password': 'anotherpassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already registered'}
