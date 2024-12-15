# login_screen.py
from base_screen import BaseScreen
from db import MongoDB

class LoginScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.db = MongoDB()
        
        # Dodanie tytułu
        self.add_widget(self.create_title("Logowanie"))
        
        # Kontener na formularz
        self.form_container = self.create_container()
        
        # Label na błędy
        self.error_label = self.create_error_label()
        self.form_container.add_widget(self.error_label)
        
        # Pola formularza
        self.username_input = self.create_text_input("Nazwa użytkownika")
        self.password_input = self.create_text_input("Hasło", password=True)
        
        # Ustawienie kolejności tab
        self.username_input.next_field = self.password_input
        
        # Dodanie pól do formularza
        self.form_container.add_widget(self.username_input)
        self.form_container.add_widget(self.password_input)
        
        # Przyciski
        login_button = self.create_button(
            "Zaloguj się",
            self.get_primary_color()
        )
        login_button.bind(on_press=self.login)
        
        register_button = self.create_button(
            "Utwórz nowe konto",
            self.get_secondary_color()
        )
        register_button.bind(on_press=self.go_to_register)
        
        # Dodanie przycisków do formularza
        self.form_container.add_widget(login_button)
        self.form_container.add_widget(register_button)
        
        # Dodanie formularza do ekranu
        self.add_widget(self.form_container)

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        if not username:
            self.error_label.text = "Wprowadź nazwę użytkownika"
            return
            
        if not password:
            self.error_label.text = "Wprowadź hasło"
            return

        success, message = self.db.login_user(username, password)
        if success:
            self.error_label.text = ""
            self.manager.current = 'menu'
        else:
            self.error_label.text = message

    def go_to_register(self, instance):
        self.error_label.text = ""
        self.manager.current = 'register'