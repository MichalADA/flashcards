# # Moduł zawierający klasę RegisterScreen odpowiedzialną za ekran rejestracji użytkownika.
# # Obsługuje formularz rejestracji, walidację danych i komunikację z bazą danych.


# from base_screen import BaseScreen  # Import klasy bazowej dla ekranów
# from db import MongoDB  # Import klasy do obsługi bazy danych MongoDB
# from password_validator import PasswordValidator  # Import klasy do walidacji hasła

# class RegisterScreen(BaseScreen):
    
#     # Klasa reprezentująca ekran rejestracji użytkownika.
#     # Dziedziczy po BaseScreen i implementuje formularz rejestracji z walidacją.
    
    
#     def __init__(self, manager, **kwargs):
        
#         # Inicjalizacja ekranu rejestracji.
        
#         # Parametry:
#         # - manager: Obiekt ScreenManager zarządzający przełączaniem ekranów
#         # - kwargs: Dodatkowe parametry przekazywane do klasy bazowej
        
#         # Wywołanie konstruktora klasy bazowej
#         super().__init__(**kwargs)
        
#         # Zapisanie referencji do managera ekranów
#         self.manager = manager
        
#         # Inicjalizacja połączenia z bazą danych
#         self.db = MongoDB()
        
#         # Inicjalizacja walidatora hasła
#         self.password_validator = PasswordValidator()
        
#         # === Tworzenie interfejsu użytkownika ===
        
#         # Dodanie tytułu ekranu
#         self.add_widget(self.create_title("Rejestracja"))
        
#         # Tworzenie głównego kontenera na formularz
#         self.form_container = self.create_container()
        
#         # Tworzenie i dodawanie etykiety na komunikaty błędów
#         self.error_label = self.create_error_label()
#         self.form_container.add_widget(self.error_label)
        
#         # Tworzenie i dodawanie etykiety z wymaganiami hasła
#         self.requirements_label = self.create_error_label()
#         self.requirements_label.text = self.password_validator.get_password_requirements()
#         self.form_container.add_widget(self.requirements_label)
        
#         # === Pola wprowadzania danych ===
        
#         # Pole na nazwę użytkownika
#         self.username_input = self.create_text_input("Nazwa użytkownika")
        
#         # Pole na hasło (z ukrywaniem znaków)
#         self.password_input = self.create_text_input("Hasło", password=True)
        
#         # Pole na potwierdzenie hasła
#         self.confirm_password_input = self.create_text_input("Potwierdź hasło", password=True)
        
#         # Konfiguracja kolejności przechodzenia między polami (TAB)
#         self.username_input.next_field = self.password_input
#         self.password_input.next_field = self.confirm_password_input
        
#         # Dodawanie pól do kontenera formularza
#         self.form_container.add_widget(self.username_input)
#         self.form_container.add_widget(self.password_input)
#         self.form_container.add_widget(self.confirm_password_input)
        
#         # === Przyciski akcji ===
        
#         # Przycisk rejestracji
#         register_button = self.create_button(
#             "Zarejestruj się",
#             self.get_primary_color()
#         )
#         register_button.bind(on_press=self.register)
        
#         # Przycisk powrotu do ekranu logowania
#         back_button = self.create_button(
#             "Powrót do logowania",
#             self.get_secondary_color()
#         )
#         back_button.bind(on_press=self.go_to_login)
        
#         # Dodawanie przycisków do formularza
#         self.form_container.add_widget(register_button)
#         self.form_container.add_widget(back_button)
        
#         # Dodanie całego kontenera formularza do ekranu
#         self.add_widget(self.form_container)

#     def register(self, instance):
        
#         # Obsługa procesu rejestracji użytkownika.
#         # Parametry:
#         # - instance: Obiekt przycisku, który wywołał funkcję (wymagany przez Kivy)
        
#         # Pobieranie i oczyszczanie danych z formularza
#         username = self.username_input.text.strip()
#         password = self.password_input.text.strip()
#         confirm_password = self.confirm_password_input.text.strip()
        
