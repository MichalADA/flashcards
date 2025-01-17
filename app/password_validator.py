# password_validator.py
import re

class PasswordValidator:
    def __init__(self):
        self.min_length = 8
        self.min_digits = 1
        self.min_special_chars = 1
        self.min_uppercase = 1
        self.min_lowercase = 1
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def validate(self, password):
        # Sprawdza, czy hasło spełnia wszystkie kryteria bezpieczeństwa.
        # Zwraca tuple (bool, str) - (czy_poprawne, komunikat_błędu)
        
        # Sprawdzenie długości
        if len(password) < self.min_length:
            return False, f"Hasło musi mieć co najmniej {self.min_length} znaków"

        # Sprawdzenie cyfr
        if len(re.findall(r"\d", password)) < self.min_digits:
            return False, "Hasło musi zawierać co najmniej jedną cyfrę"

        # Sprawdzenie znaków specjalnych
        if len([char for char in password if char in self.special_chars]) < self.min_special_chars:
            return False, "Hasło musi zawierać co najmniej jeden znak specjalny"

        # Sprawdzenie wielkich liter
        if len(re.findall(r"[A-Z]", password)) < self.min_uppercase:
            return False, "Hasło musi zawierać co najmniej jedną wielką literę"

        # Sprawdzenie małych liter
        if len(re.findall(r"[a-z]", password)) < self.min_lowercase:
            return False, "Hasło musi zawierać co najmniej jedną małą literę"

        return True, "Hasło jest poprawne"

    def get_password_requirements(self):
        # """
        # Zwraca string z listą wszystkich wymagań dla hasła
        # """
        return f"""Wymagania dla hasła:
- Minimum {self.min_length} znaków
- Co najmniej {self.min_digits} cyfra
- Co najmniej {self.min_special_chars} znak specjalny
- Co najmniej {self.min_uppercase} wielka litera
- Co najmniej {self.min_lowercase} mała litera"""



