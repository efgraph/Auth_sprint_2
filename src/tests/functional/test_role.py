from http import HTTPStatus


def test_create_role(test_client, admin_tokens):
    response = test_client.post('/role', query_string={'jwt': admin_tokens[0]},
                                data=dict(name='subscriber', description='is subscriber'))
    assert response.status_code == HTTPStatus.OK


def test_edit_role(test_client, admin_tokens):
    response = test_client.put('/role', query_string={'jwt': admin_tokens[0]},
                               data=dict(name='subscriber', new_name='new_subscriber'))
    assert response.status_code == HTTPStatus.OK


def test_get_roles(test_client, admin_tokens):
    response = test_client.get('/role', query_string={'jwt': admin_tokens[0]})
    assert response.status_code == HTTPStatus.OK


def test_set_user_role(test_client, admin_tokens):
    response = test_client.post('/role/user', query_string={'jwt': admin_tokens[0]},
                                data=dict(login='user', role_name='new_subscriber'))
    assert response.status_code == HTTPStatus.OK


def test_get_user_roles(test_client, admin_tokens):
    response = test_client.get('/role/user', query_string={'jwt': admin_tokens[0], 'login': 'user'})
    assert response.status_code == HTTPStatus.OK


def test_delete_user_role(test_client, admin_tokens):
    response = test_client.delete('/role/user', query_string={'jwt': admin_tokens[0]},
                                  data=dict(login='user', role_name='new_subscriber'))
    assert response.status_code == HTTPStatus.OK


def test_delete_role(test_client, admin_tokens):
    response = test_client.delete('/role', query_string={'jwt': admin_tokens[0], 'name': 'new_subscriber'})
    assert response.status_code == HTTPStatus.OK
