
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from db import MongoDB
from screen_config import SCREEN_CONFIG

class ScreenWrapper(Screen):
    """Podstawowa klasa wrappera dla ekranów"""
    def __init__(self, manager, screen_class, name, db_instance=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        
        # Tworzenie instancji ekranu z odpowiednimi parametrami
        screen_params = {'manager': manager}
        if db_instance and SCREEN_CONFIG[name].get('requires_db'):
            screen_params['db_instance'] = db_instance
            
        self.screen = screen_class(**screen_params)
        self.add_widget(self.screen)

class MainApp(App):
    def build(self):
        """Tworzy główną aplikację i ustawia ScreenManager"""
        self.db = MongoDB()
        sm = ScreenManager()
        screens = {}

        # Tworzenie wszystkich ekranów na podstawie konfiguracji
        for screen_id, config in SCREEN_CONFIG.items():
            screen = ScreenWrapper(
                manager=sm,
                screen_class=config['class'],
                name=config['name'],
                db_instance=self.db
            )
            screens[screen_id] = screen
            sm.add_widget(screen)

        # Dodatkowa konfiguracja dla ekranu logowania (powiązanie z menu)
        if 'login' in screens and 'menu' in screens:
            login_screen = screens['login'].screen
            menu_screen = screens['menu'].screen
            if hasattr(login_screen, 'menu_screen'):
                login_screen.menu_screen = menu_screen

        return sm

if __name__ == "__main__":
    MainApp().run()

