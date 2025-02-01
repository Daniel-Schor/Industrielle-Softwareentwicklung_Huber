import os
import sqlite3
import pandas as pd
from tabulate import tabulate

class Datei_Einlesen:
    """Klasse zum Einlesen einer CSV-Datei und Speichern der Daten in einer SQLite-Datenbank. ETL erfolgt hier drin."""

    def __init__(self, file_path: str):
        """Initialisiert die Klasse mit dem Pfad zur CSV-Datei."""
        self.file_path = os.path.abspath(file_path)
        self.data_frame = pd.read_csv(
            self.file_path,
            sep=",",  # Trennzeichen in der CSV-Datei
            encoding="utf-8-sig"  # Kodierung der Datei
        )
        # Entfernt überflüssige Leerzeichen aus den Spaltennamen
        self.data_frame.columns = self.data_frame.columns.str.strip()

        # Zwei Dezimalstellen für numerische Werte (außer "Year", "Country" und "Region" Spalten)
        required_columns = ["Year", "Country", "Region"]
        for column in self.data_frame.columns:
            if column not in required_columns:
                self.data_frame[column] = pd.to_numeric(
                    self.data_frame[column], errors='coerce')
                self.data_frame[column] = self.data_frame[column].map(
                    lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)

        # Methode um eine neue Spalte zu erzeugen, was die Summe von allen Spalten mit "Percentage" im Namen ist.
        self.add_sum_percentage_column()

        # Spalten mit den Wörtern "Tax" oder "Percentage" werden als Prozent formatiert, die mit Cost oder Income mit $.
        # Bei manchen Spalten sind sowohl das Wort "Tax" als "Cost" enthalten, da kommt dann die erste Bedingung.
        for column in self.data_frame.columns:
            if any(keyword in column for keyword in ["Tax", "Percentage"]):
                self.data_frame[column] = self.data_frame[column].map(
                    lambda x: f"{str(x)}%" if isinstance(x, (int, float, str)) else x)
            elif any(keyword in column for keyword in ["Cost", "Income"]):
                self.data_frame[column] = self.data_frame[column].map(
                    lambda x: f"${str(x)}" if isinstance(x, (int, float, str)) else x)
                
 # Methode um eine neue Spalte zu erzeugen, was die Summe von allen Spalten mit "Percentage" im Namen ist.
    def add_sum_percentage_column(self):
        """Erzeugt eine neue Spalte, die die Summe aller 'Percentage'-Spalten enthält."""
        percentage_columns = [column for column in self.data_frame.columns if "Percentage" in column]
        self.data_frame["Sum_Percentage"] = self.data_frame[percentage_columns].map(lambda x: float(str(x).replace('%', '')) if isinstance(x, str) else x).sum(axis=1)
        self.data_frame["Sum_Percentage"] = self.data_frame["Sum_Percentage"].map(lambda x: f"{x:.2f}")

    # Methode um die Daten in einer SQLite-Datenbank zu speichern
    def save_to_db(self, db_name: str, table_name: str):
        """Speichert die Daten in einer SQLite-Datenbank."""
        with sqlite3.connect(db_name) as connection:
            self.data_frame.to_sql(
                table_name, connection, if_exists='replace', index=False)
            connection.commit()

    # Methode um die Daten aus der SQLite-Datenbank anzuzeigen. Ist eigentlich nicht notwendig, wir müssen entscheiden ob wir das drin lassen.
    def show_db(self, db_name: str, table_name: str):
        """Liest die Daten aus der SQLite-Datenbank und gibt sie als Tabelle aus."""
        connection = sqlite3.connect(db_name)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, connection)
        connection.close()
        print(tabulate(df, headers='keys', tablefmt='psql'))

    def get_data_from_db(db_name: str, table_name: str):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data

if __name__ == "__main__":
    # Initialisiert die Verarbeitungsklasse mit dem Pfad zur CSV-Datei.
    processor = Datei_Einlesen(r"Industrielle-Softwareentwicklung_Huber\src\database\ETL\data\CostOfLivingAndIncome.csv")

    # Speichert die Daten in der SQLite-Datenbank.
    processor.save_to_db('Database1.db', 'CostOfLivingAndIncome')

    # Zeigt die Daten in der SQLite-Datenbank an.
    # processor.show_db('Database1.db', 'CostOfLivingAndIncome')
   