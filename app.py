# hello_world.py

from ctypes import alignment
from tkinter import CENTER
from urllib import response
import PySimpleGUI as sg
import requests
import json
from HackChat import app as hcAPI
import threading
import configparser
import git
#sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()
repourl = "https://github.com/lubek-dc/Lubchat.git"
configparser_ = configparser.ConfigParser()

# checks if config.ini exists
if not configparser_.read('config.ini'):
    # if not, create one
    configparser_.add_section('server')
    configparser_.set('server', 'url', '')
    configparser_.add_section('user')
    configparser_.set('user', 'token', '')
    configparser_.write(open('config.ini', 'w'))
# Read version from file version.txt
def get_local_version():
    file = open('version.txt', 'r')
    version = file.read()
    file.close()
    print(version)
    return version
    

# Get version from github 

def log_to_file(text_to_log):
    file = open("log.txt", "w", encoding='utf8') #temporary (later change to append mode)
    file.write(text_to_log)
    file.close()
    

def get_version():
    r = requests.get('https://raw.githubusercontent.com/lubek-dc/Lubchat/main/version.txt')
    return r.text

def refresh_loop():
    threading.Timer(1, refresh_loop).start()
    messages = hcAPI.Message.get_last_messages()
    output = ''
    for message in messages['messages']:
        output += '[' + message['author'] + '] ' + message['message'] + '\n'
       
    log_to_file(output)
    global texte
    texte = output
    

def register_window():
    #layout: username, email, password, confirm password
        layout = [[sg.Text('Username', size=(15, 1)) , sg.InputText()],
                    [sg.Text('Password', size=(15, 1)), sg.InputText()],
                    [sg.Text('Confirm Password', size=(15, 1)), sg.InputText()],
                    [sg.Button('Register'), sg.Button('Cancel')]]
                    
        window = sg.Window('LubChat - Register', layout)
        event, values = window.read()
        if event == 'Register':
            #check if all are filled
            if values[0] == '' or values[1] == '' or values[2] == '':
                # make a popup
                sg.popup('Please enter all the fields!')
                window.close()
                register_window()
                
            #check if password and confirm password are the same
            elif values[1] != values[2]:
                sg.popup('Passwords are not the same!')
                window.close()
                register_window()
            else:
                data = hcAPI.User.register(values[0], values[1])
                print(data)
                window.close()
                sg.popup('You have been registered! Have a nice day.')
                exit()

def login_window():
    #layout: username, password
        layout = [[sg.Text('Username', size=(15, 1)) , sg.InputText()],
                    [sg.Text('Password', size=(15, 1)), sg.InputText()],
                    [sg.Button('Login'), sg.Button('Cancel')],
                    [sg.Checkbox('Remember me')]]
                    
        window = sg.Window('LubChat - Login', layout)
        event, values = window.read()
        

        if event == 'Login':
            #check if all are filled
            if values[0] == '' or values[1] == '':
                if configparser_.get('user', 'token') != '':
                    response = {'token': configparser_.get('user', 'token')}
                    hcAPI.set_token(response['token'])
                    window.close()
                    return response
                # make a popup
                else:
                    sg.popup('Please fill all the fields up')
                    window.close()
                    login_window()
            else:
                token = hcAPI.User.login(values[0], values[1])
                if token['code'] == 401:
                    sg.popup('Invalid credentials')
                    window.close()
                    login_window()
                else:
                    if values[2] == True:
                        configparser_.set('user', 'token', token['token'])
                        configparser_.write(open('config.ini', 'w'))
                    window.close()
                    return token

if __name__ == '__main__':
    git.refresh()
    version = get_local_version()
    #This is a chat client
    #login data needed : username or mail, password
    #chat data needed : message
    # azure theme
    # white background
    sg.theme_background_color('white')
    sg.theme_text_color('black')
    sg.theme_button_color('black')
    sg.theme_element_background_color('white')
    sg.theme_element_text_color('black')
    sg.theme_input_background_color('white')
    # if get_version contains version, then the client is up to date
    if get_version().startswith(version):
        pass
    else:
        
        layout = [[sg.Text('Your version is outdated, please update to the latest version.')],
                   [sg.Text('When you click update, the program will stash changes and pull the latest version.')],
                 [sg.Text('IMPORTANT NOTE: INSTALL GIT IF YOU HAVE NOT INSTALLED IT ALREADY')],
                    [sg.Button('Update'),sg.Button('Download Git'), sg.Button('Ignore')]]
        window = sg.Window('Update LubChat', layout)
        event, values = window.read()
        if event == 'Update':
            #git stash
            git.Git('./').stash()
            #git pull
            git.Git('./').pull()
            window.close()
            exit()
        elif event == 'Download Git':
            import webbrowser
            webbrowser.open('https://gitforwindows.org/')
            window.close()
            exit()
        else:
            window.close()
    if configparser_.get('server', 'url') == '':
        layout = [[sg.Text('Enter the server URI')],
                [sg.InputText(key='url'), sg.Checkbox('Official server', key= "off")],
                [sg.Button('Register'), sg.Button('Login'), sg.Button('Cancel')],
                [sg.Checkbox('Remember me', key='remember')]]
        window = sg.Window('Server Settings', layout)
        event, values = window.read()
        url = values['url']
        
        hcAPI.set_url(url)
        window.close()
        if event == 'Register':
            #register window
            if values['off'] == True:
                url = 'https://hcapi.cubesoftware.xyz/'
            if values['remember'] == True:
                configparser_.set('server', 'url', url)
                configparser_.write(open('config.ini', 'w'))
            hcAPI.set_url(url)
            response = register_window()
            print(response)
            token = None
        elif event == 'Login':
            #login window
            if values['off'] == True:
                url = 'https://hcapi.cubesoftware.xyz/'
            if values['remember'] == True:
                configparser_.set('server', 'url', url)
                configparser_.write(open('config.ini', 'w'))
            hcAPI.set_url(url)
            response = login_window()
            token = response['token']
        elif event == 'Cancel':
            #quit the program
            exit()
    else:
        hcAPI.set_url(configparser_.get('server', 'url'))
        response = login_window()
        token = response['token']
    if configparser_.get('user', 'token') == '' :
        token = login_window()['token']


    
    
    #make a window for chat
    if token == None:
        exit()
    #if user is admin 
