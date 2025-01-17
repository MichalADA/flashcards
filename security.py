import bcrypt
import re
import time
from typing import Dict, Tuple, Optional
import logging

class DatabaseSecurity:
    def __init__(self):
        # Konfiguracja logowania
        logging.basicConfig(
            filename='security.log',
            level=logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Słownik do śledzenia prób logowania
        self.login_attempts: Dict[str, Dict] = {}
        
        # Konfiguracja limitów
        self.MAX_LOGIN_ATTEMPTS = 5
        self.LOCKOUT_TIME = 300  # 5 minut

    def check_injection(self, input_str: str) -> bool:
        """
        Sprawdza czy dane wejściowe nie zawierają prób SQL injection
        """
        dangerous_patterns = [
            r'(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)(\s|$)',
            r';',
            r'--',
            r'\/\*.*\*\/',
            r'xp_.*',
            r'exec\s+.*'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, input_str, re.IGNORECASE):
                logging.warning(f"Wykryto próbę SQL injection: {input_str}")
                return False
        return True

    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """
        Sprawdza siłę hasła według ustalonych kryteriów
        """
        if len(password) < 8:
            return False, "Hasło musi mieć co najmniej 8 znaków"
        
        if not re.search(r"[A-Z]", password):
            return False, "Hasło musi zawierać przynajmniej jedną wielką literę"
            
        if not re.search(r"[a-z]", password):
            return False, "Hasło musi zawierać przynajmniej jedną małą literę"
            
        if not re.search(r"\d", password):
            return False, "Hasło musi zawierać przynajmniej jedną cyfrę"
            
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Hasło musi zawierać przynajmniej jeden znak specjalny"
            
        return True, "Hasło spełnia wszystkie wymagania"

    def can_attempt_login(self, username: str) -> Tuple[bool, str]:
        """
        Sprawdza czy użytkownik może próbować się zalogować
        """
        current_time = time.time()
        
        if username in self.login_attempts:
            attempts = self.login_attempts[username]
            
            # Sprawdź czy minął czas blokady
            if attempts['count'] >= self.MAX_LOGIN_ATTEMPTS:
                if current_time - attempts['last_attempt'] < self.LOCKOUT_TIME:
                    remaining_time = int(self.LOCKOUT_TIME - (current_time - attempts['last_attempt']))
                    return False, f"Konto zablokowane. Spróbuj za {remaining_time} sekund"
                else:
                    # Reset po czasie blokady
                    self.login_attempts[username] = {'count': 0, 'last_attempt': current_time}
                    
        return True, "Można próbować logowania"

    def record_failed_attempt(self, username: str):
        """
        Zapisuje nieudaną próbę logowania
        """
        current_time = time.time()
        
        if username not in self.login_attempts:
            self.login_attempts[username] = {'count': 1, 'last_attempt': current_time}
        else:
            self.login_attempts[username]['count'] += 1
            self.login_attempts[username]['last_attempt'] = current_time
            
        if self.login_attempts[username]['count'] >= self.MAX_LOGIN_ATTEMPTS:
            logging.warning(f"Konto {username} zostało zablokowane po {self.MAX_LOGIN_ATTEMPTS} nieudanych próbach")

    def reset_attempts(self, username: str):
        """
        Resetuje licznik nieudanych prób po udanym logowaniu
        """
        if username in self.login_attempts:
            del self.login_attempts[username]

    def sanitize_input(self, input_str: str) -> str:
        """
        Oczyszcza dane wejściowe
        """
        # Usuń znaki specjalne i potencjalnie niebezpieczne
        sanitized = re.sub(r'[<>"\';]', '', input_str)
        return sanitized.strip()

    def check_username_format(self, username: str) -> Tuple[bool, str]:
        """
        Sprawdza poprawność formatu nazwy użytkownika
        """
        if len(username) < 3:
            return False, "Nazwa użytkownika musi mieć co najmniej 3 znaki"
            
        if len(username) > 20:
            return False, "Nazwa użytkownika nie może być dłuższa niż 20 znaków"
            
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False, "Nazwa użytkownika może zawierać tylko litery, cyfry, podkreślenia i myślniki"
            
        return True, "Poprawna nazwa użytkownika"

    def hash_password(self, password: str) -> str:
        """
        Hashuje hasło używając bcrypt
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Weryfikuje hasło z hashem
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))