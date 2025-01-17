# Używamy oficjalnego obrazu MongoDB jako bazy
FROM mongo:latest

# Stwórz katalog w kontenerze na plik JSON
RUN mkdir -p /data

# Skopiuj plik flashcards.json do katalogu /data w obrazie
COPY ./data/flashcards.json /data/flashcards.json

# Wykonaj polecenie importowania danych podczas uruchamiania obrazu
CMD ["bash", "-c", "mongod --bind_ip_all --fork --logpath /var/log/mongodb.log &&   sleep 5 && mongoimport --db flashcard_app --collection flashcards --file /data/flashcards.json --jsonArray && tail -f /dev/null"]