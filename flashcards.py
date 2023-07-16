from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from random import choice

# Przykładowe fiszki
flashcards = {
    "Hund": "pies",
    "Katze": "kot",
    # Dodaj więcej fiszek...
}

class FlashcardApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.flashcard = choice(list(flashcards.items()))

        self.german_word_label = Label(text=self.flashcard[0], font_size='20sp', color=[1, 2, 0, 1], halign="center", size_hint=(1, 0.6))
        self.add_widget(self.german_word_label)

        self.polish_word_label = Label(text=self.flashcard[1], font_size='20sp', color=[1, 0, 0, 1], halign="center", size_hint=(1, 0.6))
        
        
        
        
        self.flip_button = Button(text="Flip card", background_color=[1, 3, 3, 1], color=[1, 1, 1, 1], size_hint=(1, 0.1))
        self.flip_button.bind(on_press=self.flip_card)
        self.add_widget(self.flip_button)

        self.next_button = Button(text="Next card", background_color=[1, 0, 0, 1], color=[1, 1, 1, 1], size_hint=(1, 0.1))
        self.next_button.bind(on_press=self.next_card)
        self.add_widget(self.next_button)

        self.know_button = Button(text="Umiem", background_color=[0, 1, 0, 1], color=[1, 1, 1, 1], size_hint=(1, 0.2))
        self.know_button.bind(on_press=self.know_card)
        self.add_widget(self.know_button)


        self.dontknow_button = Button(text="Nie umiem ", background_color=[0, 1, 0, 1], color=[1, 1, 1, 1], size_hint=(1, 0.2))
        
        self.add_widget(self.dontknow_button)


    def flip_card(self, instance):
        if self.polish_word_label not in self.children:
            self.clear_widgets()
            self.add_widget(self.polish_word_label)
            self.add_widget(self.flip_button)
            self.add_widget(self.next_button)
            self.add_widget(self.know_button)
        else:
            self.clear_widgets()
            self.add_widget(self.german_word_label)
            self.add_widget(self.flip_button)
            self.add_widget(self.next_button)
            self.add_widget(self.know_button)

    def next_card(self, instance):
        self.flashcard = choice(list(flashcards.items()))
        self.german_word_label.text = self.flashcard[0]
        self.polish_word_label.text = self.flashcard[1]
        self.clear_widgets()
        self.add_widget(self.german_word_label)
        self.add_widget(self.flip_button)
        self.add_widget(self.next_button)
        self.add_widget(self.know_button)

    def know_card(self, instance):
        if flashcards:  # Check if there are any flashcards left
            del flashcards[self.flashcard[0]]
            if flashcards:
                self.flashcard = choice(list(flashcards.items()))
                self.german_word_label.text = self.flashcard[0]
                self.polish_word_label.text = self.flashcard[1]
            else:
                self.german_word_label.text = "Brak fiszek"
                self.polish_word_label.text = ""
            self.clear_widgets()
            self.add_widget(self.german_word_label)
            self.add_widget(self.flip_button)
            self.add_widget(self.next_button)
            self.add_widget(self.know_button)
   
    