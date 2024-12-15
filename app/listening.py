from base_screen import BaseScreen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.metrics import dp
from menu import MenuButton
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider

class ListeningScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        
        # Dodaj tytuł
        self.add_widget(self.create_title("Ćwiczenia ze słuchania"))
        
        # Główny kontener na całą zawartość
        main_container = GridLayout(
            cols=1,
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None
        )
        main_container.bind(minimum_height=main_container.setter('height'))
        
        # Kategorie słuchanek
        categories_container = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(200)
        )
        
        # Przyciski kategorii
        listening_categories = [
            ("Dialogi", [0.5, 0.2, 0.8, 1]),
            ("Słownictwo", [0.3, 0.6, 0.9, 1]),
            ("Gramatyka", [0.2, 0.7, 0.3, 1]),
            ("Wymowa", [0.9, 0.4, 0.2, 1])
        ]
        
        for text, color in listening_categories:
            btn = MenuButton(
                text=text,
                color=color
            )
            btn.bind(on_release=lambda x, t=text: self.show_listening_exercises(t))
            categories_container.add_widget(btn)
            
        main_container.add_widget(categories_container)
        
        # Kontener na ćwiczenia
        exercises_scroll = ScrollView(
            size_hint_y=None,
            height=dp(200)
        )
        self.exercises_container = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None,
            padding=dp(10)
        )
        self.exercises_container.bind(minimum_height=self.exercises_container.setter('height'))
        exercises_scroll.add_widget(self.exercises_container)
        main_container.add_widget(exercises_scroll)
        
        # Przyciski kontrolne
        controls_container = GridLayout(
            cols=3,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        controls = [
            ("▶️ Play", [0.2, 0.7, 0.3, 1]),
            ("⏸️ Pause", [0.9, 0.6, 0.2, 1]),
            ("⏹️ Stop", [0.9, 0.2, 0.2, 1])
        ]
        
        for text, color in controls:
            btn = MenuButton(
                text=text,
                color=color
            )
            controls_container.add_widget(btn)
            
        main_container.add_widget(controls_container)
        
        # Pasek postępu
        self.progress = ProgressBar(
            max=100,
            size_hint_y=None,
            height=dp(20)
        )
        main_container.add_widget(self.progress)
        
        # Suwak głośności
        volume_container = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        volume_label = Label(
            text="Głośność:",
            size_hint_x=None,
            width=dp(100)
        )
        
        self.volume_slider = Slider(
            min=0,
            max=100,
            value=50,
            size_hint=(None, None),
            size=(dp(200), dp(30))
        )
        
        volume_container.add_widget(volume_label)
        volume_container.add_widget(self.volume_slider)
        main_container.add_widget(volume_container)
        
        # Dodaj scroll dla głównego kontenera
        main_scroll = ScrollView(size_hint=(1, 1))
        main_scroll.add_widget(main_container)
        self.add_widget(main_scroll)
        
        # Przycisk powrotu - zawsze na dole
        back_btn = MenuButton(
            text="Powrót do menu",
            color=[0.5, 0.5, 0.5, 1],
            size_hint_y=None,
            height=dp(50)
        )
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        self.add_widget(back_btn)

    def show_listening_exercises(self, category):
        """Wyświetla ćwiczenia ze słuchania dla wybranej kategorii"""
        self.exercises_container.clear_widgets()
        
        exercises = [
            f"Ćwiczenie 1 - {category}",
            f"Ćwiczenie 2 - {category}",
            f"Ćwiczenie 3 - {category}"
        ]
        
        for exercise in exercises:
            exercise_btn = MenuButton(
                text=exercise,
                color=[0.3, 0.5, 0.8, 1]
            )
            self.exercises_container.add_widget(exercise_btn)