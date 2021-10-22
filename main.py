import re
from math import log, ceil

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
import ffpyplayer
from kivy.uix.textinput import TextInput

from checksum import Checksum
from db_manager import UserData
from pass_gen import PassGen, Alphas
from enum import Enum
from auth import AppAuth
from exeptions import *


# Builder.load_file("./lab.kv") #раскомментировать при билде

class ScrnType(Enum):
    START_SCREEN = 0
    LAB1_SCREEN = 1
    LAB2_SCREEN = 2
    LAB2_LOGIN = 3
    LAB2_REGISTRATION = 4
    LAB2_MAIN = 5
    LAB2_CHANGE = 6
    LAB3_SCREEN = 7
    LAB4_SCREEN = 8


class StartScreen(BoxLayout):
    @staticmethod
    def on_lab1button_release():
        screens_manager.switch_screen(ScrnType.LAB1_SCREEN)

    @staticmethod
    def on_lab2button_release():
        screens_manager.switch_screen(ScrnType.LAB2_SCREEN)

    @staticmethod
    def on_lab3button_release():
        screens_manager.switch_screen(ScrnType.LAB3_SCREEN)

    @staticmethod
    def on_lab4button_release():
        screens_manager.switch_screen(ScrnType.LAB4_SCREEN)


class LabScreenWidget(BoxLayout):
    @staticmethod
    def on_back_button_release():
        screens_manager.switch_screen(ScrnType.START_SCREEN)


class Lab1Screen(LabScreenWidget):
    @staticmethod
    def get_pass(ind: str):
        return PassGen.get_rand_pass_lab1(ind)


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


class Lab3Screen(LabScreenWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alphas = set()

    def update_values(self):
        self.ids.A_textbox.text = str(sum(map(len, self.alphas)))
        try:
            self.ids.S_textbox.text = str(int(int(self.ids.V_textbox.text) * int(self.ids.T_textbox.text) /
                                              float(self.ids.P_textbox.text)))
        except ZeroDivisionError:
            self.ids.S_textbox.text = "inf"
        except ValueError:
            self.ids.S_textbox.text = "inf"

        try:
            self.ids.L_textbox.text = str(ceil(log(int(self.ids.S_textbox.text)) / log(int(self.ids.A_textbox.text))))
        except ValueError:
            self.ids.L_textbox.text = "inf"

    def update_alphas(self):
        self.alphas = set()
        if self.ids.eng_alpha.active:
            self.alphas.add(Alphas.eng_alpha)
        if self.ids.eng_alpha_upper.active:
            self.alphas.add(Alphas.eng_alpha_upper)
        if self.ids.rus_alpha.active:
            self.alphas.add(Alphas.rus_alpha)
        if self.ids.rus_alpha_upper.active:
            self.alphas.add(Alphas.rus_alpha_upper)
        if self.ids.digits.active:
            self.alphas.add(Alphas.digits)
        if self.ids.spec_chars.active:
            self.alphas.add(Alphas.spec_chars)
        self.update_values()

    def on_gen_pass_button_release(self):
        try:
            if self.ids.A_textbox.text == "0":
                raise InvalidAlphasSetException()
        except InvalidAlphasSetException as exception:
            ErrorPopup(message=str(exception)).open()
        else:
            self.ids.password_textbox.text = PassGen.get_rand_pass_lab3(int(self.ids.L_textbox.text), *self.alphas)


class Lab4Screen(LabScreenWidget):
    def on_calc_checksums_button_release(self):
        texts = [self.ids[f"p_textbox_{i + 1}"].text for i in range(4)]
        for i, text in enumerate(texts):
            self.ids[f"c_sum_textbox_{i + 1}"].text = str(Checksum.checksum(texts[i], 255))
            self.ids[f"c_sum_g_textbox_{i + 1}"].text = str(Checksum.checksum_gamma(texts[i], 51, 13, 256, 102, 255))


class IntInput(TextInput):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring: str, from_undo=False):
        s = re.sub(self.pat, '', substring)
        return super(IntInput, self).insert_text(s, from_undo=from_undo)


class FloatInput(TextInput):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring: str, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


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
        self.screens[ScrnType.LAB3_SCREEN] = Lab3Screen()
        self.screens[ScrnType.LAB4_SCREEN] = Lab4Screen()
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
    print(f"ffpyplayer: {ffpyplayer.version}")
    app_auth = AppAuth()
    screens_manager = ScreensManager()
    LabApp().run()
