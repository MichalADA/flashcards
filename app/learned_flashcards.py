# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.scrollview import ScrollView
# from kivy.uix.gridlayout import GridLayout
# from db import MongoDB

# class LearnedFlashcardsScreen(BoxLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.orientation = 'vertical'
#         self.db = MongoDB()
        
#         # Dodaj widok przewijania
#         scroll_view = ScrollView(size_hint=(1, 1))
#         grid = GridLayout(cols=1, size_hint_y=None)
#         grid.bind(minimum_height=grid.setter('height'))

#         # Pobierz nauczone fiszki
#         learned_flashcards = self.db.get_learned_flashcards()
#         if learned_flashcards:
#             for flashcard in learned_flashcards:
#                 grid.add_widget(Label(
#                     text=f"{flashcard['german']} - {flashcard['polish']}",
#                     font_size='20sp',
#                     size_hint_y=None,
#                     height=40
#                 ))
#         else:
#             grid.add_widget(Label(
#                 text="Brak nauczonych fiszek.",
#                 font_size='20sp',
#                 size_hint_y=None,
#                 height=40
#             ))
        
#         scroll_view.add_widget(grid)
#         self.add_widget(scroll_view)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from db import MongoDB

class LearnedFlashcardsScreen(BoxLayout):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager  # Przechowujemy menedżera ekranów
        self.orientation = 'vertical'

        # Przycisk powrotu
        back_button = Button(
            text="Powrót do menu",
            size_hint=(1, 0.1),
            background_color=[0.2, 0.5, 0.8, 1],
            font_size='18sp'
        )
        back_button.bind(on_press=self.go_back_to_menu)
        self.add_widget(back_button)

        # Sekcja przewijania fiszek
        scroll_view = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Pobranie nauczonych fiszek
        db = MongoDB()
        learned_flashcards = db.get_learned_flashcards()

        if learned_flashcards:
            for flashcard in learned_flashcards:
                grid.add_widget(Label(
                    text=f"{flashcard['german']} - {flashcard['polish']}",
                    font_size='20sp',
                    size_hint_y=None,
                    height=40
                ))
        else:
            grid.add_widget(Label(
                text="Brak nauczonych fiszek.",
                font_size='20sp',
                size_hint_y=None,
                height=40
            ))

        scroll_view.add_widget(grid)
        self.add_widget(scroll_view)

    def go_back_to_menu(self, instance):
        self.manager.current = 'menu'  # Zmień ekran na menu
