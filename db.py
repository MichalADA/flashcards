# from pymongo import MongoClient  # Moduł do obsługi bazy danych MongoDB
# import bcrypt  # Moduł do obsługi hashowania haseł

# class MongoDB:
#     def __init__(self, uri="mongodb://localhost:27017", db_name="flashcard_app"):
#         """
#         Inicjalizacja połączenia z bazą danych MongoDB.
#         - uri: Adres URI bazy danych (domyślnie lokalny MongoDB).
#         - db_name: Nazwa bazy danych, z której korzysta aplikacja.
#         """
#         self.client = MongoClient(uri)  # Łączenie z MongoDB
#         self.db = self.client[db_name]  # Otwieranie bazy danych
#         self.current_user = None  # Zmienna do przechowywania aktualnie zalogowanego użytkownika

#         # Inicjalizacja kolekcji w bazie danych
#         self.flashcards_collection = self.db["flashcards"]
#         self.learned_flashcards_collection = self.db["learned_flashcards"]
#         self.users_collection = self.db["users"]
#         self.grammar_collection = self.db["grammar"]  # Kolekcja dla zasad gramatycznych

#     # **Operacje na fiszkach**
#     def get_all_flashcards(self):
#         """Pobiera wszystkie fiszki z bazy danych."""
#         return list(self.flashcards_collection.find({}, {"_id": 0}))

#     def delete_flashcard(self, german_word):
#         """Usuwa fiszkę na podstawie podanego niemieckiego słowa."""
#         self.flashcards_collection.delete_one({"german": german_word})

#     def add_to_learned(self, flashcard):
#         """Dodaje fiszkę do kolekcji nauczonych fiszek."""
#         self.learned_flashcards_collection.insert_one(flashcard)

#     def get_learned_flashcards(self):
#         """Pobiera wszystkie nauczone fiszki."""
#         return list(self.learned_flashcards_collection.find({}, {"_id": 0}))

#     # **Operacje związane z użytkownikami**
#     def register_user(self, username, password):
#         """
#         Rejestruje nowego użytkownika w bazie danych.
#         - username: Nazwa użytkownika.
#         - password: Hasło w postaci czystego tekstu.
#         """
#         # Sprawdzanie, czy użytkownik już istnieje
#         if self.users_collection.find_one({"username": username}):
#             return False, "Użytkownik już istnieje"

#         # Hashowanie hasła przed zapisaniem w bazie
#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#         self.users_collection.insert_one({
#             "username": username,
#             "password": hashed_password
#         })
#         return True, "Rejestracja zakończona sukcesem"

#     def login_user(self, username, password):
#         """
#         Logowanie użytkownika.
#         - username: Nazwa użytkownika.
#         - password: Hasło w postaci czystego tekstu.
#         """
#         user = self.users_collection.find_one({"username": username})
#         if not user:
#             return False, "Nie znaleziono użytkownika"

#         # Sprawdzanie poprawności hasła
#         if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
#             return True, "Zalogowano pomyślnie"
#         else:
#             return False, "Nieprawidłowe hasło"

#     # **Operacje na regułach gramatycznych**
#     def add_grammar_rule(self, rule_data):
#         """Dodaje regułę gramatyczną do kolekcji `grammar`."""
#         return self.grammar_collection.insert_one(rule_data)

#     def get_all_grammar_rules(self):
#         """Pobiera wszystkie reguły gramatyczne z kolekcji `grammar`."""
#         return list(self.grammar_collection.find({}, {"_id": 0}))

#     def get_grammar_by_category(self, category):
#         """Pobiera reguły gramatyczne dla podanej kategorii."""
#         return list(self.grammar_collection.find({"category": category}, {"_id": 0}))

#     # **Operacje na wymowie (pronunciation)**
#     def get_pronunciations(self):
#         """Pobiera wszystkie pliki wymowy."""
#         return list(self.db.pronunciation.find(
#             {"category": "Wymowa"},
#             {"_id": 0}
#         ))

#     def get_pronunciation_by_word(self, german_word):
#         """Pobiera plik wymowy dla konkretnego słowa."""
#         return self.db.pronunciation.find_one(
#             {"german": german_word, "category": "Wymowa"},
#             {"_id": 0}
#         )

#     def delete_pronunciation(self, german_word):
#         """Usuwa plik wymowy dla konkretnego słowa."""
#         return self.db.pronunciation.delete_one({
#             "german": german_word,
#             "category": "Wymowa"
#         })

