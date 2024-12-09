from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from menu import MenuScreen
from flashcards import FlashcardApp
from learned_flashcards import LearnedFlashcardsScreen
from login_screen import LoginScreen
from register_screen import RegisterScreen



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



class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreenWrapper(manager=sm, name='login'))
        sm.add_widget(RegisterScreenWrapper(manager=sm, name='register'))  # Dodano ekran rejestracji
        sm.add_widget(Menu(manager=sm, name='menu'))
        sm.add_widget(FlashcardScreen(manager=sm, name='flashcards'))
        sm.add_widget(LearnedFlashcardsScreenWrapper(manager=sm, name='learned_flashcards'))
        return sm


if __name__ == "__main__":
    MainApp().run()
