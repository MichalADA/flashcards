# Aplikacja Flashcards

## 📖 Opis Projektu
Aplikacja Flashcards to narzędzie edukacyjne do nauki języka niemieckiego. Umożliwia użytkownikom:
- Naukę przy pomocy fiszek
- Odtwarzanie dialogów i materiałów audio
- Przeglądanie zasad gramatycznych

Projekt powstał jako zaliczenie przedmiotu na studiach, koncentrując się na wykorzystaniu technologii MongoDB, Python Kivy oraz Docker.

## 🚀 Funkcjonalności
- Uwierzytelnianie użytkowników (logowanie i rejestracja) z bezpiecznym przechowywaniem haseł
- Tworzenie i przeglądanie fiszek z możliwością oznaczania jako nauczone
- Odtwarzanie dialogów i materiałów do słuchania z bazy danych
- Interfejs graficzny zaprojektowany w Kivy z responsywnym układem
- Integracja z bazą danych MongoDB

## 🛠️ Wymagania Systemowe
- Python 3.8+
- MongoDB
- Docker i Docker Compose
- Wirtualne środowisko Python (zalecane)

### Wymagane biblioteki Python:
- Kivy (framework GUI)
- pymongo (łączność z MongoDB)
- pozostałe zależności znajdują się w pliku requirements.txt

### Instalacja Dockera:
1. Dla Ubuntu/Debian:
```bash
# Aktualizacja systemu
sudo apt update
sudo apt upgrade

# Instalacja wymaganych pakietów
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Dodanie klucza GPG repozytorium Dockera
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Dodanie repozytorium Dockera
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalacja Dockera
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

# Instalacja Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Dodanie użytkownika do grupy docker
sudo usermod -aG docker $USER
```

2. Dla Windows:
- Pobierz i zainstaluj Docker Desktop ze strony: https://www.docker.com/products/docker-desktop
- Docker Compose jest już dołączony do Docker Desktop dla Windows

## 📦 Struktura Projektu
```
├── app/
│   ├── add_to_base/
│   │   ├── add_dialogs.py     # Skrypty dodające dialogi do bazy
│   │   ├── add_grama.py       # Skrypty dodające gramatykę
│   │   ├── add_voice.py       # Skrypty dodające pliki głosowe
│   │   └── grammar_rules.json
│   ├── base_screen.py
│   ├── db.py
│   ├── flashcards.py
│   ├── grama.py
│   ├── learned_flashcards.py
│   ├── listening.py
│   ├── login_screen.py
│   ├── main.py
│   ├── menu.py
│   ├── password_requirements_popup.py
│   ├── password_validator.py
│   ├── register_screen.py
│   ├── screen_config.py
│   └── test/
│       └── test_db.py
├── data/
│   └── flashcards.json        # Zawartość bazy danych
├── Dialogs/                   # Pliki audio z dialogami
│   ├── PrzedstawienieSie.mp3
│   ├── PytanieODroga.mp3
│   ├── WKawiarni.mp3
│   └── WSklepie.mp3
├── Voice/                     # Nagrania głosowe
│   ├── Blume.mp3
│   ├── Hallo.mp3
│   ├── Milch.mp3
│   └── Tisch.mp3
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🚀 Instalacja i Konfiguracja

### Używając Dockera
WAŻNE: Po zbudowaniu środowiska Docker należy zainicjalizować bazę danych używając skryptów z katalogu add_to_base:

1. Klonowanie repozytorium:
```bash
git clone <adres-repozytorium>
cd flashcards
```

2. Budowa i uruchomienie przy użyciu Docker Compose:
```bash
docker-compose up -d

3. Inicjalizacja bazy danych:
```bash
# Aktywuj środowisko wirtualne jeśli używasz
source myenv/bin/activate  # Na Windows: myenv\Scripts\activate

# Uruchom skrypty inicjalizujące w następującej kolejności:
python app/add_to_base/add_dialogs.py
python app/add_to_base/add_grama.py
python app/add_to_base/add_voice.py
```

Te skrypty są niezbędne do prawidłowego działania aplikacji, ponieważ dodają do bazy danych:
- Dialogi (add_dialogs.py)
- Zasady gramatyczne (add_grama.py)
- Pliki dźwiękowe (add_voice.py)
```

Aplikacja wykorzystuje oficjalny obraz MongoDB jako bazę danych, jak określono w Dockerfile:
```dockerfile
FROM mongo:latest
```

Konfiguracja docker-compose.yml zawiera:
```yaml
services:
  mongodb:
    image: flashcards-mongo
    container_name: mongodb-container
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped

volumes:
  mongodb_data:
```

### Instalacja Manualna
1. Utworzenie wirtualnego środowiska:
```bash
python -m venv myenv
source myenv/bin/activate  # Na Windows: myenv\Scripts\activate
```

2. Instalacja zależności:
```bash
pip install -r requirements.txt
```

3. Uruchomienie MongoDB lokalnie lub przez Dockera

4. Uruchomienie aplikacji:
```bash
python main.py
```

## 💾 Zarządzanie Danymi
- Aplikacja wykorzystuje `flashcards.json` do przechowywania danych fiszek
- Pliki audio są zorganizowane w dwóch katalogach:
  - `Dialogs/`: Zawiera pliki audio z konwersacjami
  - `Voice/`: Zawiera wymowę pojedynczych słów
- Skrypty do zasilania bazy danych znajdują się w `app/add_to_base/`


## ⚠️ Uwagi i Znane Problemy

1. **Interfejs użytkownika**
   - Menu aplikacji wymaga dopracowania - brak wyświetlania zalogowanego użytkownika
   - Interfejs gramatyki jest nieintuicyjny - obecny system przesuwania treści powinien zostać zastąpiony podziałem na działy i osobne ekrany

2. **System nauczonych fiszek**
   - Brak powiązania nauczonych fiszek z konkretnymi użytkownikami
   - Problem wymaga restrukturyzacji bazy danych - utworzenia osobnej kolekcji użytkowników zamiast obecnego systemu dynamicznego
   - Aplikacja nie aktualizuje widoku nauczonych fiszek w czasie rzeczywistym - wymaga restartu aplikacji

## 🔮 Plany Rozwoju

### Nowe Funkcjonalności
1. **System Wielojęzyczny**
   - Dodanie możliwości wyboru różnych języków do nauki
   - Spersonalizowane profile użytkowników

2. **System Osiągnięć**
   - Wdrożenie systemu odznak i nagród
   - Śledzenie postępów nauki

3. **Udoskonalenie Systemu Nauki**
   - Implementacja systemu codziennych zadań
   - Wprowadzenie inteligentnego systemu powtórek
   - Personalizacja ścieżki nauki

---


## 📄 Licencja
Licencja MIT
