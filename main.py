from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from db_manager import UserData
from pass_gen import PassGen
from enum import Enum
from auth import AppAuth
from exeptions import *

#Builder.load_file("./lab.kv") #раскомментировать при билде

class ScrnType(Enum):
    START_SCREEN = 0
    LAB1_SCREEN = 1
    LAB2_SCREEN = 2
    LAB2_LOGIN = 3
    LAB2_REGISTRATION = 4
    LAB2_MAIN = 5
    LAB2_CHANGE = 6
    LAB3_SCREEN = 7


class StartScreen(BoxLayout):
    @staticmethod
    def on_lab1button_release():
        screens_manager.switch_screen(ScrnType.LAB1_SCREEN)

    @staticmethod
    def on_lab2button_release():
        screens_manager.switch_screen(ScrnType.LAB2_SCREEN)


class LabScreenWidget(BoxLayout):
    @staticmethod
    def on_back_button_release():
        screens_manager.switch_screen(ScrnType.START_SCREEN)


class Lab1Screen(LabScreenWidget):
    @staticmethod
    def get_pass(ind: str):
        return PassGen.get_rand_pass_12_var(ind)


class Lab2Screen(LabScreenWidget):
    @staticmethod
    def on_registration_button_release():
        screens_manager.switch_screen(ScrnType.LAB2_REGISTRATION)

    @staticmethod
    def on_login_button_release():
        screens_manager.switch_screen(ScrnType.LAB2_LOGIN)


class ErrorPopup(Popup):
    message = StringProperty()


class MessagePopup(Popup):
    message = StringProperty()


class Lab2Login(BoxLayout):
    @staticmethod
    def on_login_button_release(login: str, password: str):
        if app_auth.try_login(login, password):
            screens_manager.reset_screen(ScrnType.LAB2_MAIN)
            screens_manager.switch_screen(ScrnType.LAB2_MAIN).start_video()
            app_auth.current_login = login

        else:
            ErrorPopup(message="Неверный логин или пароль").open()

    @staticmethod
    def on_back_button_release():
        screens_manager.switch_screen(ScrnType.LAB2_SCREEN)


class Lab2Registration(BoxLayout):
    def on_register_button_release(self):
        ids = self.ids
        try:
            app_auth.try_register(username=ids.username_textbox.text,
                                  password=ids.password_textbox.text,
                                  lastname=ids.lastname_textbox.text,
                                  name=ids.name_textbox.text,
                                  patronymic=ids.patronymic_textbox.text,
                                  birthday=ids.birthday_textbox.text,
                                  place_of_birth=ids.place_of_birth_textbox.text,
                                  phone_number=ids.phone_number_textbox.text)
            MessagePopup(message="Вы успешно зарегистрировались!").open()
            screens_manager.switch_screen(ScrnType.LAB2_LOGIN)
        except RegistrationException as exception:
            ErrorPopup(message=str(exception)).open()

    @staticmethod
    def on_back_button_release():
        screens_manager.switch_screen(ScrnType.LAB2_SCREEN)


class Lab2Change(BoxLayout):
    def set_user_data(self):
        user_data = app_auth.get_logged_data()
        ids = self.ids
        ids.lastname_textbox.text = user_data.lastname
        ids.name_textbox.text = user_data.name
        ids.patronymic_textbox.text = user_data.patronymic
        ids.birthday_textbox.text = user_data.birthday
        ids.place_of_birth_textbox.text = user_data.place_of_birth
        ids.phone_number_textbox.text = user_data.phone_number

    @staticmethod
    def on_back_button_release():
        screens_manager.switch_screen(ScrnType.LAB2_MAIN).start_video()

    def on_change_button_release(self):
        ids = self.ids
        try:
            app_auth.try_change_userdata(password=ids.password_textbox.text,
                                         lastname=ids.lastname_textbox.text,
                                         name=ids.name_textbox.text,
                                         patronymic=ids.patronymic_textbox.text,
                                         birthday=ids.birthday_textbox.text,
                                         place_of_birth=ids.place_of_birth_textbox.text,
                                         phone_number=ids.phone_number_textbox.text)
            MessagePopup(message="Вы успешно изменили данные").open()
            screens_manager.switch_screen(ScrnType.LAB2_MAIN).start_video()
        except RegistrationException as exception:
            ErrorPopup(message=str(exception)).open()


class Lab2Main(BoxLayout):
    def start_video(self):
        self.ids.video.state = "play"

    def stop_video(self):
        self.ids.video.state = "pause"

    def on_logout_button_release(self):
        self.stop_video()
        screens_manager.switch_screen(ScrnType.LAB2_LOGIN)

    def on_change_button_release(self):
        self.stop_video()
        screens_manager.switch_screen(ScrnType.LAB2_CHANGE).set_user_data()


class ScreensManager(BoxLayout):
    def __init__(self, **kwargs):
        super(ScreensManager, self).__init__(**kwargs)
        self.screens = dict()
        self.screens[ScrnType.START_SCREEN] = StartScreen()
        self.screens[ScrnType.LAB1_SCREEN] = Lab1Screen()
        self.screens[ScrnType.LAB2_SCREEN] = Lab2Screen()
        self.screens[ScrnType.LAB2_LOGIN] = Lab2Login()
        self.screens[ScrnType.LAB2_REGISTRATION] = Lab2Registration()
        self.screens[ScrnType.LAB2_MAIN] = Lab2Main()
        self.screens[ScrnType.LAB2_CHANGE] = Lab2Change()
        # ...
        self.add_widget(self.screens[ScrnType.START_SCREEN])

    def switch_screen(self, screen_type: ScrnType):
        self.clear_widgets()
        self.add_widget(self.screens[screen_type])
        return self.screens[screen_type]

    def reset_screen(self, screen_type: ScrnType):
        self.screens[screen_type] = type(self.screens[screen_type])()
        return self.screens[screen_type]


class LabApp(App):
    def build(self):
        global screens_manager
        screens_manager = ScreensManager(orientation='vertical')
        return screens_manager


if __name__ == '__main__':
    app_auth = AppAuth()
    screens_manager = ScreensManager()
    LabApp().run()
