from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from db import MongoDB

class LoginScreen(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.manager = manager
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = [20, 20, 20, 20]

        self.db = MongoDB()

        # Tytuł
        self.add_widget(Label(
            text="Logowanie",
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

        # Przycisk "Zaloguj"
        login_button = Button(
            text="Zaloguj",
            size_hint=(1, 0.2),
            background_color=[0.2, 0.6, 0.8, 1]
        )
        login_button.bind(on_press=self.login)
        self.add_widget(login_button)

        # Przycisk "Rejestracja"
        register_button = Button(
            text="Rejestracja",
            size_hint=(1, 0.2),
            background_color=[0.8, 0.2, 0.2, 1]
        )
        register_button.bind(on_press=self.go_to_register)
        self.add_widget(register_button)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username and password:
            success, message = self.db.login_user(username, password)
            print(message)
            if success:
                self.manager.current = 'menu'  # Przejdź do menu głównego
        else:
            print("Wprowadź nazwę użytkownika i hasło")

    def go_to_register(self, instance):
        self.manager.current = 'register'
