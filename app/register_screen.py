# register_screen.py
from base_screen import BaseScreen
from db import MongoDB

class RegisterScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.db = MongoDB()
        
        # Dodanie tytułu
        self.add_widget(self.create_title("Rejestracja"))
        
        # Kontener na formularz
        self.form_container = self.create_container()
        
        # Label na błędy
        self.error_label = self.create_error_label()
        self.form_container.add_widget(self.error_label)
        
        # Pola formularza
        self.username_input = self.create_text_input("Nazwa użytkownika")
        self.password_input = self.create_text_input("Hasło", password=True)
        self.confirm_password_input = self.create_text_input("Potwierdź hasło", password=True)
        
        # Ustawienie kolejności tab
        self.username_input.next_field = self.password_input
        self.password_input.next_field = self.confirm_password_input
        
        # Dodanie pól do formularza
        self.form_container.add_widget(self.username_input)
        self.form_container.add_widget(self.password_input)
        self.form_container.add_widget(self.confirm_password_input)
        
        # Przyciski
        register_button = self.create_button(
            "Zarejestruj się",
            self.get_primary_color()
        )
        register_button.bind(on_press=self.register)
        
        back_button = self.create_button(
            "Powrót do logowania",
            self.get_secondary_color()
        )
        back_button.bind(on_press=self.go_to_login)
        
        # Dodanie przycisków do formularza
        self.form_container.add_widget(register_button)
        self.form_container.add_widget(back_button)
        
        # Dodanie formularza do ekranu
        self.add_widget(self.form_container)

    def register(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        confirm_password = self.confirm_password_input.text.strip()
        
        # Walidacja pól
        if not username:
            self.error_label.text = "Wprowadź nazwę użytkownika"
            return
            
        if not password:
            self.error_label.text = "Wprowadź hasło"
            return
            
        if not confirm_password:
            self.error_label.text = "Potwierdź hasło"
            return
            
        if password != confirm_password:
            self.error_label.text = "Hasła nie są identyczne"
            return
            
        if len(password) < 6:
            self.error_label.text = "Hasło musi mieć co najmniej 6 znaków"
            return

        success, message = self.db.register_user(username, password)
        if success:
            self.error_label.text = ""
            self.manager.current = 'login'
        else:
            self.error_label.text = message

    def go_to_login(self, instance):
        self.error_label.text = ""
        self.manager.current = 'login'