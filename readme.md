# Hydroponic System API

Projekt API do zarządzania systemami hydroponicznym.

## Wymagania systemowe
- Python **3.10+**
- PostgreSQL **17**
- Django **5.1.6**
- Django REST Framework **3.15.2**

**1. Klonowanie repozytorium:**


    > git clone https://github.com/twoje-repo/hydroponic-system.git
    
    > cd hydroponic-system


**2. Utworzenie środowiska i instalacja zależności:**


    > python -m venv venv

    > source venv/bin/activate

    > pip install -r requirements.txt


**3. Konfiguracja .env - wprowadź własne dane:**

    DATABASE_NAME=NAME
    
    DATABASE_USER=USERNAME
    
    DATABASE_PASSWORD=PASSWORD
    
    DATABASE_HOST=localhost
    
    DATABASE_PORT=5432


**4. Migracja i uruchomienie serwera:**

    > python manage.py migrate
    
    > python manage.py runserver
