from base_screen import BaseScreen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from db import MongoDB

class FlashcardBox(BoxLayout):
    def __init__(self, german_text, polish_text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(120)
        self.padding = [dp(20), dp(10)]
        self.spacing = dp(10)
        
        # Tło karty
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Jasne tło
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Niemieckie słowo
        self.add_widget(Label(
            text=german_text,
            font_size=dp(24),
            color=[0, 0, 0, 1],  # Czarny
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))
        
        # Polskie słowo
        self.add_widget(Label(
            text=polish_text,
            font_size=dp(20),
            color=[0.3, 0.3, 0.3, 1],  # Ciemny szary
            size_hint_y=None,
            height=dp(40)
        ))

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class LearnedFlashcardsScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.db = MongoDB()

        # Główny kontener
        main_container = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(20)
        )

        # Przycisk powrotu
        back_button = self.create_button(
            text="Powrót do menu",
            color=[0.2, 0.6, 0.9, 1]
        )
        back_button.bind(on_press=self.go_back_to_menu)
        main_container.add_widget(back_button)

        # Kontener na listę fiszek
        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False
        )

        # Grid na fiszki
        grid = GridLayout(
            cols=1,
            spacing=dp(20),
            size_hint_y=None,
            padding=[0, dp(10)]
        )
        grid.bind(minimum_height=grid.setter('height'))

        # Pobranie nauczonych fiszek
        learned_flashcards = self.db.get_learned_flashcards()

        if learned_flashcards:
            for flashcard in learned_flashcards:
                card = FlashcardBox(
                    german_text=flashcard['german'],
                    polish_text=flashcard['polish']
                )
                grid.add_widget(card)
        else:
            no_cards_label = Label(
                text="Brak nauczonych fiszek.",
                font_size=dp(20),
                color=[1, 1, 1, 1],
                size_hint_y=None,
                height=dp(60)
            )
            grid.add_widget(no_cards_label)

        scroll_view.add_widget(grid)
        main_container.add_widget(scroll_view)
        self.add_widget(main_container)

    def go_back_to_menu(self, instance):
        self.manager.current = 'menu'