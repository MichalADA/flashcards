# from base_screen import BaseScreen
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.scrollview import ScrollView
# from kivy.uix.label import Label
# from kivy.metrics import dp
# from db import MongoDB
# from menu import MenuButton  # Dodaj ten import

# class GrammarScreen(BaseScreen):
#     def __init__(self, manager, **kwargs):
#         super().__init__(**kwargs)
#         self.manager = manager
#         self.db = MongoDB()
        
#         # Dodaj tytuł
#         self.add_widget(self.create_title("Gramatyka niemiecka"))
        
#         # Kontener na kategorie
#         categories_container = GridLayout(
#             cols=2,
#             spacing=dp(10),
#             padding=dp(10)
#         )
        
#         # Przyciski kategorii
#         categories = ["syntax", "articles", "verbs", "tenses", 
#                      "adjectives", "pronouns", "prepositions"]
        
#         for category in categories:
#             btn = MenuButton(
#                 text=category.capitalize(),
#                 color=[0.3, 0.5, 0.8, 1]  # Niebieski
#             )
#             btn.bind(on_release=lambda x, c=category: self.show_grammar_rules(c))
#             categories_container.add_widget(btn)
        
#         self.add_widget(categories_container)
        
#         # Kontener na reguły gramatyczne
#         self.rules_scroll = ScrollView(size_hint=(1, 0.7))
#         self.rules_container = GridLayout(
#             cols=1,
#             spacing=dp(10),
#             size_hint_y=None,
#             padding=dp(10)
#         )
#         self.rules_container.bind(minimum_height=self.rules_container.setter('height'))
#         self.rules_scroll.add_widget(self.rules_container)
#         self.add_widget(self.rules_scroll)
        
#         # Przycisk powrotu
#         back_btn = MenuButton(
#             text="Powrót do menu",
#             color=[0.5, 0.5, 0.5, 1]
#         )
#         back_btn.bind(on_release=self.go_back)
#         self.add_widget(back_btn)

#     def show_grammar_rules(self, category):
#         """Wyświetla reguły gramatyczne dla wybranej kategorii"""
#         self.rules_container.clear_widgets()
#         rules = self.db.get_grammar_by_category(category)
        
#         for rule in rules:
#             # Kontener dla pojedynczej reguły
#             rule_box = GridLayout(
#                 cols=1,
#                 spacing=dp(5),
#                 size_hint_y=None,
#                 height=dp(200),
#                 padding=dp(10)
#             )
            
#             # Tytuł reguły
#             title = Label(
#                 text=f"[b]{rule['title']}[/b]",
#                 markup=True,
#                 font_size=dp(18),
#                 size_hint_y=None,
#                 height=dp(30)
#             )
#             rule_box.add_widget(title)
            
#             # Opis
#             description = Label(
#                 text=rule['description'],
#                 font_size=dp(16),
#                 size_hint_y=None,
#                 height=dp(60),
#                 text_size=(400, None)
#             )
#             rule_box.add_widget(description)
            
#             # Przykłady
#             examples = Label(
#                 text="\n".join(f"• {example}" for example in rule['examples']),
#                 font_size=dp(14),
#                 size_hint_y=None,
#                 height=dp(100),
#                 halign='left'
#             )
#             rule_box.add_widget(examples)
            
#             self.rules_container.add_widget(rule_box)

#     def go_back(self, instance):
#         """Powrót do menu głównego"""
#         self.manager.current = 'menu'


from base_screen import BaseScreen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.metrics import dp
from db import MongoDB
from menu import MenuButton  # Dodaj ten import

class GrammarScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.db = MongoDB()
        
        # Dodaj tytuł
        self.add_widget(self.create_title("Gramatyka niemiecka"))
        
        # Kontener na reguły gramatyczne
        self.rules_scroll = ScrollView(size_hint=(1, 0.9))
        self.rules_container = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None,
            padding=dp(10)
        )
        self.rules_container.bind(minimum_height=self.rules_container.setter('height'))
        self.rules_scroll.add_widget(self.rules_container)
        self.add_widget(self.rules_scroll)
        
        # Załaduj reguły gramatyczne
        self.show_all_grammar_rules()
        
        # Przycisk powrotu
        back_btn = MenuButton(
            text="Powrót do menu",
            color=[0.5, 0.5, 0.5, 1],
            size_hint=(1, None),
            height=dp(50)
        )
        back_btn.bind(on_release=self.go_back)
        self.add_widget(back_btn)

    def show_all_grammar_rules(self):
        """Wyświetla wszystkie reguły gramatyczne"""
        self.rules_container.clear_widgets()
        rules = self.db.get_all_grammar_rules()  # Pobranie wszystkich reguł z MongoDB

        if not rules:
            self.rules_container.add_widget(Label(
                text="Brak reguł gramatycznych do wyświetlenia.",
                font_size=dp(16),
                size_hint_y=None,
                height=dp(30),
                color=[0,0,0,1]
            ))
            return
        
        for rule in rules:
            # Sprawdzanie, czy wszystkie pola istnieją
            title = rule.get('title', 'Brak tytułu')
            description = rule.get('description', 'Brak opisu')
            examples = rule.get('examples', [])

            # Kontener dla pojedynczej reguły
            rule_box = GridLayout(
                cols=1,
                spacing=dp(5),
                size_hint_y=None,
                padding=dp(10),
                height=dp(200)
            )
            
            # Tytuł reguły
            title_label = Label(
                text=f"[b]{title}[/b]",
                markup=True,
                font_size=dp(18),
                size_hint_y=None,
                height=dp(30),
                color=[0,0,0,1]
            )
            rule_box.add_widget(title_label)
            
            # Opis reguły
            description_label = Label(
                text=description,
                font_size=dp(16),
                size_hint_y=None,
                height=dp(60),
                text_size=(400, None),
                color=[0,0.0,1]
            )
            rule_box.add_widget(description_label)
            
            # Przykłady
            if examples:
                examples_text = "\n".join(f"• {example}" for example in examples)
                examples_label = Label(
                    text=examples_text,
                    font_size=dp(14),
                    size_hint_y=None,
                    height=dp(100),
                    halign='left',
                    color=[0,0,0,1]
                )
                rule_box.add_widget(examples_label)
            else:
                rule_box.add_widget(Label(
                    text="Brak przykładów.",
                    font_size=dp(14),
                    size_hint_y=None,
                    height=dp(30),
                    color=[0,0,0,1]
                ))
            
            self.rules_container.add_widget(rule_box)

    def go_back(self, instance):
        """Powrót do menu głównego"""
        self.manager.current = 'menu'