#    #Example response of get_user_info
#    {
#    "id": 1,
#    "name": "test",
#    "password": null,
#    "public_id": null,
#    "rankid": 3
#}
    userss = hcAPI.User.get_user_info()
    rankid = None
    try:
        rankid = userss['rankid']
    except KeyError:
        print("Server stopped or restarting; please restart the program and relog.")
        exit()

    if rankid == 1:
        layout = [
                    [sg.Multiline(size=(30, 10), key='-OUTPUT-')],
                    [sg.InputText(key='-INPUT-')],
                    [sg.Button('Send') , sg.Button('Logout'), sg.Button('Remove Message'), sg.Button('Grant Permission'), sg.Button('Revoke Permission')]]
        
        window = sg.Window('LubChat - Admin Chat', layout)
        event, values = window.read()
        refresh_loop()
        while True:
            #refresh the chat
            event, values = window.read(timeout=100,timeout_key='timeout')

            # Change -OUTPUT- to the new text
        
            #send a message
            if event == 'timeout':
                window['-OUTPUT-'].update(texte)
            if event == 'Send':
                hcAPI.Message.send_message(values['-INPUT-'])
            #logout
            elif event == 'Logout':
                hcAPI.User.logout()
                exit()
            #remove a message
            elif event == 'Remove Message':
                hcAPI.Message.delete_message(values['-INPUT-'])
            #read the message
            elif event == 'Grant Permission':
                #make a popup for the user to choose the user
                layout = [[sg.Text('Choose user')],
                            [sg.InputText(key='user')],
                            [sg.DropDown(['Admin','Moderator','User'], key='type')],
                            [sg.Button('Grant'), sg.Button('Cancel')]]
                popup = sg.Window('Grant Permission', layout)
                event, values = window.read()
                popup.close()
                if event == 'Grant':
                    #Rank id's
                    #1 - Admin
                    #2 - Moderator
                    #3 - User
                    rankid = 0
                    if values['type'] == 'Admin':
                        rankid = 1
                    elif values['type'] == 'Moderator':
                        rankid = 2
                    elif values['type'] == 'User':
                        rankid = 3
                    hcAPI.User.grant_permission(values['user'], rankid)
            elif event == 'Revoke Permission':
                #make a popup for the user to choose the user
                layout = [[sg.Text('Choose the user')],
                            [sg.InputText(key='user')],
                            [sg.Button('Revoke'), sg.Button('Cancel')]]
                popup = sg.Window('Revoke Permission', layout)
                event, values = window.read()
                popup.close()
                if event == 'Revoke':
                    user = hcAPI.User.get_user_by_name(values['user'])
                    print(user)
                    hcAPI.User.revoke_permission(user['id'])
            
    else:
        layout = [
                    [sg.Multiline(size=(70, 10), key='-OUTPUT-')],
                    [sg.InputText(key='-INPUT-', size=(70, 1))],
                    #center the button
                    [sg.Button('Send', size=(10, 1), pad=((200, 0), (0, 0)))]]

            #what will be the size of this layout
            #respone: {'width': '600', 'height': '400'}
        window = sg.Window('LubChat - Chat', layout)
        refresh_loop()
        while True:
            #refresh the chat
            event, values = window.read(timeout=100, timeout_key='timeout')

            #send a message
            if event == 'timeout':
                window['-OUTPUT-'].update(texte)

            elif event == 'Send':
                hcAPI.Message.send_message(values['-INPUT-'])
                window['-INPUT-'].update('')
            #logout
            elif event == 'Logout':
                exit()
                #if user clicks exit button
            elif event == sg.WIN_CLOSED:
                exit()
        
    
        
        


        
        

            

            
                

    
