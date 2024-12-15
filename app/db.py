from pymongo import MongoClient
import bcrypt

class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017", db_name="flashcard_app"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.flashcards_collection = self.db["flashcards"]
        self.learned_flashcards_collection = self.db["learned_flashcards"]
        self.users_collection = self.db["users"]
        self.grammar_collection = self.db["grammar"]  # Dodanie kolekcji grammar

    def get_all_flashcards(self):
        """Pobierz wszystkie fiszki"""
        return list(self.flashcards_collection.find({}, {"_id": 0}))

    def delete_flashcard(self, german_word):
        """Usuń fiszkę na podstawie niemieckiego słowa"""
        self.flashcards_collection.delete_one({"german": german_word})

    def add_to_learned(self, flashcard):
        """Dodaj fiszkę do nauczonych"""
        self.learned_flashcards_collection.insert_one(flashcard)

    def get_learned_flashcards(self):
        """Pobierz wszystkie nauczone fiszki"""
        return list(self.learned_flashcards_collection.find({}, {"_id": 0}))

    def register_user(self, username, password):
        """Rejestracja nowego użytkownika"""
        if self.users_collection.find_one({"username": username}):
            return False, "Użytkownik już istnieje"

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users_collection.insert_one({
            "username": username,
            "password": hashed_password
        })
        return True, "Rejestracja zakończona sukcesem"

    def login_user(self, username, password):
        """Logowanie użytkownika"""
        user = self.users_collection.find_one({"username": username})
        if not user:
            return False, "Nie znaleziono użytkownika"

        if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            return True, "Zalogowano pomyślnie"
        else:
            return False, "Nieprawidłowe hasło"

    def add_grammar_rule(self, rule_data):
        """Dodaje regułę gramatyczną do bazy danych"""
        return self.grammar_collection.insert_one(rule_data)

    def get_all_grammar_rules(self):
        """Pobiera wszystkie reguły gramatyczne"""
        return list(self.grammar_collection.find({}, {"_id": 0}))

    def get_grammar_by_category(self, category):
        """Pobiera reguły gramatyczne dla danej kategorii"""
        return list(self.grammar_collection.find({"category": category}, {"_id": 0}))
    
    def get_pronunciations(self):
        """Pobiera wszystkie pliki wymowy"""
        return list(self.db.pronunciation.find(
            {"category": "Wymowa"},
            {"_id": 0}
        ))

    def get_pronunciation_by_word(self, german_word):
        """Pobiera wymowę konkretnego słowa"""
        return self.db.pronunciation.find_one(
            {"german": german_word, "category": "Wymowa"},
            {"_id": 0}
        )

    def delete_pronunciation(self, german_word):
        """Usuwa wymowę słowa"""
        return self.db.pronunciation.delete_one({
            "german": german_word,
            "category": "Wymowa"
        })
    def get_dialogs(self):
        """Pobiera wszystkie dialogi"""
        return list(self.db.dialogs.find(
            {"category": "Dialogi"},
            {"_id": 0}
        ))

    def get_dialog_by_name(self, dialog_name):
        """Pobiera konkretny dialog po nazwie"""
        return self.db.dialogs.find_one(
            {"german": dialog_name, "category": "Dialogi"},
            {"_id": 0}
        )

    def delete_dialog(self, dialog_name):
        """Usuwa dialog"""
        return self.db.dialogs.delete_one({
            "german": dialog_name,
            "category": "Dialogi"
        })