# load_dialogs.py
import os
import base64
from db import MongoDB
import sys

def load_dialog_files():
    """
    Ładuje pliki mp3 z folderu Dialogs i dodaje je do bazy danych
    """
    db = MongoDB()
    
    # Uzyskaj ścieżkę do folderu Dialogs (jeden poziom wyżej względem app)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    folder_path = os.path.join(parent_dir, 'Dialogs')
    
    print(f"Szukam plików w: {folder_path}")
    
    # Sprawdź czy folder istnieje
    if not os.path.exists(folder_path):
        print(f"Błąd: Folder {folder_path} nie istnieje!")
        return
    
    # Przejdź przez wszystkie pliki mp3 w folderze
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):
            # Nazwa dialogu to nazwa pliku bez rozszerzenia
            dialog_name = os.path.splitext(filename)[0]
            
            # Wczytaj plik audio
            file_path = os.path.join(folder_path, filename)
            print(f"Przetwarzanie pliku: {file_path}")
            
            with open(file_path, 'rb') as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode()
            
            # Przygotuj dane do zapisania
            dialog_data = {
                "german": dialog_name,
                "audio_data": audio_data,
                "type": "dialog",
                "category": "Dialogi"
            }
            
            # Sprawdź czy dialog już istnieje w bazie
            existing = db.db.dialogs.find_one({"german": dialog_name})
            if existing:
                print(f"Aktualizuję {dialog_name}")
                db.db.dialogs.update_one(
                    {"german": dialog_name},
                    {"$set": dialog_data}
                )
            else:
                print(f"Dodaję {dialog_name}")
                db.db.dialogs.insert_one(dialog_data)

if __name__ == "__main__":
    load_dialog_files()