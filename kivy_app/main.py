'''
GUI Should be done in .kv and use Py for Logic;

KIVY houses the GUI similar to tkinker
FOR every screen - there is a >>> class ScreenName(Screen):
    all action occurring in and from that Screen will be in that Class
'''
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from datetime import datetime
import glob
from pathlib import Path
import random
from happy_app.hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


Builder.load_file('design.kv')

class LoginScreen(Screen):
    def log_in(self):
        self.manager.current = "login_screen"

    def sign_up(self):
        self.manager.current = "sign_up_screen"
    def home_screen(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "home_screen"
            self.manager.transition.direction = "left"
        else:
            self.ids.incorrect.text = "Incorrect Username or Password"


class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open('users.json') as file:
            users = json.load(file)

        users[uname] = {'username': uname,
                        'password': pword,
                        'created': datetime.now().strftime('%Y-%m-%d %H-%M-%S')}

        with open('users.json', 'w') as file:
            json.dump(users, file)
        print(users)
        self.manager.current = "sign_up_success"

class SignUpSuccess(Screen):
    def log_in(self):
        self.manager.current = "login_screen"

class HomeScreen(Screen):
    def log_out(self):
        self.manager.current = "login_screen"
        self.manager.transition.direction = "right"

    def get_quote(self, quote):
        quote = quote.lower()
        avail_quotes = glob.glob('data/*.txt')
        avail_quotes = [Path(filename).stem for filename in avail_quotes]

        if quote in avail_quotes:
            with open(f"data/{quote}.txt", encoding="utf8") as file:
                topic = file.readlines()
            self.ids.topic.text = random.choice(topic)
        else:
            self.ids.topic.text = "Try Another One"

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

class ImageButton(HoverBehavior, Image, ButtonBehavior):
    pass

if __name__ == "__main__":
    MainApp().run()