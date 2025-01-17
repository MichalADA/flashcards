from db import MongoDB
import json
import os

def load_grammar_rules():
    
    # Wczytuje reguły gramatyczne z pliku JSON.
    try:
        with open('grammar_rules.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Nie znaleziono pliku grammar_rules.json")
        return None
    except json.JSONDecodeError:
        print("Błąd dekodowania JSON w pliku grammar_rules.json")
        return None

def add_grammar_rules_to_db():
    # Dodaje reguly gramatyczne z pliku Json do bazy danych MongoDB
    db = MongoDB()
    rules = load_grammar_rules() # Ladowanie regul gramatycznych

    
    if not rules:
        return # Jeśli plik nie został załadowany, zakończ funkcję
    
    # Usunięcie wszystkich istniejących reguł w kolekcji `grammar_collection`
    db.grammar_collection.delete_many({})
    
    # Dodaj nowe reguły
    for rule in rules['grammar_rules']:
        db.add_grammar_rule(rule)
    
    print("Zasady gramatyczne zostały dodane do bazy danych!")

if __name__ == "__main__":
    add_grammar_rules_to_db()