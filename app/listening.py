from base_screen import BaseScreen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.metrics import dp
from menu import MenuButton
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.core.audio import SoundLoader
import base64
import os

class ListeningScreen(BaseScreen):
    def __init__(self, manager, db_instance, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.db = db_instance
        self.current_audio = None
        
        # Dodaj tytuł
        self.add_widget(self.create_title("Ćwiczenia ze słuchania"))
        
        # Główny kontener
        main_container = GridLayout(
            cols=1,
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None
        )
        main_container.bind(minimum_height=main_container.setter('height'))
        
        # Kategorie słuchanek - tylko Dialogi i Wymowa
        categories_container = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(200)
        )
        
        # Przyciski kategorii - zredukowane do dwóch
        listening_categories = [
            ("Dialogi", [0.5, 0.2, 0.8, 1]),
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
        
        self.controls = [
            ("▶️ Play", [0.2, 0.7, 0.3, 1]),
            ("⏸️ Pause", [0.9, 0.6, 0.2, 1]),
            ("⏹️ Stop", [0.9, 0.2, 0.2, 1])
        ]
        
        # Dodaj obsługę kontrolek
        for text, color in self.controls:
            btn = MenuButton(
                text=text,
                color=color
            )
            if text == "▶️ Play":
                btn.bind(on_release=self.play_audio)
            elif text == "⏸️ Pause":
                btn.bind(on_release=self.pause_audio)
            elif text == "⏹️ Stop":
                btn.bind(on_release=self.stop_audio)
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
        self.volume_slider.bind(value=self.on_volume_change)
        
        volume_container.add_widget(volume_label)
        volume_container.add_widget(self.volume_slider)
        main_container.add_widget(volume_container)
        
        # Dodaj scroll dla głównego kontenera
        main_scroll = ScrollView(size_hint=(1, 1))
        main_scroll.add_widget(main_container)
        self.add_widget(main_scroll)
        
        # Przycisk powrotu
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
        
        if category == "Wymowa":
            # Pobierz pliki wymowy z bazy
            pronunciations = self.db.get_pronunciations()
            
            for pronunciation in pronunciations:
                btn = MenuButton(
                    text=pronunciation['german'],
                    color=[0.3, 0.5, 0.8, 1],
                    size_hint_y=None,
                    height=dp(50)
                )
                btn.bind(on_release=lambda x, p=pronunciation: self.play_pronunciation(p))
                self.exercises_container.add_widget(btn)
                
        elif category == "Dialogi":
            # Pobierz dialogi z bazy
            dialogs = self.db.get_dialogs()
            
            for dialog in dialogs:
                dialog_btn = MenuButton(
                    text=dialog['german'],
                    color=[0.3, 0.5, 0.8, 1],
                    size_hint_y=None,
                    height=dp(50)
                )
                dialog_btn.bind(on_release=lambda x, d=dialog: self.play_pronunciation(d))
                self.exercises_container.add_widget(dialog_btn)

    def play_pronunciation(self, pronunciation_data):
        """Odtwarza wymowę od razu po kliknięciu"""
        if self.current_audio:
            self.current_audio.stop()
            
        # Zapisz audio do tymczasowego pliku
        temp_file = 'temp_audio.mp3'
        with open(temp_file, 'wb') as f:
            f.write(base64.b64decode(pronunciation_data['audio_data']))
            
        self.current_audio = SoundLoader.load(temp_file)
        if self.current_audio:
            self.current_audio.volume = self.volume_slider.value / 100
            self.current_audio.play()  # Odtwórz od razu

    def play_audio(self, instance):
        if self.current_audio:
            self.current_audio.play()

    def pause_audio(self, instance):
        if self.current_audio:
            self.current_audio.stop()

    def stop_audio(self, instance):
        if self.current_audio:
            self.current_audio.stop()
            self.current_audio.seek(0)

    def on_volume_change(self, instance, value):
        if self.current_audio:
            self.current_audio.volume = value / 100

    def on_leave(self):
        if self.current_audio:
            self.current_audio.stop()
        if os.path.exists('temp_audio.mp3'):
            os.remove('temp_audio.mp3')