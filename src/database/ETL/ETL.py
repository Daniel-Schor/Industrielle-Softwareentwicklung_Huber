import os
import sqlite3
import pandas as pd
from tabulate import tabulate

class Datei_Einlesen:
    """Klasse zum Einlesen einer CSV-Datei und Speichern der Daten in einer SQLite-Datenbank. ETL erfolgt hier drin."""

    def __init__(self, file_path: str):
        """Initialisiert die Klasse mit dem Pfad zur CSV-Datei."""
        self.file_path = os.path.abspath(file_path)
        self.extract()

        # Entfernt überflüssige Leerzeichen aus den Spaltennamen
        self.df.columns = self.df.columns.str.strip()

        self.transform()

# extract ---------------------------------------------------------------------------------------------------------

    def extract(self):
        self.df = pd.read_csv(
            self.file_path,
            sep=",",  # Trennzeichen in der CSV-Datei
            encoding="utf-8-sig"  # Kodierung der Datei
        )

# transform ---------------------------------------------------------------------------------------------------------
    def transform(self):
        self.df.sort_values(by=["Year", "Country"], inplace=True)

        self.calc_net_income()
        self.add_sum_percentage_column()
        self.calc_real_values()

    def calc_net_income(self):
        self.df["Net_Income"] = self.df["Average_Monthly_Income"] * 0.01 * self.df["Tax_Rate"]
        self.move_to_neighbour("Average_Monthly_Income", "Net_Income")
    
    def calc_real_values(self):
        suffix = "_Percentage"
        for column in self.df.columns:
            if suffix in column:
                self.df[column.removesuffix(suffix)] = self.df[column] * 0.01 * self.df["Net_Income"]
                self.move_to_neighbour(column, column.removesuffix(suffix))
    
    def move_to_neighbour(self, column, new_neighbour):
        neighbour_index = self.df.columns.get_loc(column)+1
        self.df.insert(neighbour_index, new_neighbour, self.df.pop(new_neighbour))

    # Methode um eine neue Spalte zu erzeugen, was die Summe von allen Spalten mit "Percentage" im Namen ist.
    def add_sum_percentage_column(self):
        """Erzeugt eine neue Spalte, die die Summe aller 'Percentage'-Spalten enthält."""
        percentage_columns = [column for column in self.df.columns if "Percentage" in column]
        self.df["Sum_Percentage"] = self.df[percentage_columns].map(lambda x: float(x) if isinstance(x, str) else x).sum(axis=1)
        self.df["Sum_Percentage"] = self.df["Sum_Percentage"].map(lambda x: float(x))

# load ---------------------------------------------------------------------------------------------------------

    # Methode um die Daten in einer SQLite-Datenbank zu speichern
    def save_to_db(self, db_name: str, table_name: str):
        """Speichert die Daten in einer SQLite-Datenbank."""
        with sqlite3.connect(db_name) as connection:
            self.df.to_sql(
                table_name, connection, if_exists='replace', index=False)
            connection.commit()

# other---------------------------------------------------------------------------------------------------------

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
    
# Main ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Initialisiert die Verarbeitungsklasse mit dem Pfad zur CSV-Datei.
    
    #processor = Datei_Einlesen("src/database/ETL/data/CostOfLivingAndIncome.csv")
    processor = Datei_Einlesen("data/CostOfLivingAndIncome.csv")

    # Speichert die Daten in der SQLite-Datenbank.
    processor.save_to_db('Database1.db', 'CostOfLivingAndIncome')

    # Zeigt die Daten in der SQLite-Datenbank an.
    # processor.show_db('Database1.db', 'CostOfLivingAndIncome')
   