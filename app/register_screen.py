from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from db import MongoDB

class RegisterScreen(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.manager = manager
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = [20, 20, 20, 20]

        self.db = MongoDB()

        # Tytuł
        self.add_widget(Label(
            text="Rejestracja",
            font_size='30sp',
            size_hint=(1, 0.2)
        ))

        # Pole tekstowe na nazwę użytkownika
        self.username_input = TextInput(
            hint_text="Nazwa użytkownika",
            multiline=False,
            size_hint=(1, 0.2)
        )
        self.add_widget(self.username_input)

        # Pole tekstowe na hasło
        self.password_input = TextInput(
            hint_text="Hasło",
            password=True,
            multiline=False,
            size_hint=(1, 0.2)
        )
        self.add_widget(self.password_input)

        # Przycisk "Zarejestruj"
        register_button = Button(
            text="Zarejestruj",
            size_hint=(1, 0.2),
            background_color=[0.2, 0.6, 0.8, 1]
        )
        register_button.bind(on_press=self.register)
        self.add_widget(register_button)

        # Przycisk "Powrót do logowania"
        back_button = Button(
            text="Powrót do logowania",
            size_hint=(1, 0.2),
            background_color=[0.8, 0.2, 0.2, 1]
        )
        back_button.bind(on_press=self.go_to_login)
        self.add_widget(back_button)

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username and password:
            success, message = self.db.register_user(username, password)
            print(message)
            if success:
                self.manager.current = 'login'
        else:
            print("Wprowadź nazwę użytkownika i hasło")

    def go_to_login(self, instance):
        self.manager.current = 'login'
