# Hydroponic System API

Projekt API do zarządzania systemami hydroponicznym.

* Tworzenie i edycja systemów hydroponicznych.
* Dodawanie czujników (pH, temperatura, TDS) do systemu.
* Zapisywanie i odczytywanie pomiarów z czujników.
* Filtrowanie, sortowanie, paginacja danych.
* Autoryzacja użytkowników (JWT lub inna

## Wymagania systemowe.
* Python 3.9+
* PostgreSQL 14+ (lub nowszy)
* pip (zarządzanie pakietami Pythona)
* virtualenv lub docker

## Instalacja.

**1. Klonowanie repozytorium:**


    > git clone https://github.com/DiWorg/hydroponic.git
    
    > cd hydroponic


**2. Utworzenie środowiska:**


    > python -m venv venv
    
    > source venv/bin/activate   # Linux/MacOS
    
    # lub
    
    > venv\Scripts\activate      # Windows


**3. Instalacja zależności:**

    > pip install -r requirements.txt

**4. Utworzenie bazy danych PostgreSQL:**
* Upewnij się, że serwer PostgreSQL działa i masz utworzoną bazę danych.
* Jeśli potrzebujesz utworzyć bazę, wykonaj np.:

        > createdb hydroponic_db -U postgres

**5. Konfiguracja bazy danych PostgreSQL:**
* Stwórz plik .env na podstawie .env.example.

        DATABASE_NAME=hydroponic_db
        DATABASE_USER=USER
        DATABASE_PASSWORD=HASLO
        DATABASE_HOST=localhost
        DATABASE_PORT=5432


**6. Migracja i uruchomienie serwera:**

    > python manage.py makemigrations
    > python manage.py migrate

**7. Tworzenie superużytkownika (jeśli chcesz mieć dostęp do panelu admin):**

    python manage.py createsuperuser

## Uruchamianie aplikacji.
**1. Uruchom serwer:**

    > python manage.py runserver

Aplikacja będzie dostępna pod adresem:
http://127.0.0.1:8000/

Logowanie do panelu admin (opcjonalne):
http://127.0.0.1:8000/admin/ przy pomocy danych superużytkownika.

Dokumentacja API:

* http://127.0.0.1:8000/swagger/

* http://127.0.0.1:8000/redoc/

## Seedowanie danych.

Możesz  zapełnić bazę przykładowymi danymi:

    > python manage.py seed_test_data

## Konfiguracja dodatkowa.

**Debug Toolbar**

W trybie deweloperskim możesz użyć django-debug-toolbar, aby monitorować zapytania SQL i wydajność. Upewnij się, że masz DEBUG=True w .env.

**Paginacja**

Ustawienia paginacji dostępne są w pagination.py.
Można je modyfikować w celu zwiększenia lub zmniejszenia liczby elementów na stronie


## Uruchomienie z Dockerem (opcjonalna opcja instalacji).

**1. Instalcja Dockera.**

* Windows / macOS: Docker Desktop
* Linux: Docker Engine z repozytorium dystrybucji

**2. Konfiguracja docker-compose.yml.**

Przykład został dodany do repozytorium.

**3. Uruchomienie kontenery.**

    > docker compose build
    > docker compose up -d

Aplikacja będzie dostępna pod adresem:
http://127.0.0.1:8000/

**4. Migracja i utworzenie superużytkownika.**

W innym oknie terminala (lub tym samym, jeśli użyłeś -d):

    > docker compose exec web python manage.py migrate
    > docker compose exec web python manage.py createsuperuse

Możesz też zasilić bazę przykładowymi danymi:

    > docker compose exec web python manage.py seed_test_data



