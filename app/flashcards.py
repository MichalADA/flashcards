from base_screen import BaseScreen
from kivy.uix.label import Label
from kivy.uix.button import Button
from random import choice
from kivy.metrics import dp
from db import MongoDB

class FlashcardApp(BaseScreen):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.db = MongoDB()
        
        # Pobranie fiszek
        self.flashcards = self.db.get_all_flashcards()
        if not self.flashcards:
            self.show_no_flashcards_message()
            return

        self.flashcard = choice(self.flashcards)
        
        # Kontener na kartę
        self.card_container = self.create_container()
        self.card_container.size_hint = (1, 0.6)
        
        # Niemieckie słowo
        self.german_word_label = Label(
            text=self.flashcard["german"],
            font_size=dp(40),
            color=[1, 0.5, 0, 1],
            size_hint=(1, None),
            height=dp(100),
            bold=True
        )
        
        # Polskie słowo
        self.polish_word_label = Label(
            text=self.flashcard["polish"],
            font_size=dp(40),
            color=[1, 0, 0, 1],
            size_hint=(1, None),
            height=dp(100),
            bold=True
        )
        
        # Dodanie niemieckiego słowa jako domyślnego
        self.card_container.add_widget(self.german_word_label)
        self.add_widget(self.card_container)
        
        # Kontener na przyciski
        buttons_container = self.create_container()
        buttons_container.spacing = dp(15)
        
        # Przycisk "Flip card"
        self.flip_button = self.create_button(
            "Flip card",
            [0.2, 0.6, 0.8, 1]
        )
        self.flip_button.bind(on_press=self.flip_card)
        buttons_container.add_widget(self.flip_button)
        
        # Przycisk "Next card"
        self.next_button = self.create_button(
            "Next card",
            [0.8, 0.2, 0.2, 1]
        )
        self.next_button.bind(on_press=self.next_card)
        buttons_container.add_widget(self.next_button)
        
        # Przycisk "Umiem"
        self.know_button = self.create_button(
            "Umiem",
            [0.2, 0.8, 0.2, 1]
        )
        self.know_button.bind(on_press=self.know_card)
        buttons_container.add_widget(self.know_button)
        
        # Przycisk powrotu
        self.back_button = self.create_button(
            "Powrót do menu",
            [0.2, 0.5, 0.8, 1]
        )
        self.back_button.bind(on_press=self.go_back_to_menu)
        buttons_container.add_widget(self.back_button)
        
        self.add_widget(buttons_container)

    def show_no_flashcards_message(self):
        self.clear_widgets()
        no_cards_label = Label(
            text="Brak fiszek w bazie danych.",
            font_size=dp(20),
            color=[1, 0, 0, 1]
        )
        self.add_widget(no_cards_label)
        
        # Dodaj przycisk powrotu
        back_button = self.create_button(
            "Powrót do menu",
            [0.2, 0.5, 0.8, 1]
        )
        back_button.bind(on_press=self.go_back_to_menu)
        self.add_widget(back_button)

    def flip_card(self, instance):
        self.card_container.clear_widgets()
        if hasattr(self, 'current_side') and self.current_side == 'german':
            self.card_container.add_widget(self.polish_word_label)
            self.current_side = 'polish'
        else:
            self.card_container.add_widget(self.german_word_label)
            self.current_side = 'german'

    def next_card(self, instance):
        if self.flashcards:
            self.flashcard = choice(self.flashcards)
            self.german_word_label.text = self.flashcard["german"]
            self.polish_word_label.text = self.flashcard["polish"]
            # Pokaż niemiecką stronę
            self.card_container.clear_widgets()
            self.card_container.add_widget(self.german_word_label)
            self.current_side = 'german'

    def know_card(self, instance):
        if self.flashcards:
            self.db.add_to_learned(self.flashcard)
            self.db.delete_flashcard(self.flashcard["german"])
            self.flashcards = self.db.get_all_flashcards()
            
            if not self.flashcards:
                self.show_no_flashcards_message()
            else:
                self.next_card(instance)

    def go_back_to_menu(self, instance):
        self.manager.current = 'menu'