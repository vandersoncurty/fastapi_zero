from http import HTTPStatus


def test_root_deve_retornar_hello_world(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'securepassword',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'johndoe',
        'email': 'johndoe@example.com',
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'johndoe',
                'email': 'johndoe@example.com',
            }
        ]
    }


def test_update_user(client):
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


def test_delete_user(client):
    response = client.delete('/users/1/')
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


def test_delete_error_user_not_found(client):
    response = client.delete('/users/999/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_error_user_not_found(client):
    response = client.get('/users/999/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user(client):
    client.post(
        '/users/',
        json={
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'securepassword',
        },
    )
    response = client.get('/users/1/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'johndoe',
        'email': 'johndoe@example.com',
    }
