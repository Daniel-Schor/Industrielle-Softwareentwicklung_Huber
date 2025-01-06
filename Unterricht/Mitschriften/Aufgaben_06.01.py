import sqlite3

connection = sqlite3.connect('test.db')
cursor = connection.cursor()
# cursor.execute('CREATE TABLE IF NOT EXISTS person (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
# cursos.execute('INSERT INTO person (name, age) VALUES ("Max", 25)')
# connection.commit()

result = cursor.execute('SELECT * FROM person')
print(result.fetchall())
connection.close()


class DatabaseConnector:

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def create_table(self, table_name, columns):
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(columns)})')
        self.connection.commit()

    def insert(self, table_name, values):
        self.cursor.execute(f'INSERT INTO {table_name} VALUES ({", ".join(values)})')
        self.connection.commit()

    def select(self, table_name):
        return self.cursor.execute(f'SELECT * FROM {table_name}').fetchall()
    

with DatabaseConnector("person") as db:
    db.create_table("person", ["id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"])












"""# Schreibe einen Decorator, der für eine einfache Division überprüft, ob der untere Divident unter dem 
# Bruchstrich 0 ist und printe auf die Konsole: "Die Operation is nicht erlaubt" falls das so ist.
# Das Programm soll nicht abstürzen und sich normal beenden.





def save_division(func):
    def wrapper(a, b):
        if b == 0:
            return "Die Operation ist nicht erlaubt"
        return func(a, b)
    return wrapper

@save_division
def division(a, b):
    return a / b

print(division(5, 0))
print(division(5, 2))
"""
