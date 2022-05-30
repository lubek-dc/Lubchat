import requests as rq
import json

# make a variable that will be accessable from functions




def set_url(url_):
    global url
    url = url_


#get url function
def get_url():
    return url

def set_token(token_):
    global token
    token = token_
def get_token():
    return token
class User:
    def register(name, password):
        address = get_url() + '/register'
        payload = json.dumps({'name': name, 'password': password})
        headers = {'content-type': 'application/json'}
        r = rq.post(address, data=payload, headers=headers)
        return r
    def login(name, password):
        address = get_url() + '/login'
        payload = json.dumps({'name': name, 'password': password})
        headers = {'content-type': 'application/json'}
        r = rq.post(address, data=payload, headers=headers)
        set_token(r.json()['token'])
        return r.json()
    def change_password(old,new):
        address = get_url() + '/change_password'
        payload = json.dumps({'oldpassword': old, 'newpassword': new})
        headers = {'content-type': 'application/json', 'x-access-tokens': get_token()}
        r = rq.post(address, data=payload, headers=headers)
        return r.json()
    def change_name(name):
        address = get_url() + '/change_name'
        payload = json.dumps({'name': name})
        headers = {'content-type': 'application/json','x-access-tokens': get_token()}
        r = rq.post(address, data=payload, headers=headers)
        return r.json()
    def get_user_info():
        address = get_url() + '/user'
        headers = {'content-type': 'application/json', 'x-access-tokens': get_token()}
        r = rq.get(address, headers=headers)
        return r.json()
    def grant_rank(userid,rankid):
        address = get_url() + '/grant_rank'
        payload = json.dumps({'userid': userid, 'rankid': rankid})
        headers = {'content-type': 'application/json', 'x-access-tokens': get_token()}
        r = rq.post(address, data=payload, headers=headers)
        return r.json()
    def revoke_rank(userid):
        address = get_url() + '/revoke_rank'
        payload = json.dumps({'userid': userid})
        headers = {'content-type': 'application/json', 'x-access-tokens': get_token()}
        r = rq.post(address, data=payload, headers=headers)
        return r.json()
    def get_user_by_id(userid):
        address = get_url() + '/user/' + str(userid)
        headers = {'content-type': 'application/json', 'x-access-tokens': get_token()}
        r = rq.get(address, headers=headers)
        return r.json()
    def get_user_by_name(name):
        address = get_url() + '/user/name/' + name
        headers = {'content-type': 'application/json', 'x-access-tokens': get_token()}
        r = rq.get(address, headers=headers)
        return r.json()

class Message:
    def get_last_messages():
        address = get_url() + '/messages'
        headers = {'x-access-tokens': token}
        r = rq.get(address, headers=headers)
        return r.json()
    def get_message(id):
        address = get_url() + '/message/' + id
        headers = {'x-access-tokens': token}
        r = rq.get(address, headers=headers)
        return r.json()
    def send_message(message):
        address = get_url() + '/add_message'
        payload = json.dumps({'message': message})
        headers = {'x-access-tokens': token, 'content-type': 'application/json'}
        r = rq.post(address, data=payload, headers=headers)
        return r.json()
    def delete_message(id):
        address = get_url() + '/delete_message/' + id
        headers = {'x-access-tokens': token}
        r = rq.delete(address, headers=headers)
        return r.json()
class Admin:
    def delete_user(id):
        address = get_url() + '/delete_user/' + id
        headers = {'x-access-tokens': token}
        r = rq.delete(address, headers=headers)
        return r.json()
    def delete_specific_message(id):
        address = get_url() + '/delete_specific_message/' + id
        headers = {'x-access-tokens': token}
        r = rq.delete(address, headers=headers)
        return r.json()

if __name__ == '__main__':
    set_url('http://localhost:5000')
    set_token(User.login('Lubekd','LUbeK')['token'])
    print(User.get_last_messages())
