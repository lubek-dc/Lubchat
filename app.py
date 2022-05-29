# hello_world.py

import PySimpleGUI as sg
import requests
import json
from HackChat import app as hcAPI

global url
#sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()

def register_window():
    #layout: username, email, password, confirm password
        layout = [[sg.Text('Username', size=(15, 1)) , sg.InputText()],
                    [sg.Text('Password', size=(15, 1)), sg.InputText()],
                    [sg.Text('Confirm Password', size=(15, 1)), sg.InputText()],
                    [sg.Button('Register'), sg.Button('Cancel')]]
                    
        window = sg.Window('HackChat - Register', layout)
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
                hcAPI.User.register(values[0], values[1])
                window.close()
                sg.popup('You have been registered')
                login_window()

def login_window():
    #layout: username, password
        layout = [[sg.Text('Username', size=(15, 1)) , sg.InputText()],
                    [sg.Text('Password', size=(15, 1)), sg.InputText()],
                    [sg.Button('Login'), sg.Button('Cancel')],
                    [sg.Text('', size=(15, 1), key='-OUTPUT-')]]
                    
        window = sg.Window('HackChat - Login', layout)
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
    sg.theme('DarkAmber')
    # make a window for setting url
    layout = [[sg.Text('Enter the url of the server')],
                [sg.InputText(key='url')],
                [sg.Button('Register'), sg.Button('Login'), sg.Button('Cancel')]]
    window = sg.Window('Server Settings', layout)
    event, values = window.read()
    url = values['url']
    window.close()
    if event == 'Register':
        #register window
        hcAPI.Settings.set_url(url)
        
        token = register_window()['token']
    elif event == 'Login':
        #login window
        hcAPI.Settings.set_url(url)
        token = login_window()['token']
    if event == 'Cancel':
        #quit the program
        exit()
    #make a window for chat
    hcAPI.Settings.set_token(token)
    layout = [[sg.Text('Chat')],
                [sg.Button('Refresh'), sg.Button('Send'), sg.Button('Logout')],
                [sg.Multiline(size=(30, 10), key='-OUTPUT-')],
                [sg.InputText(key='-INPUT-')]]
    window = sg.Window('Chat', layout)
    event, values = window.read()
    while True:
        #refresh the chat
        if event == 'Refresh': # example response: [[{'author': 'Lubekd', 'id': 1, 'message': 'Hello'}], 200]
            messages = hcAPI.Message.get_last_messages()
            output = ''
            for message in messages[0]:
                output += message['author'] + ': ' + message['message'] + '\n'
            window['-OUTPUT-'].update(output)
            event, values = window.read()

        #send a message
        elif event == 'Send':
            hcAPI.Message.send_message(values['-INPUT-'])
        #logout
        elif event == 'Logout':
            hcAPI.User.logout()
            exit()
        #read the message
        event, values = window.read()
        
        


        
        

            

            
                

    