#         # === Podstawowa walidacja pól ===
        
#         # Sprawdzenie czy podano nazwę użytkownika
#         if not username:
#             self.error_label.text = "Wprowadź nazwę użytkownika"
#             return
        
#         # Sprawdzenie czy podano hasło
#         if not password:
#             self.error_label.text = "Wprowadź hasło"
#             return
        
#         # Sprawdzenie czy podano potwierdzenie hasła
#         if not confirm_password:
#             self.error_label.text = "Potwierdź hasło"
#             return
        
#         # Sprawdzenie czy hasła są identyczne
#         if password != confirm_password:
#             self.error_label.text = "Hasła nie są identyczne"
#             return
        
#         # === Zaawansowana walidacja hasła ===
        
#         # Sprawdzenie czy hasło spełnia wymagania bezpieczeństwa
#         is_valid, message = self.password_validator.validate(password)
#         if not is_valid:
#             self.error_label.text = message
#             return

#         # === Rejestracja użytkownika ===
        
#         # Próba rejestracji użytkownika w bazie danych
#         success, message = self.db.register_user(username, password)
        
#         if success:
#             # W przypadku sukcesu - przejście do ekranu logowania
#             self.error_label.text = ""
#             self.manager.current = 'login'
#         else:
#             # W przypadku błędu - wyświetlenie komunikatu
#             self.error_label.text = message

#     def go_to_login(self, instance):
        
#         # Obsługa przejścia do ekranu logowania.
        
#         # Parametry:
#         # - instance: Obiekt przycisku, który wywołał funkcję (wymagany przez Kivy)
#         # Wyczyszczenie komunikatu błędu
#         self.error_label.text = ""
        
#         # Zmiana aktualnego ekranu na ekran logowania
#         self.manager.current = 'login'

# Moduł zawierający klasę RegisterScreen odpowiedzialną za ekran rejestracji użytkownika.
# Obsługuje formularz rejestracji, walidację danych i komunikację z bazą danych.

from base_screen import BaseScreen  # Import klasy bazowej dla ekranów
from db import MongoDB  # Import klasy do obsługi bazy danych MongoDB
from password_validator import PasswordValidator  # Import klasy do walidacji hasła
from password_requirements_popup import PasswordRequirementsPopup  # Import klasy popupu z wymaganiami hasła
from kivy.uix.boxlayout import BoxLayout  # Import dla układu poziomego
from kivy.uix.button import Button  # Import dla przycisku
from kivy.metrics import dp  # Import dla jednostek rozmiaru

