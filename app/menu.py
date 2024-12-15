from base_screen import BaseScreen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from db import MongoDB


class MenuButton(Button):
    def __init__(self, text, color, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.background_normal = ''
        self.background_color = color
        self.font_size = dp(20)
        self.bold = True
        self.padding = [dp(10), dp(10)]
        self.border_radius = [dp(10)]


class MenuScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        
        # Dodanie tytułu
        self.add_widget(self.create_title("Menu Główne"))
        
        # Siatka przycisków
        button_grid = GridLayout(
            cols=2, 
            spacing=dp(20), 
            padding=dp(20),
            size_hint=(1, 0.8)
        )
        
        # Przyciski z odpowiednimi kolorami i funkcjami
        buttons_config = [
            {
                'text': 'Fiszki',
                'color': [0.2, 0.7, 0.3, 1],  # Zielony
                'action': self.go_to_flashcards
            },
            {
                'text': 'Gramatyka',
                'color': [0.3, 0.5, 0.8, 1],  # Niebieski
                'action': self.go_to_grammar
            },
            {
                'text': 'Nauczone fiszki',
                'color': [0.8, 0.5, 0.2, 1],  # Pomarańczowy
                'action': self.go_to_learned_flashcards
            },
            {
                'text': 'Słuchanki',
                'color': [0.5, 0.2, 0.8, 1],  # Fioletowy
                'action': self.go_to_listening
            }
        ]
        
        # Tworzenie przycisków
        for btn_config in buttons_config:
            button = MenuButton(
                text=btn_config['text'],
                color=btn_config['color']
            )
            if btn_config['action']:
                button.bind(on_release=btn_config['action'])
            button_grid.add_widget(button)

        self.add_widget(button_grid)

    def go_to_flashcards(self, instance):
        self.manager.current = 'flashcards'

    def go_to_learned_flashcards(self, instance):
        self.manager.current = 'learned_flashcards'

    def go_to_grammar(self, instance):
        """Przejście do ekranu gramatyki"""
        self.manager.current = 'grammar'
    
    def go_to_listening(self, instance):
        """Przejście do ekranu sluchanek"""
        self.manager.current = 'listening'