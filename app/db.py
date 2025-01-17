from pymongo import MongoClient  # Moduł do obsługi bazy danych MongoDB
import bcrypt  # Moduł do obsługi hashowania haseł

class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017", db_name="flashcard_app"):
        """
        Inicjalizacja połączenia z bazą danych MongoDB.
        - uri: Adres URI bazy danych (domyślnie lokalny MongoDB).
        - db_name: Nazwa bazy danych, z której korzysta aplikacja.
        """
        self.client = MongoClient(uri)  # Łączenie z MongoDB
        self.db = self.client[db_name]  # Otwieranie bazy danych
        self.current_user = None  # Zmienna do przechowywania aktualnie zalogowanego użytkownika

        # Inicjalizacja kolekcji w bazie danych
        self.flashcards_collection = self.db["flashcards"]
        self.learned_flashcards_collection = self.db["learned_flashcards"]
        self.users_collection = self.db["users"]
        self.grammar_collection = self.db["grammar"]  # Kolekcja dla zasad gramatycznych

    # **Operacje na fiszkach**
    def get_all_flashcards(self):
        """Pobiera wszystkie fiszki z bazy danych."""
        return list(self.flashcards_collection.find({}, {"_id": 0}))

    def delete_flashcard(self, german_word):
        """Usuwa fiszkę na podstawie podanego niemieckiego słowa."""
        self.flashcards_collection.delete_one({"german": german_word})

    def add_to_learned(self, flashcard):
        """Dodaje fiszkę do kolekcji nauczonych fiszek."""
        self.learned_flashcards_collection.insert_one(flashcard)

    def get_learned_flashcards(self):
        """Pobiera wszystkie nauczone fiszki."""
        return list(self.learned_flashcards_collection.find({}, {"_id": 0}))

    # **Operacje związane z użytkownikami**
    def register_user(self, username, password):
        """
        Rejestruje nowego użytkownika w bazie danych.
        - username: Nazwa użytkownika.
        - password: Hasło w postaci czystego tekstu.
        """
        # Sprawdzanie, czy użytkownik już istnieje
        if self.users_collection.find_one({"username": username}):
            return False, "Użytkownik już istnieje"

        # Hashowanie hasła przed zapisaniem w bazie
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users_collection.insert_one({
            "username": username,
            "password": hashed_password
        })
        return True, "Rejestracja zakończona sukcesem"

    def login_user(self, username, password):
        """
        Logowanie użytkownika.
        - username: Nazwa użytkownika.
        - password: Hasło w postaci czystego tekstu.
        """
        user = self.users_collection.find_one({"username": username})
        if not user:
            return False, "Nie znaleziono użytkownika"

        # Sprawdzanie poprawności hasła
        if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            return True, "Zalogowano pomyślnie"
        else:
            return False, "Nieprawidłowe hasło"

    # **Operacje na regułach gramatycznych**
    def add_grammar_rule(self, rule_data):
        """Dodaje regułę gramatyczną do kolekcji `grammar`."""
        return self.grammar_collection.insert_one(rule_data)

    def get_all_grammar_rules(self):
        """Pobiera wszystkie reguły gramatyczne z kolekcji `grammar`."""
        return list(self.grammar_collection.find({}, {"_id": 0}))

    def get_grammar_by_category(self, category):
        """Pobiera reguły gramatyczne dla podanej kategorii."""
        return list(self.grammar_collection.find({"category": category}, {"_id": 0}))

    # **Operacje na wymowie (pronunciation)**
    def get_pronunciations(self):
        """Pobiera wszystkie pliki wymowy."""
        return list(self.db.pronunciation.find(
            {"category": "Wymowa"},
            {"_id": 0}
        ))

    def get_pronunciation_by_word(self, german_word):
        """Pobiera plik wymowy dla konkretnego słowa."""
        return self.db.pronunciation.find_one(
            {"german": german_word, "category": "Wymowa"},
            {"_id": 0}
        )

    def delete_pronunciation(self, german_word):
        """Usuwa plik wymowy dla konkretnego słowa."""
        return self.db.pronunciation.delete_one({
            "german": german_word,
            "category": "Wymowa"
        })

    # **Operacje na dialogach**
    def get_dialogs(self):
        """Pobiera wszystkie dialogi."""
        return list(self.db.dialogs.find(
            {"category": "Dialogi"},
            {"_id": 0}
        ))

    def get_dialog_by_name(self, dialog_name):
        """Pobiera konkretny dialog na podstawie nazwy."""
        return self.db.dialogs.find_one(
            {"german": dialog_name, "category": "Dialogi"},
            {"_id": 0}
        )

    def delete_dialog(self, dialog_name):
        """Usuwa dialog na podstawie nazwy."""
        return self.db.dialogs.delete_one({
            "german": dialog_name,
            "category": "Dialogi"
        })
