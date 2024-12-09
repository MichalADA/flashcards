from pymongo import MongoClient
import bcrypt

class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017", db_name="flashcard_app"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.flashcards_collection = self.db["flashcards"]
        self.learned_flashcards_collection = self.db["learned_flashcards"]
        self.users_collection = self.db["users"]

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
