from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from random import choice
from db import MongoDB

class FlashcardApp(BoxLayout):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager  # Menedżer ekranów do obsługi nawigacji
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = [20, 20, 20, 20]  # Odstępy (lewy, góra, prawy, dół)
        
        self.db = MongoDB()
        self.flashcards = self.db.get_all_flashcards()
        if not self.flashcards:
            self.show_no_flashcards_message()
            return

        self.flashcard = choice(self.flashcards)

        # Dodanie etykiety z niemieckim słowem
        self.german_word_label = Label(
            text=self.flashcard["german"],
            font_size='30sp',
            color=[1, 1, 0, 1],
            halign="center",
            size_hint=(1, 0.6)
        )
        self.add_widget(self.german_word_label)

        # Etykieta na polskie słowo (początkowo niewidoczna)
        self.polish_word_label = Label(
            text=self.flashcard["polish"],
            font_size='30sp',
            color=[1, 0, 0, 1],
            halign="center",
            size_hint=(1, 0.6)
        )

        # Przycisk "Flip card"
        self.flip_button = Button(
            text="Flip card",
            background_color=[0.2, 0.6, 0.8, 1],  # Ładniejszy kolor
            color=[1, 1, 1, 1],
            size_hint=(1, 0.15),
            font_size='20sp'
        )
        self.flip_button.bind(on_press=self.flip_card)
        self.add_widget(self.flip_button)

        # Przycisk "Next card"
        self.next_button = Button(
            text="Next card",
            background_color=[0.8, 0.2, 0.2, 1],
            color=[1, 1, 1, 1],
            size_hint=(1, 0.15),
            font_size='20sp'
        )
        self.next_button.bind(on_press=self.next_card)
        self.add_widget(self.next_button)

        # Przycisk "Umiem"
        self.know_button = Button(
            text="Umiem",
            background_color=[0.2, 0.8, 0.2, 1],
            color=[1, 1, 1, 1],
            size_hint=(1, 0.15),
            font_size='20sp'
        )
        self.know_button.bind(on_press=self.know_card)
        self.add_widget(self.know_button)

        # Przycisk powrotu do menu głównego
        self.back_button = Button(
            text="Powrót do menu",
            size_hint=(1, 0.1),
            background_color=[0.2, 0.5, 0.8, 1],
            font_size='18sp'
        )
        self.back_button.bind(on_press=self.go_back_to_menu)
        self.add_widget(self.back_button)

    def show_no_flashcards_message(self):
        self.clear_widgets()
        self.add_widget(Label(
            text="Brak fiszek w bazie danych.",
            font_size='20sp',
            color=[1, 0, 0, 1],
            halign="center"
        ))

    def flip_card(self, instance):
        if self.polish_word_label not in self.children:
            self.clear_widgets()
            self.add_widget(self.polish_word_label)
            self.add_widget(self.flip_button)
            self.add_widget(self.next_button)
            self.add_widget(self.know_button)
            self.add_widget(self.back_button)  # Dodaj przycisk powrotu
        else:
            self.clear_widgets()
            self.add_widget(self.german_word_label)
            self.add_widget(self.flip_button)
            self.add_widget(self.next_button)
            self.add_widget(self.know_button)
            self.add_widget(self.back_button)  # Dodaj przycisk powrotu

    def next_card(self, instance):
        if self.flashcards:
            self.flashcard = choice(self.flashcards)
            self.german_word_label.text = self.flashcard["german"]
            self.polish_word_label.text = self.flashcard["polish"]

    def know_card(self, instance):
        if self.flashcards:
            # Przenieś fiszkę do kolekcji learned_flashcards
            self.db.add_to_learned(self.flashcard)
            
            # Usuń fiszkę z kolekcji flashcards
            self.db.delete_flashcard(self.flashcard["german"])
            
            # Odśwież listę fiszek
            self.flashcards = self.db.get_all_flashcards()
            if not self.flashcards:
                self.show_no_flashcards_message()
            else:
                self.next_card(instance)

    def go_back_to_menu(self, instance):
        # Zmień ekran na "menu"
        self.manager.current = 'menu'
