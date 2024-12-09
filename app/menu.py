from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class MenuScreen(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = [20, 20, 20, 20]
        self.manager = manager

        # Tytuł menu
        title = Label(
            text="Menu Główne",
            font_size='30sp',
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        self.add_widget(title)

        # Przyciski menu
        button_grid = GridLayout(cols=2, spacing=10, size_hint=(1, 0.8))

        # Przycisk "Fiszki"
        flashcards_button = Button(
            text="Fiszki",
            font_size='20sp',
            background_color=[0.2, 0.7, 0.3, 1]
        )
        flashcards_button.bind(on_release=self.go_to_flashcards)
        button_grid.add_widget(flashcards_button)

        # Przycisk "Gramatyka"
        grammar_button = Button(
            text="Gramatyka",
            font_size='20sp',
            background_color=[0.3, 0.5, 0.8, 1]
        )
        button_grid.add_widget(grammar_button)

        # Przycisk "Nauczone fiszki"
        learned_flashcards_button = Button(
            text="Nauczone fiszki",
            font_size='20sp',
            background_color=[0.8, 0.5, 0.2, 1]
        )
        learned_flashcards_button.bind(on_release=self.go_to_learned_flashcards)
        button_grid.add_widget(learned_flashcards_button)

        # Przycisk "Słuchanki"
        listening_button = Button(
            text="Słuchanki",
            font_size='20sp',
            background_color=[0.5, 0.2, 0.8, 1]
        )
        button_grid.add_widget(listening_button)

        self.add_widget(button_grid)

    def go_to_flashcards(self, instance):
        self.manager.current = 'flashcards'

    def go_to_learned_flashcards(self, instance):
        self.manager.current = 'learned_flashcards'
