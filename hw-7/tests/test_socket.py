import json


class TestUserCreate:
    def test_create(self, socket_client, random_user):
        resp = socket_client.post('/create', data=json.dumps(random_user), jsonify_response=True)

        assert resp['status_code'] == '201'
        assert json.loads(resp['data']) == random_user

        socket_client.delete('/delete', data=json.dumps(random_user), jsonify_response=True)

    def test_create_without_last_name(self, socket_client, random_first_name):
        resp = socket_client.post('/create', data=json.dumps(random_first_name), jsonify_response=True)

        assert resp['status_code'] == '400'


class TestUserGet:
    def test_get(self, socket_client, random_user):
        socket_client.post('/create', data=json.dumps(random_user), jsonify_response=True)
        resp = socket_client.get(f'/get_surname/{random_user["name"]}', jsonify_response=True)

        assert resp['status_code'] == '200'
        assert json.loads(resp['data']) == random_user['surname']

    def test_get_non_existing(self, socket_client, random_user):
        resp = socket_client.get(f'/get_surname/{random_user["name"]}', jsonify_response=True)

        assert resp['status_code'] == '404'


class TestUserUpdate:
    def test_update_existing(self, socket_client, random_user, random_last_name):
        last_name = random_last_name['surname']
        user = random_user.copy()

        socket_client.post('/create', data=json.dumps(user), jsonify_response=True)
        user['surname'] = last_name
        resp = socket_client.put('/update', data=json.dumps(user), jsonify_response=True)

        assert resp['status_code'] == '200'
        assert json.loads(resp['data']) == user

        socket_client.delete('/delete', data=json.dumps(user), jsonify_response=True)

    def test_update_non_existing(self, socket_client, random_user):
        resp = socket_client.put('/update', data=json.dumps(random_user), jsonify_response=True)

        assert resp['status_code'] == '201'
        assert json.loads(resp['data']) == random_user

        socket_client.delete('/delete', data=json.dumps(random_user), jsonify_response=True)


class TestUserDelete:
    # Если в других тестах не удалять после себя пользователей, то может случиться,
    # что faker два раза выдаст одного и того же пользователя - тогда тест упадет
    def test_delete(self, socket_client, random_user):
        socket_client.post('/create', data=json.dumps(random_user), jsonify_response=True)
        resp = socket_client.delete('/delete', data=json.dumps(random_user), jsonify_response=True)

        assert resp['status_code'] == '200'

    def test_delete_non_existing(self, socket_client, random_user):
        resp = socket_client.delete('/delete', data=json.dumps(random_user), jsonify_response=True)

        assert resp['status_code'] == '404'
