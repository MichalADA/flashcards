from pymongo import MongoClient

class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017", db_name="flashcard_app"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.flashcards_collection = self.db["flashcards"]
        self.learned_flashcards_collection = self.db["learned_flashcards"]

    def get_all_flashcards(self):
        return list(self.flashcards_collection.find({}, {"_id": 0}))

    def delete_flashcard(self, german_word):
        self.flashcards_collection.delete_one({"german": german_word})

    def add_to_learned(self, flashcard):
        # Dodaje fiszkę do kolekcji learned_flashcards
        self.learned_flashcards_collection.insert_one(flashcard)

    def get_learned_flashcards(self):
        # Pobiera wszystkie fiszki z kolekcji learned_flashcards
        return list(self.learned_flashcards_collection.find({}, {"_id": 0}))