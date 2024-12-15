from db import MongoDB
import json
import os

def load_grammar_rules():
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
    db = MongoDB()
    rules = load_grammar_rules()
    
    if not rules:
        return
    
    # Wyczyść istniejące reguły
    db.grammar_collection.delete_many({})
    
    # Dodaj nowe reguły
    for rule in rules['grammar_rules']:
        db.add_grammar_rule(rule)
    
    print("Zasady gramatyczne zostały dodane do bazy danych!")

if __name__ == "__main__":
    add_grammar_rules_to_db()