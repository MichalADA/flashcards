from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from menu import MenuScreen
from flashcards import FlashcardApp


class FlashcardScreen(Screen):
    def __init__(self, **kwargs):
        super(FlashcardScreen, self).__init__(**kwargs)
        self.name = 'flashcards'
        self.add_widget(FlashcardApp())


class Menu(Screen):
    def __init__(self, manager, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.name = 'menu'
        self.add_widget(MenuScreen(manager=manager))


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Menu(manager=sm, name='menu'))
        sm.add_widget(FlashcardScreen(name='flashcards'))
        return sm


if __name__ == "__main__":
    MainApp().run()
