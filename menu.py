from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class MenuScreen(GridLayout):
    def __init__(self, manager, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.cols = 2  # ilość kolumn na ekranie menu
        self.manager = manager

        # Przyciski do menu
        self.flashcards_button = Button(text="Fiszki")
        self.flashcards_button.bind(on_release=self.go_to_flashcards)
        self.add_widget(self.flashcards_button)

        self.grammar_button = Button(text="Gramatyka")
        # self.grammar_button.bind(on_release=self.go_to_grammar)  # Dodaj funkcję go_to_grammar, kiedy będzie gotowa
        self.add_widget(self.grammar_button)

        self.learned_flashcards_button = Button(text="Nauczone fiszki")
        # self.learned_flashcards_button.bind(on_release=self.go_to_learned_flashcards)  # Dodaj funkcję go_to_learned_flashcards, kiedy będzie gotowa
        self.add_widget(self.learned_flashcards_button)

        self.lisneing_button = Button(text = "Słuchanki ")
        #  tu przekierowanie bedzie 
        self.add_widget(self.lisneing_button)

    def go_to_flashcards(self, instance):
        self.manager.current = 'flashcards'  # przełączanie na ekran fiszek
