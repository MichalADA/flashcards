from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from menu import MenuScreen
from flashcards import FlashcardApp
from learned_flashcards import LearnedFlashcardsScreen
from login_screen import LoginScreen
from register_screen import RegisterScreen
from grama import GrammarScreen
from listening import ListeningScreen  # Dodaj ten import


class FlashcardScreen(Screen):
    def __init__(self, manager, **kwargs):
        super(FlashcardScreen, self).__init__(**kwargs)
        self.name = 'flashcards'
        self.add_widget(FlashcardApp(manager=manager))


class LearnedFlashcardsScreenWrapper(Screen):
    def __init__(self, manager, **kwargs):
        super(LearnedFlashcardsScreenWrapper, self).__init__(**kwargs)
        self.name = 'learned_flashcards'
        self.add_widget(LearnedFlashcardsScreen(manager=manager))


class Menu(Screen):
    def __init__(self, manager, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.name = 'menu'
        self.add_widget(MenuScreen(manager=manager))


class LoginScreenWrapper(Screen):
    def __init__(self, manager, **kwargs):
        super(LoginScreenWrapper, self).__init__(**kwargs)
        self.name = 'login'
        self.add_widget(LoginScreen(manager=manager))


class RegisterScreenWrapper(Screen):
    def __init__(self, manager, **kwargs):
        super(RegisterScreenWrapper, self).__init__(**kwargs)
        self.name = 'register'
        self.add_widget(RegisterScreen(manager=manager))


class GrammarScreenWrapper(Screen):
    def __init__(self, manager, **kwargs):
        super(GrammarScreenWrapper, self).__init__(**kwargs)
        self.name = 'grammar'
        self.add_widget(GrammarScreen(manager=manager))


class ListeningScreenWrapper(Screen):  # Dodaj tę klasę
    def __init__(self, manager, **kwargs):
        super(ListeningScreenWrapper, self).__init__(**kwargs)
        self.name = 'listening'
        self.add_widget(ListeningScreen(manager=manager))


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreenWrapper(manager=sm, name='login'))
        sm.add_widget(RegisterScreenWrapper(manager=sm, name='register'))
        sm.add_widget(Menu(manager=sm, name='menu'))
        sm.add_widget(FlashcardScreen(manager=sm, name='flashcards'))
        sm.add_widget(LearnedFlashcardsScreenWrapper(manager=sm, name='learned_flashcards'))
        sm.add_widget(GrammarScreenWrapper(manager=sm, name='grammar'))
        sm.add_widget(ListeningScreenWrapper(manager=sm, name='listening'))  # Dodaj tę linię
        return sm


if __name__ == "__main__":
    MainApp().run()