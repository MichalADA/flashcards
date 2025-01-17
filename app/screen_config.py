from menu import MenuScreen
from flashcards import FlashcardApp
from learned_flashcards import LearnedFlashcardsScreen
from login_screen import LoginScreen
from register_screen import RegisterScreen
from grama import GrammarScreen
from listening import ListeningScreen

# Konfiguracja wszystkich ekranów aplikacji
SCREEN_CONFIG = {
    'login': {
        'class': LoginScreen,  # Klasa odpowiedzialna za ekran logowania
        'name': 'login',  # Unikalna nazwa ekranu
        'requires_menu_screen': True  # Wskazuje, że ekran wymaga referencji do ekranu menu
    },
    'register': {
        'class': RegisterScreen,  # Klasa odpowiedzialna za ekran rejestracji
        'name': 'register'
    },
    'menu': {
        'class': MenuScreen,  # Klasa odpowiedzialna za główne menu aplikacji
        'name': 'menu'
    },
    'flashcards': {
        'class': FlashcardApp,  # Klasa odpowiedzialna za ekran fiszek
        'name': 'flashcards'
    },
    'learned_flashcards': {
        'class': LearnedFlashcardsScreen,  # Klasa odpowiedzialna za ekran nauczonych fiszek
        'name': 'learned_flashcards'
    },
    'grammar': {
        'class': GrammarScreen,  # Klasa odpowiedzialna za ekran gramatyki
        'name': 'grammar'
    },
    'listening': {
        'class': ListeningScreen,  # Klasa odpowiedzialna za ekran słuchanek
        'name': 'listening',
        'requires_db': True  # Wskazuje, że ekran wymaga dostępu do bazy danych
    }
}
