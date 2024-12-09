from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class MenuScreen(GridLayout):
    def __init__(self, manager, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.cols = 2
        self.manager = manager

        self.flashcards_button = Button(text="Fiszki")
        self.flashcards_button.bind(on_release=self.go_to_flashcards)
        self.add_widget(self.flashcards_button)

        self.grammar_button = Button(text="Gramatyka")
        self.add_widget(self.grammar_button)

        self.learned_flashcards_button = Button(text="Nauczone fiszki")
        self.learned_flashcards_button.bind(on_release=self.go_to_learned_flashcards)
        self.add_widget(self.learned_flashcards_button)

        self.listening_button = Button(text="Słuchanki")
        self.add_widget(self.listening_button)

    def go_to_flashcards(self, instance):
        self.manager.current = 'flashcards'

    def go_to_learned_flashcards(self, instance):
        self.manager.current = 'learned_flashcards'
