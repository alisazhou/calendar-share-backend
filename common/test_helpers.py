import json


def get_user_token(client, username, password):
    login_response = client.post(
        '/obtain-auth-token/',
        data={'username': username, 'password': password})
    token = json.loads(login_response.content.decode())['token']
    return token
