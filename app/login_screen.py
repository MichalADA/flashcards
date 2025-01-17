from base_screen import BaseScreen
from db import MongoDB

class LoginScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        """
        Ekran logowania użytkownika.
        - manager: Zarządza przełączaniem ekranów.
        """
        super().__init__(**kwargs)
        self.manager = manager
        self.db = MongoDB()  # Inicjalizacja połączenia z bazą danych
        self.menu_screen = None  # Referencja do ekranu menu
        
        # Dodanie tytułu ekranu
        self.add_widget(self.create_title("Logowanie"))
        
        # Kontener na formularz logowania
        self.form_container = self.create_container()
        
        # Pole na komunikaty błędów
        self.error_label = self.create_error_label()
        self.form_container.add_widget(self.error_label)
        
        # Pola tekstowe do logowania
        self.username_input = self.create_text_input("Nazwa użytkownika")
        self.password_input = self.create_text_input("Hasło", password=True)
        
        # Ustawienie kolejności przełączania między polami (klawisz TAB)
        self.username_input.next_field = self.password_input
        
        # Dodanie pól tekstowych do kontenera
        self.form_container.add_widget(self.username_input)
        self.form_container.add_widget(self.password_input)
        
        # Przycisk logowania
        login_button = self.create_button("Zaloguj się", self.get_primary_color())
        login_button.bind(on_press=self.login)
        
        # Przycisk przejścia do rejestracji
        register_button = self.create_button("Utwórz nowe konto", self.get_secondary_color())
        register_button.bind(on_press=self.go_to_register)
        
        # Dodanie przycisków do kontenera
        self.form_container.add_widget(login_button)
        self.form_container.add_widget(register_button)
        
        # Dodanie kontenera do ekranu
        self.add_widget(self.form_container)

    def login(self, instance):
        """
        Funkcja logowania użytkownika.
        - instance: Obiekt przycisku, który wywołał funkcję.
        """
        username = self.username_input.text.strip()  # Pobranie nazwy użytkownika
        password = self.password_input.text.strip()  # Pobranie hasła
        
        # Sprawdzenie, czy oba pola są wypełnione
        if not username or not password:
            self.error_label.text = "Wprowadź nazwę użytkownika i hasło"
            return

        # Logowanie użytkownika w bazie danych
        success, message = self.db.login_user(username, password)
        if success:
            print(f"Logowanie udane: {username}")  
            if self.menu_screen:  # Jeśli ekran menu jest ustawiony
                print(f"Ustawianie użytkownika w menu: {username}")
                self.menu_screen.current_user = username  # Ustawienie zalogowanego użytkownika w menu
                self.db.current_user = username  # Aktualizacja w obiekcie MongoDB
                print(f"Aktualny użytkownik w menu: {self.menu_screen.current_user}")
            else:
                print("Menu screen nie jest ustawiony!")
            self.manager.current = 'menu'  # Przejście do ekranu menu
        else:
            self.error_label.text = message  # Wyświetlenie komunikatu błędu

    def go_to_register(self, instance):
        """
        Przejście do ekranu rejestracji.
        """
        self.error_label.text = ""  # Czyszczenie komunikatu błędu
        self.manager.current = 'register'
