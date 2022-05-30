import requests as rq
import json
# make a variable that will be accessable from functions

class Settings:
    def set_url(url_):
        global url
        url = url_

    def get_url():
        return url

    def set_token(token_):
        global token
        token = token_
    def get_token():
        return token
class User:
    def register(name, password):
        address = Settings.get_url() + '/register'
        payload = json.dumps({'name': name, 'password': password})
        headers = {'content-type': 'application/json'}
        r = rq.post(address, data=payload, headers=headers)
        return r.json()
    def login(name, password):
        address = Settings.get_url() + '/login'
        payload = json.dumps({'name': name, 'password': password})
        headers = {'content-type': 'application/json'}
        r = rq.post(address, data=payload, headers=headers)
        return r.json()
    def change_password(old,new):
        address = Settings.get_url() + '/change_password'
        payload = json.dumps({'oldpassword': old, 'newpassword': new})
        headers = {'content-type': 'application/json'}
        r = rq.post(address, data=payload, headers=headers)
        return r.json()
    def change_name(name):
        address = Settings.get_url() + '/change_name'
        payload = json.dumps({'name': name})
        headers = {'content-type': 'application/json'}
        r = rq.post(address, data=payload, headers=headers)
        return r.json()
    def get_user_info():
        address = Settings.get_url() + '/user_info'
        headers = {'content-type': 'application/json'}
        r = rq.get(address, headers=headers)

class Message:
    def get_last_messages():
        address = Settings.get_url() + '/messages'
        headers = {'x-access-tokens': token}
        r = rq.get(address, headers=headers)
        return r.json()
    def get_message(id):
        address = Settings.get_url() + '/message/' + id
        headers = {'x-access-tokens': token}
        r = rq.get(address, headers=headers)
        return r.json()
    def send_message(message):
        address = Settings.get_url() + '/add_message'
        payload = json.dumps({'message': message})
        headers = {'x-access-tokens': token, 'content-type': 'application/json'}
        r = rq.post(address, data=payload, headers=headers)
        return r.json()
    def delete_message(id):
        address = Settings.get_url() + '/delete_message/' + id
        headers = {'x-access-tokens': token}
        r = rq.delete(address, headers=headers)
        return r.json()
class Admin:
    def delete_user(id):
        address = Settings.get_url() + '/delete_user/' + id
        headers = {'x-access-tokens': token}
        r = rq.delete(address, headers=headers)
        return r.json()
    def delete_specific_message(id):
        address = Settings.get_url() + '/delete_specific_message/' + id
        headers = {'x-access-tokens': token}
        r = rq.delete(address, headers=headers)
        return r.json()

if __name__ == '__main__':
    Settings.set_url('http://localhost:5000')
    Settings.set_token(User.login('Lubekd','LUbeK')['token'])
    print(User.get_last_messages())