class RegisterScreen(BaseScreen):
    
    # Klasa reprezentująca ekran rejestracji użytkownika.
    # Dziedziczy po BaseScreen i implementuje formularz rejestracji z walidacją.
    
    def __init__(self, manager, **kwargs):
        
        # Inicjalizacja ekranu rejestracji.
        
        # Parametry:
        # - manager: Obiekt ScreenManager zarządzający przełączaniem ekranów
        # - kwargs: Dodatkowe parametry przekazywane do klasy bazowej
        
        # Wywołanie konstruktora klasy bazowej
        super().__init__(**kwargs)
        
        # Zapisanie referencji do managera ekranów
        self.manager = manager
        
        # Inicjalizacja połączenia z bazą danych
        self.db = MongoDB()
        
        # Inicjalizacja walidatora hasła
        self.password_validator = PasswordValidator()
        
        # === Tworzenie interfejsu użytkownika ===
        
        # Dodanie tytułu ekranu
        self.add_widget(self.create_title("Rejestracja"))
        
        # Tworzenie głównego kontenera na formularz
        self.form_container = self.create_container()
        
        # Tworzenie i dodawanie etykiety na komunikaty błędów
        self.error_label = self.create_error_label()
        self.form_container.add_widget(self.error_label)
        
        # === Pola wprowadzania danych ===
        
        # Pole na nazwę użytkownika
        self.username_input = self.create_text_input("Nazwa użytkownika")
        self.form_container.add_widget(self.username_input)
        
        # Tworzenie kontenera na pole hasła i przycisk info
        password_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        # Pole na hasło
        self.password_input = self.create_text_input("Hasło", password=True)
        password_container.add_widget(self.password_input)
        
        # Przycisk wyświetlający wymagania hasła
        info_button = Button(
            text='?',
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            background_color=[0.3, 0.5, 1, 1]  # Niebieski kolor
        )
        info_button.bind(on_press=self.show_password_requirements)
        password_container.add_widget(info_button)
        
        # Dodanie kontenera z hasłem i przyciskiem info
        self.form_container.add_widget(password_container)
        
        # Pole na potwierdzenie hasła
        self.confirm_password_input = self.create_text_input("Potwierdź hasło", password=True)
        self.form_container.add_widget(self.confirm_password_input)
        
        # Konfiguracja kolejności przechodzenia między polami (TAB)
        self.username_input.next_field = self.password_input
        self.password_input.next_field = self.confirm_password_input
        
        # === Przyciski akcji ===
        
        # Przycisk rejestracji
        register_button = self.create_button(
            "Zarejestruj się",
            self.get_primary_color()
        )
        register_button.bind(on_press=self.register)
        
        # Przycisk powrotu do ekranu logowania
        back_button = self.create_button(
            "Powrót do logowania",
            self.get_secondary_color()
        )
        back_button.bind(on_press=self.go_to_login)
        
        # Dodawanie przycisków do formularza
        self.form_container.add_widget(register_button)
        self.form_container.add_widget(back_button)
        
        # Dodanie całego kontenera formularza do ekranu
        self.add_widget(self.form_container)

    def show_password_requirements(self, instance):
        
        # Wyświetla popup z wymaganiami hasła
        
        # Parametry:
        # - instance: Obiekt przycisku, który wywołał funkcję
        popup = PasswordRequirementsPopup()
        popup.open()

    def register(self, instance):
        
        # Obsługa procesu rejestracji użytkownika.
        
        # Parametry:
        # - instance: Obiekt przycisku, który wywołał funkcję (wymagany przez Kivy)
        
        # Pobieranie i oczyszczanie danych z formularza
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        confirm_password = self.confirm_password_input.text.strip()
        
        # === Podstawowa walidacja pól ===
        
        # Sprawdzenie czy podano nazwę użytkownika
        if not username:
            self.error_label.text = "Wprowadź nazwę użytkownika"
            return
        
        # Sprawdzenie czy podano hasło
        if not password:
            self.error_label.text = "Wprowadź hasło"
            return
        
        # Sprawdzenie czy podano potwierdzenie hasła
        if not confirm_password:
            self.error_label.text = "Potwierdź hasło"
            return
        
        # Sprawdzenie czy hasła są identyczne
        if password != confirm_password:
            self.error_label.text = "Hasła nie są identyczne"
            return
        
        # === Zaawansowana walidacja hasła ===
        
        # Sprawdzenie czy hasło spełnia wymagania bezpieczeństwa
        is_valid, message = self.password_validator.validate(password)
        if not is_valid:
            self.error_label.text = message
            return

        # === Rejestracja użytkownika ===
        
        # Próba rejestracji użytkownika w bazie danych
        success, message = self.db.register_user(username, password)
        
        if success:
            # W przypadku sukcesu - przejście do ekranu logowania
            self.error_label.text = ""
            self.manager.current = 'login'
        else:
            # W przypadku błędu - wyświetlenie komunikatu
            self.error_label.text = message

    def go_to_login(self, instance):
        
        # Obsługa przejścia do ekranu logowania.
        
        # Parametry:
        # - instance: Obiekt przycisku, który wywołał funkcję (wymagany przez Kivy)
        
        # Wyczyszczenie komunikatu błędu
        self.error_label.text = ""
        
        # Zmiana aktualnego ekranu na ekran logowania
        self.manager.current = 'login'