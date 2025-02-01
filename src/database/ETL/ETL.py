import os
import sqlite3
import pandas as pd
from tabulate import tabulate
import yaml


class Datei_Einlesen:
    """
        Klasse zum Einlesen einer CSV-Datei und Speichern der Daten in einer SQLite-Datenbank. ETL erfolgt hier drin.

    :param _csv_path: Pfad zur CSV-Datei
    :param _df: DataFrame mit den Daten aus der CSV-Datei
    """

    def __init__(
            self,
            _csv_path: str
    ):
        """
            Initialisiert die Klasse mit dem Pfad zur CSV-Datei.

        :param _csv_path: Pfad zur CSV-Datei, welche die Datenbasis enthält
        """
        self._csv_path = os.path.abspath(_csv_path)
        self.extract()

        # Entfernt überflüssige Leerzeichen aus den Spaltennamen
        self._df.columns = self._df.columns.str.strip()

        self.transform()

# extract ---------------------------------------------------------------------------------------------------------

    def extract(self) -> None:
        """
            Extrahiert die Daten aus der CSV-Datei und speichert sie in einem DataFrame.

        """

        self._df = pd.read_csv(
            self._csv_path,
            sep=",",  # Trennzeichen in der CSV-Datei
            encoding="utf-8-sig"  # Kodierung der Datei
        )

# transform ---------------------------------------------------------------------------------------------------------

    def transform(self) -> None:
        """
            Transformiert die Daten im DataFrame.
                Transformationsprozess:
            1. x
            2. x
            3. x

        """

        self._df.sort_values(by=["Year", "Country"], inplace=True)

        self.calc_net_income()
        self.add_sum("Sum_Percentage", [column for column in self._df.columns if column.endswith(
            "Percentage") and column != "Savings_Percentage"])
        self.calc_real_values()
        self.add_sum(
            "Sum_Costs", [column for column in self._df.columns if column.endswith("Cost")])

    def calc_net_income(self) -> None:
        """
            Berechnet das Nettoeinkommen.
        """

        self._df["Net_Income"] = self._df["Average_Monthly_Income"] * \
            0.01 * self._df["Tax_Rate"]
        self.move_to_neighbour("Average_Monthly_Income", "Net_Income")

    def calc_real_values(self) -> None:
        """
            Berechnet die dollar-Werte für alle Spalten im DataFrame die mit "_Percentage" enden
            und fügt diese als Spalte ohne diesen suffix rechts daneben ein.
        """

        suffix = "_Percentage"
        for column in self._df.columns:
            if suffix in column:
                self._df[column.removesuffix(
                    suffix)] = self._df[column] * 0.01 * self._df["Net_Income"]
                self.move_to_neighbour(column, column.removesuffix(suffix))

    def move_to_neighbour(
            self,
            column,
            new_neighbour
    ) -> None:
        """
            Verschiebt eine Spalte im DataFrame.

        :param column: Spalte woneben die neue Spalte eingefügt werden soll
        :param new_neighbour: Spalte die verschoben werden soll
        """

        neighbour_index = self._df.columns.get_loc(column)+1
        self._df.insert(neighbour_index, new_neighbour,
                        self._df.pop(new_neighbour))

    def add_sum(
            self,
            column_name: str,
            columns: list
    ) -> None:
        """
            Berechnet die Summe der Werte in den Spalten und fügt sie als neue Spalte hinzu.

        :param column_name: Name der neuen Spalte
        :param columns: Liste der Spalten, deren Werte summiert werden sollen
        """

        self._df[column_name] = self._df[columns].sum(axis=1)

# load ---------------------------------------------------------------------------------------------------------

    def save_to_db(
            self,
            db_name: str,
            table_name: str
    ) -> None:
        """
            Speichert die Daten in einer SQLite-Datenbank.

        :param db_name: Name der SQLite-Datenbank
        :param table_name: Name der Tabelle in der SQLite-Datenbank
        """

        with sqlite3.connect(db_name) as connection:
            self._df.to_sql(
                table_name, connection, if_exists='replace', index=False)
            connection.commit()

# other---------------------------------------------------------------------------------------------------------

    # XXX unnötig
    def show_db(
            self,
            db_name: str,
            table_name: str
    ) -> None:
        """
            Liest die Daten aus der SQLite-Datenbank und gibt sie als Tabelle aus.

        :param db_name: Name der SQLite-Datenbank
        :param table_name: Name der Tabelle in der SQLite-Datenbank
        """

        connection = sqlite3.connect(db_name)
        query = f"SELECT * FROM {table_name}"
        _df = pd.read_sql_query(query, connection)
        connection.close()
        print(tabulate(_df, headers='keys', tablefmt='psql'))

    def get_data_from_db(
            db_name: str,
            table_name: str
    ) -> list:
        """
            Liest die Daten aus der SQLite-Datenbank und gibt sie als Liste aus.

        :param db_name: Name der SQLite-Datenbank
        :param table_name: Name der Tabelle in der SQLite-Datenbank
        :return: Liste mit den Daten
        """

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
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    CONFIG_FILE = os.path.join(ROOT, "ETL/ETL_Config.yaml")

    with open(CONFIG_FILE, "r") as file:
        CONFIG: dict = dict(yaml.safe_load(file))

    processor = Datei_Einlesen(
        os.path.join(ROOT, CONFIG["CSV_PATH"]))

    # Speichert die Daten in der SQLite-Datenbank.
    processor.save_to_db(os.path.join(
        ROOT, CONFIG["DB_NAME"]), CONFIG["TABLE_NAME"])

    # Zeigt die Daten in der SQLite-Datenbank an.
    # processor.show_db('Database1.db', 'CostOfLivingAndIncome')
