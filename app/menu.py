# Import niezbędnych modułów
from base_screen import BaseScreen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.properties import StringProperty
from db import MongoDB

# Klasa definiująca wygląd i zachowanie przycisków w menu
class MenuButton(Button):
    def __init__(self, text, color, **kwargs):
        super().__init__(**kwargs)
        # Ustawienie podstawowych właściwości przycisku
        self.text = text
        self.background_normal = ''
        self.background_color = color
        self.font_size = dp(20)
        self.bold = True
        self.padding = [dp(10), dp(10)]
        self.border_radius = [dp(10)]


# Klasa głównego ekranu menu
class MenuScreen(BaseScreen):
   # Zmienna przechowująca informację o aktualnie zalogowanym użytkowniku
   current_user = StringProperty("")
   
   def __init__(self, manager, **kwargs):
       super().__init__(**kwargs)
       self.manager = manager
       self.db = MongoDB()
       
       # Utworzenie głównego layoutu
       main_layout = GridLayout(cols=1, spacing=dp(10), size_hint=(1, 1))
       
       # Nagłówek z tytułem i danymi użytkownika
       header = GridLayout(cols=2, size_hint=(1, 0.1), spacing=dp(5))
       
       # Lewa strona nagłówka - tytuł
       left_header = GridLayout(cols=1, size_hint=(0.7, 1))
       left_header.add_widget(self.create_title("Menu Główne"))
       
       # Prawa strona nagłówka - informacje o użytkowniku i przycisk wylogowania
       right_header = GridLayout(cols=2, size_hint=(0.3, 1), spacing=dp(5))
       self.user_label = Label(
           text=f"Zalogowany: {self.current_user}",
           size_hint=(0.6, 1),
           font_size=dp(16),
           halign='right'
       )
       
       # Przycisk wylogowania
       logout_button = Button(
           text="Wyloguj",
           size_hint=(0.4, 0.7),
           background_color=[0.5, 0.1, 0.1, 1],  # Czerwony kolor
           color=[1, 1, 1, 1],  # Biały tekst
           font_size=dp(14),
           pos_hint={'center_y': 0.5}
       )
       logout_button.bind(on_release=self.logout)
       
       # Dodanie elementów do prawej strony nagłówka
       right_header.add_widget(self.user_label)
       right_header.add_widget(logout_button)
       
       # Złożenie nagłówka
       header.add_widget(left_header)
       header.add_widget(right_header)
       
       # Powiązanie aktualizacji etykiety użytkownika
       self.bind(current_user=self.update_user_label)
       main_layout.add_widget(header)
       
       # Konfiguracja siatki przycisków menu
       button_grid = GridLayout(
           cols=2, 
           spacing=dp(20), 
           padding=dp(20),
           size_hint=(1, 0.8)
       )
       
       # Konfiguracja przycisków menu - tekst, kolor i akcja po kliknięciu
       buttons_config = [
           {'text': 'Fiszki', 'color': [0.2, 0.7, 0.3, 1], 'action': self.go_to_flashcards},
           {'text': 'Gramatyka', 'color': [0.3, 0.5, 0.8, 1], 'action': self.go_to_grammar},
           {'text': 'Nauczone fiszki', 'color': [0.8, 0.5, 0.2, 1], 'action': self.go_to_learned_flashcards},
           {'text': 'Słuchanki', 'color': [0.5, 0.2, 0.8, 1], 'action': self.go_to_listening}
       ]
       
       # Utworzenie przycisków na podstawie konfiguracji
       for btn_config in buttons_config:
           button = MenuButton(text=btn_config['text'], color=btn_config['color'])
           if btn_config['action']:
               button.bind(on_release=btn_config['action'])
           button_grid.add_widget(button)
           
       main_layout.add_widget(button_grid)
       self.add_widget(main_layout)

   # Metoda aktualizująca etykietę z nazwą użytkownika
   def update_user_label(self, instance, value):
       self.user_label.text = f"Zalogowany: {value}"

   # Metoda obsługująca wylogowanie
   def logout(self, instance):
       self.current_user = ""
       self.manager.current = 'login'

   # Metody nawigacji do poszczególnych ekranów
   def go_to_flashcards(self, instance):
       self.manager.current = 'flashcards'

   def go_to_learned_flashcards(self, instance):
       self.manager.current = 'learned_flashcards'

   def go_to_grammar(self, instance):
       self.manager.current = 'grammar'
   
   def go_to_listening(self, instance):
       self.manager.current = 'listening'