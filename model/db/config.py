import os

DB_HOST = os.getenv('AGENDA_DB_HOST', 'localhost')
DB_PORT = os.getenv('AGENDA_DB_PORT', '5433')
DB_NAME = os.getenv('AGENDA_DB_NAME', 'agenda_virtual')
DB_USER = os.getenv('AGENDA_DB_USER', 'postgres')
DB_PASSWORD = os.getenv('AGENDA_DB_PASSWORD', 'admin') 