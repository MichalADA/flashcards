from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from menu import MenuScreen
from flashcards import FlashcardApp
from learned_flashcards import LearnedFlashcardsScreen

class FlashcardScreen(Screen):
    def __init__(self, **kwargs):
        super(FlashcardScreen, self).__init__(**kwargs)
        self.name = 'flashcards'
        # self.add_widget(FlashcardApp(manager=self.manager)) działa apka
        self.app = None
    def on_enter(self):
        if not self.app:
            self.app = FlashcardApp(manager=self.manager)  # Przekazanie manager
            self.add_widget(self.app)    



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

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Menu(manager=sm, name='menu'))
        sm.add_widget(FlashcardScreen(name='flashcards'))  
        sm.add_widget(LearnedFlashcardsScreenWrapper(manager=sm, name='learned_flashcards'))
        return sm



if __name__ == "__main__":
    MainApp().run()