#     # **Operacje na dialogach**
#     def get_dialogs(self):
#         """Pobiera wszystkie dialogi."""
#         return list(self.db.dialogs.find(
#             {"category": "Dialogi"},
#             {"_id": 0}
#         ))

#     def get_dialog_by_name(self, dialog_name):
#         """Pobiera konkretny dialog na podstawie nazwy."""
#         return self.db.dialogs.find_one(
#             {"german": dialog_name, "category": "Dialogi"},
#             {"_id": 0}
#         )

#     def delete_dialog(self, dialog_name):
#         """Usuwa dialog na podstawie nazwy."""
#         return self.db.dialogs.delete_one({
#             "german": dialog_name,
#             "category": "Dialogi"
#         })
from pymongo import MongoClient
from security import DatabaseSecurity
import logging

class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017", db_name="flashcard_app"):
        """
        Inicjalizacja połączenia z bazą danych MongoDB i modułu bezpieczeństwa.
        - uri: Adres URI bazy danych (domyślnie lokalny MongoDB)
        - db_name: Nazwa bazy danych
        """
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.current_user = None
        self.security = DatabaseSecurity()

        # Inicjalizacja kolekcji w bazie danych
        self.flashcards_collection = self.db["flashcards"]
        self.learned_flashcards_collection = self.db["learned_flashcards"]
        self.users_collection = self.db["users"]
        self.grammar_collection = self.db["grammar"]

        # Konfiguracja logowania
        logging.basicConfig(
            filename='database.log',
            level=logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    # Operacje na fiszkach
    def get_all_flashcards(self):
        """Pobiera wszystkie fiszki z bazy danych."""
        try:
            return list(self.flashcards_collection.find({}, {"_id": 0}))
        except Exception as e:
            logging.error(f"Błąd podczas pobierania fiszek: {str(e)}")
            return []

    def delete_flashcard(self, german_word):
        """Usuwa fiszkę na podstawie podanego niemieckiego słowa."""
        try:
            sanitized_word = self.security.sanitize_input(german_word)
            self.flashcards_collection.delete_one({"german": sanitized_word})
            logging.info(f"Usunięto fiszkę: {sanitized_word}")
            return True, "Fiszka została usunięta"
        except Exception as e:
            logging.error(f"Błąd podczas usuwania fiszki: {str(e)}")
            return False, "Wystąpił błąd podczas usuwania fiszki"

    def add_to_learned(self, flashcard):
        """Dodaje fiszkę do kolekcji nauczonych fiszek."""
        try:
            self.learned_flashcards_collection.insert_one(flashcard)
            logging.info(f"Dodano nauczoną fiszkę: {flashcard.get('german', '')}")
            return True, "Fiszka została oznaczona jako nauczona"
        except Exception as e:
            logging.error(f"Błąd podczas dodawania do nauczonych: {str(e)}")
            return False, "Wystąpił błąd podczas oznaczania fiszki"

    def get_learned_flashcards(self):
        """Pobiera wszystkie nauczone fiszki."""
        try:
            return list(self.learned_flashcards_collection.find({}, {"_id": 0}))
        except Exception as e:
            logging.error(f"Błąd podczas pobierania nauczonych fiszek: {str(e)}")
            return []

    # Operacje związane z użytkownikami
    def register_user(self, username, password):
        """
        Rejestruje nowego użytkownika z zabezpieczeniami.
        - username: Nazwa użytkownika
        - password: Hasło w postaci czystego tekstu
        """
        # Sprawdzenie formatu nazwy użytkownika
        valid_username, username_msg = self.security.check_username_format(username)
        if not valid_username:
            return False, username_msg

        # Walidacja siły hasła
        valid_password, password_msg = self.security.validate_password_strength(password)
        if not valid_password:
            return False, password_msg

        # Sanityzacja danych
        username = self.security.sanitize_input(username)

        try:
            # Sprawdzenie czy użytkownik istnieje
            if self.users_collection.find_one({"username": username}):
                return False, "Użytkownik już istnieje"

            # Hashowanie hasła i zapis do bazy
            hashed_password = self.security.hash_password(password)
            self.users_collection.insert_one({
                "username": username,
                "password": hashed_password
            })
            logging.info(f"Zarejestrowano nowego użytkownika: {username}")
            return True, "Rejestracja zakończona sukcesem"
        except Exception as e:
            logging.error(f"Błąd podczas rejestracji: {str(e)}")
            return False, "Wystąpił błąd podczas rejestracji"

    def login_user(self, username, password):
        """
        Logowanie użytkownika z zabezpieczeniami.
        - username: Nazwa użytkownika
        - password: Hasło w postaci czystego tekstu
        """
        # Sprawdzenie blokady konta
        can_attempt, message = self.security.can_attempt_login(username)
        if not can_attempt:
            return False, message

        # Sanityzacja i sprawdzenie danych
        username = self.security.sanitize_input(username)
        if not self.security.check_injection(username):
            logging.warning(f"Wykryto próbę SQL injection: {username}")
            return False, "Niedozwolone znaki w nazwie użytkownika"

        try:
            user = self.users_collection.find_one({"username": username})
            if not user:
                self.security.record_failed_attempt(username)
                return False, "Nie znaleziono użytkownika"

            if self.security.verify_password(password, user["password"]):
                self.security.reset_attempts(username)
                self.current_user = username
                logging.info(f"Użytkownik {username} zalogowany pomyślnie")
                return True, "Zalogowano pomyślnie"
            else:
                self.security.record_failed_attempt(username)
                return False, "Nieprawidłowe hasło"
        except Exception as e:
            logging.error(f"Błąd podczas logowania: {str(e)}")
            return False, "Wystąpił błąd podczas logowania"

    # Operacje na regułach gramatycznych
    def add_grammar_rule(self, rule_data):
        """Dodaje regułę gramatyczną do kolekcji grammar."""
        try:
            return self.grammar_collection.insert_one(rule_data)
        except Exception as e:
            logging.error(f"Błąd podczas dodawania reguły gramatycznej: {str(e)}")
            return None

    def get_all_grammar_rules(self):
        """Pobiera wszystkie reguły gramatyczne."""
        try:
            return list(self.grammar_collection.find({}, {"_id": 0}))
        except Exception as e:
            logging.error(f"Błąd podczas pobierania reguł gramatycznych: {str(e)}")
            return []

    def get_grammar_by_category(self, category):
        """Pobiera reguły gramatyczne dla podanej kategorii."""
        try:
            sanitized_category = self.security.sanitize_input(category)
            return list(self.grammar_collection.find({"category": sanitized_category}, {"_id": 0}))
        except Exception as e:
            logging.error(f"Błąd podczas pobierania kategorii gramatycznej: {str(e)}")
            return []

    # Operacje na wymowie (pronunciation)
    def get_pronunciations(self):
        """Pobiera wszystkie pliki wymowy."""
        try:
            return list(self.db.pronunciation.find(
                {"category": "Wymowa"},
                {"_id": 0}
            ))
        except Exception as e:
            logging.error(f"Błąd podczas pobierania plików wymowy: {str(e)}")
            return []

    def get_pronunciation_by_word(self, german_word):
        """Pobiera plik wymowy dla konkretnego słowa."""
        try:
            sanitized_word = self.security.sanitize_input(german_word)
            return self.db.pronunciation.find_one(
                {"german": sanitized_word, "category": "Wymowa"},
                {"_id": 0}
            )
        except Exception as e:
            logging.error(f"Błąd podczas pobierania wymowy słowa: {str(e)}")
            return None

    def delete_pronunciation(self, german_word):
        """Usuwa plik wymowy dla konkretnego słowa."""
        try:
            sanitized_word = self.security.sanitize_input(german_word)
            return self.db.pronunciation.delete_one({
                "german": sanitized_word,
                "category": "Wymowa"
            })
        except Exception as e:
            logging.error(f"Błąd podczas usuwania wymowy: {str(e)}")
            return None

    # Operacje na dialogach
    def get_dialogs(self):
        """Pobiera wszystkie dialogi."""
        try:
            return list(self.db.dialogs.find(
                {"category": "Dialogi"},
                {"_id": 0}
            ))
        except Exception as e:
            logging.error(f"Błąd podczas pobierania dialogów: {str(e)}")
            return []

    def get_dialog_by_name(self, dialog_name):
        """Pobiera konkretny dialog na podstawie nazwy."""
        try:
            sanitized_name = self.security.sanitize_input(dialog_name)
            return self.db.dialogs.find_one(
                {"german": sanitized_name, "category": "Dialogi"},
                {"_id": 0}
            )
        except Exception as e:
            logging.error(f"Błąd podczas pobierania dialogu: {str(e)}")
            return None

    def delete_dialog(self, dialog_name):
        """Usuwa dialog na podstawie nazwy."""
        try:
            sanitized_name = self.security.sanitize_input(dialog_name)
            return self.db.dialogs.delete_one({
                "german": sanitized_name,
                "category": "Dialogi"
            })
        except Exception as e:
            logging.error(f"Błąd podczas usuwania dialogu: {str(e)}")
            return None