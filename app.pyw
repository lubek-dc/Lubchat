# hello_world.py

from urllib import response
import PySimpleGUI as sg
import requests
import json
from HackChat import app as hcAPI
import threading
#sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()

def refresh_loop():
    threading.Timer(3, refresh_loop).start()
    messages = hcAPI.Message.get_last_messages()
    output = ''
    for message in messages['messages']:
        output += message['author'] + ': ' + message['message'] + '\n'
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
                sg.popup('Please fill all the fields up')
                window.close()
                register_window()
                
            #check if password and confirm password are the same
            elif values[1] != values[2]:
                sg.popup('Password and confirm password are not the same')
                window.close()
                register_window()
            else:
                data = hcAPI.User.register(values[0], values[1])
                print(data)
                window.close()
                sg.popup('You have been registered')
                exit()

def login_window():
    #layout: username, password
        layout = [[sg.Text('Username', size=(15, 1)) , sg.InputText()],
                    [sg.Text('Password', size=(15, 1)), sg.InputText()],
                    [sg.Button('Login'), sg.Button('Cancel')],
                    [sg.Text('', size=(15, 1), key='-OUTPUT-')]]
                    
        window = sg.Window('LubChat - Login', layout)
        event, values = window.read()
        if event == 'Login':
            #check if all are filled
            if values[0] == '' or values[1] == '':
                # make a popup
                sg.popup('Please fill all the fields up')
                window.close()
                login_window()
            else:
                token = hcAPI.User.login(values[0], values[1])
                if token['code'] == 401:
                    sg.popup('Wrong username or password')
                    window.close()
                    login_window()
                else:
                    window.close()
                    return token

if __name__ == '__main__':
    #This is a chat client
    #login data needed : username or mail, password
    #chat data needed : message
    # azure theme
    sg.theme('DarkAmber')
    # make a window for setting url
    layout = [[sg.Text('Enter the url of the server')],
                [sg.InputText(key='url')],
                [sg.Button('Register'), sg.Button('Login'), sg.Button('Cancel')]]
    window = sg.Window('Server Settings', layout)
    event, values = window.read()
    url = values['url']
    hcAPI.set_url(url)
    window.close()
    if event == 'Register':
        #register window
        hcAPI.set_url(url)
        response = register_window()
        print(response)
        token = None
    elif event == 'Login':
        #login window
        hcAPI.set_url(url)
        response = login_window()
        token = response['token']
    if event == 'Cancel':
        #quit the program
        exit()
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
    if userss['rankid'] == 1:
        layout = [[sg.Text('Admin Chat')],
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
                layout = [[sg.Text('Choose the user')],
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
        layout = [[sg.Text('Chat')],
                    [sg.Multiline(size=(30, 10), key='-OUTPUT-')],
                    [sg.InputText(key='-INPUT-')],
                    [sg.Button('Send') , sg.Button('Logout')]]
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
            #logout
            elif event == 'Logout':
                exit()
                #if user clicks exit button
            elif event == sg.WIN_CLOSED:
                exit()
        
    
        
        


        
        

            

            
                

    