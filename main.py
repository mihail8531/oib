from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from pass_gen import PassGen


class LabWidget(BoxLayout):

    @staticmethod
    def get_pass(ind: str):
        return PassGen.get_rand_pass_12_var(ind)


class LabApp(App):
    def build(self):
        return LabWidget()

if __name__ == '__main__':
    LabApp().run()
