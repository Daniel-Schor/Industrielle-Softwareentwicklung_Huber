import os
import sqlite3
import pandas as pd
from tabulate import tabulate
# SQLite3 Editor Extension installieren.

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

        # Zwei dezimalstellen für numerische Werte (außer "Year" spalte)
        if "Year" not in self.data_frame.columns:
            self.data_frame = self.data_frame.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
        
        # Spalten mit den Wörter "Tax" oder "Percentage" werden als Prozent formatiert, die mit Cost oder Income mit $.
        # Bei manchen Spalten sind sowohl das Wort "Tax" als "Cost" enthalten, da kommt dann die erste Bedingung.
        for column in self.data_frame.columns:
            if any(keyword in column for keyword in ["Tax", "Percentage"]):
                self.data_frame[column] = self.data_frame[column].map(lambda x: f"{str(x)}%" if isinstance(x, (int, float, str)) else x)
            elif any(keyword in column for keyword in ["Cost", "Income"]):
                self.data_frame[column] = self.data_frame[column].map(lambda x: f"${str(x)}" if isinstance(x, (int, float, str)) else x)
            
    #Methode um die Daten in einer SQLite-Datenbank zu speichern
    def save_to_db(self, db_name: str, table_name: str):
        """Speichert die Daten in einer SQLite-Datenbank."""
        connection = sqlite3.connect(db_name)
        self.data_frame.to_sql(table_name, connection, if_exists='replace', index=False)
        connection.commit()
        connection.close()

    #Methode um die Daten aus der SQLite-Datenbank anzuzeigen. Ist eigentlich nicht notwendig, wir müssen entscheiden ob wir das drin lassen.
    def show_db(self, db_name: str, table_name: str):
        """Liest die Daten aus der SQLite-Datenbank und gibt sie als Tabelle aus."""
        connection = sqlite3.connect(db_name)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, connection)
        connection.close()
        print(tabulate(df, headers='keys', tablefmt='psql'))

if __name__ == "__main__":
    # Initialisiert die Verarbeitungsklasse mit dem Pfad zur CSV-Datei.
    processor = Datei_Einlesen(r"data\CostOfLivingAndIncome.csv")
    
    # Speichert die Daten in der SQLite-Datenbank.
    processor.save_to_db('Database1.db', 'CostOfLivingAndIncome')
    
    # Zeigt die Daten in der SQLite-Datenbank an.
    processor.show_db('Database1.db', 'CostOfLivingAndIncome')