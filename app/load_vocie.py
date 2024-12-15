# load_vocie.py
import os
import base64
from db import MongoDB
import sys

def load_pronunciation_files():
    """
    Ładuje pliki mp3 z folderu Voice i dodaje je do bazy danych
    """
    db = MongoDB()
    
    # Uzyskaj ścieżkę do folderu Voice (jeden poziom wyżej względem app)
    current_dir = os.path.dirname(os.path.abspath(__file__))  # ścieżka do aktualnego pliku
    parent_dir = os.path.dirname(current_dir)  # wyjście poziom wyżej
    folder_path = os.path.join(parent_dir, 'Voice')  # ścieżka do folderu Voice
    
    print(f"Szukam plików w: {folder_path}")
    
    # Sprawdź czy folder istnieje
    if not os.path.exists(folder_path):
        print(f"Błąd: Folder {folder_path} nie istnieje!")
        return
    
    # Przejdź przez wszystkie pliki mp3 w folderze
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):
            # Nazwa niemieckiego słowa to nazwa pliku bez rozszerzenia
            german_word = os.path.splitext(filename)[0]
            
            # Wczytaj plik audio
            file_path = os.path.join(folder_path, filename)
            print(f"Przetwarzanie pliku: {file_path}")
            
            with open(file_path, 'rb') as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode()
            
            # Przygotuj dane do zapisania
            word_data = {
                "german": german_word,
                "audio_data": audio_data,
                "type": "pronunciation",
                "category": "Wymowa"
            }
            
            # Sprawdź czy słowo już istnieje w bazie
            existing = db.db.pronunciation.find_one({"german": german_word})
            if existing:
                print(f"Aktualizuję {german_word}")
                db.db.pronunciation.update_one(
                    {"german": german_word},
                    {"$set": word_data}
                )
            else:
                print(f"Dodaję {german_word}")
                db.db.pronunciation.insert_one(word_data)

if __name__ == "__main__":
    load_pronunciation_files()