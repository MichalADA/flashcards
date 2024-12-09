from pymongo import MongoClient

# Połączenie z bazą MongoDB
def test_mongo_connection():
    try:
        # Połącz z MongoDB (domyślny adres localhost:27017)
        client = MongoClient("mongodb://localhost:27017")
        db = client["flashcard_app"]

        # Wyświetl kolekcje w bazie danych
        collections = db.list_collection_names()
        print("Połączenie z MongoDB zakończone sukcesem!")
        print("Kolekcje w bazie danych:", collections)

    except Exception as e:
        print("Błąd połączenia z MongoDB:")
        print(e)

# Uruchom test
if __name__ == "__main__":
    test_mongo_connection()