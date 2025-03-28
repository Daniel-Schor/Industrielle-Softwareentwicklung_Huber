import os
import sqlite3
import uuid
import pandas as pd
import datetime as dt
import yaml
from tabulate import tabulate

# read yaml file
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_FILE = os.path.join(ROOT, "Load/database_configuration.yaml")

with open(CONFIG_FILE, "r") as file:
    CONFIG: dict = dict(yaml.safe_load(file))

FOLDER: str = CONFIG.get("DIR")
NAME: str = CONFIG.get("NAME")

SOURCE_FILE: str = os.path.join(FOLDER, f"{NAME}.csv")
MODIFIED_FILE: str = os.path.join(FOLDER, f"{NAME}_modified.csv")
DB_FILE: str = os.path.join(FOLDER, f"{NAME}.db")
QUERIES: str = CONFIG.get("QUERIES")


def convert_money_to_float(
        price: int
) -> float:
    """
        Wandelt einen Geldbetrag in einen Float-Wert um.
    :param price: Der Geldbetrag, der in einen Float-Wert umgewandelt werden soll
    """

    return float(price.replace(" ", "").replace(".", "").replace(",", ".").replace(
        "$", "").replace("-", "0").replace("(", "").replace(")", ""))


class FinancialDataProcessor:
    """Klasse, um Daten aus einer CSV-Datei zu verarbeiten."""

    _df: pd.DataFrame = None

    def __init__(
            self,
            file_path: str
    ) -> None:
        """
            Initialisiert die Klasse mit dem Pfad zur CSV-Datei.

        :param file_path: Pfad zur CSV-Datei die zum DataFrame konvertiert werden soll.
        """

        self._df = pd.read_csv(file_path, sep=";", encoding="utf-8-sig")
        # Entfernt überflüssige Leerzeichen aus den Spaltennamen
        self._df.columns = self._df.columns.str.strip()

    def transform_date(
            self
    ) -> None:
        """
            Konvertiert die Datumswerte in ein anderes Format und gibt sie aus.
        """
        spalte: str = "Date"

        try:
            self._df[spalte] = self._df[spalte].map(
                lambda x: dt.datetime.strptime(x, "%d.%m.%Y").strftime("%m/%d/%Y"))
        except KeyError:
            print(f"Fehler: Spalte '{spalte}' wurde nicht gefunden.")
        except ValueError:
            print(f"Fehler: Datumsformat in Spalte '{spalte}' ist ungültig.")

    def create_subset(
            self,
            columns: list = ["Product", "Profit", "COGS", "Sales"],
            zeilen: int = 5
    ) -> pd.DataFrame:
        """
            Erstellt und gibt einen neuen DataFrame mit ausgewählten Spalten aus.

        :param columns: Liste der Spalten, die im neuen DataFrame enthalten sein sollen
        :param zeilen: Anzahl der Zeilen, die ausgegeben werden sollen

        :return: DataFrame mit ausgewählten Spalten
        """

        subset = self._df[columns]

        return subset.head(zeilen)

    def combine_columns_to_date(
            self
    ) -> None:
        """
            Kombiniert die Spalten 'Month Number', 'Month Name' und 'Year' zu einer neuen Datenspalte.
        """

        spalte: str = "MonthYear"

        self._df[spalte] = self._df.apply(lambda row:
                                          f'{row["Month Number"]
                                             } {row["Month Name"].strip()}/{row["Year"]}',
                                          axis=1)

        self._df.drop(["Month Number", "Month Name", "Year"],
                      axis=1, inplace=True)

    def find_local_maxima(
            self,
            column: str = "Profit",
            top_maxima: int = 10
    ) -> list:
        """
            Findet und gibt die Positionen der lokalen Maxima in einer bestimmten Spalte aus.

        :param column: Name der Spalte, in der die lokalen Maxima gefunden werden sollen
        :param top_maxima: Anzahl der größten Maxima, die ausgegeben werden sollen

        :return: [Liste der Positionen der lokalen Maxima, Liste der Indexes der größten Maxima]
        """

        try:
            series = self._df[column].map(
                lambda x: convert_money_to_float(x))

            maxima = []
            # Iteriert über die Werte und prüft, ob ein lokales Maximum vorliegt
            for i in range(1, len(series) - 1):
                if series[i] > series[i - 1] and series[i] > series[i + 1]:
                    maxima.append(i)

            maxima_in_series = series[maxima]
            maxima_in_series.sort_values(ascending=False, inplace=True)
            top_maxima = list(maxima_in_series.head(top_maxima).index)

        except KeyError:
            print(f"Fehler: Spalte '{column}' wurde nicht gefunden.")
        except ValueError:
            print(f"Fehler: Werte in Spalte '{column}' sind keine Zahlen.")

        return [maxima, top_maxima]
        """
        print(maxima)

        for i in maxima[0::30]:
            print(f'--\nLokales Maximum: {i}')
            print(
                f'Index: {i-1} Value: {self._df[column][i-1]}')
            print(f'Index: {i} Value: {self._df[column][i]}')
            print(
                f'Index: {i+1} Value: {self._df[column][i+1]}')
        """

    def create_grouped_subset(
            self,
            group_number: int = 2
    ) -> pd.DataFrame:
        """
            Erstellt und gibt einen Datenrahmen aus, der jede X-te Zeile enthält.

        :param group_number:  Gruppennummer X, um jede X-te Zeile auszuwählen.

        :return: DataFrame mit jeder X-ten Zeile
        """

        try:
            grouped_subset = pd.read_csv(
                MODIFIED_FILE,
                sep=";",
                encoding="utf-8-sig",
                skiprows=[i for i in range(
                    1, self._df.shape[0]) if i % int(group_number) != 0],
                header=0
            )
            # grouped_subset = self._df.iloc[0::int(group_number)]

            return grouped_subset
        except ValueError:
            print("Fehler: Gruppennummer muss eine Ganzzahl über 0 sein.")

    def change_discount(
            self,
            column: str = "Discounts",
            path: str = MODIFIED_FILE
    ) -> None:
        """
            Ändert den Rabattwert in der Spalte 'Discounts'.

        :param column: Name der Spalte, in der die Rabattwerte geändert werden sollen
        """

        def categorize_discount(
                discount: str
        ) -> str:
            """
                Kategorisiert den Rabattwert in 'Low', 'Medium' oder 'High'.
                Wenn discount ≤ 200 → Low
                Wenn discount > 200 and <  2000 → Medium
                Wenn discount ≥ 2000 → High

            :param discount: Rabattwert, der kategorisiert werden soll

            :return: Kategorie des Rabattwerts
            """

            discount = convert_money_to_float(discount)
            if discount <= 200:
                return "Low"
            elif 200 < discount < 2000:
                return "Medium"
            else:
                return "High"

        try:
            self._df = pd.read_csv(path, converters={
                column: categorize_discount}, sep=";", encoding="utf-8-sig")

        except KeyError:
            print(f"Fehler: Spalte '{column}' wurde nicht gefunden.")

    def safe_to_csv(
            self,
    ) -> None:
        """
            Speichert den aktuellen DataFrame in einer CSV-Datei.
        """

        # self.print_tail()
        self._df.to_csv(MODIFIED_FILE, sep=";",
                        encoding="utf-8-sig", index=False)


def save_to_db(
    df: pd.DataFrame,
    db_name: str,
    table_name: str
) -> None:
    """
        Speichert die Daten in einer SQLite-Datenbank.

    :param df: DataFrame, der in der Datenbank gespeichert werden soll
    :param db_name: Name der SQLite-Datenbank
    """

    with sqlite3.connect(db_name) as connection:
        df.to_sql(table_name, connection, if_exists='replace', index=False)
        connection.commit()


def show_db(
        db_name: str,
        query: str = None
) -> None:
    """
        Liest die Daten aus der SQLite-Datenbank und gibt sie als Tabelle aus.

    :param db_name: Name der SQLite-Datenbank
    :param query: SQL-Abfrage, die ausgeführt werden soll
    """

    with sqlite3.connect(db_name) as connection:
        df = pd.read_sql_query(query, connection)
        print(tabulate(df, headers='keys', tablefmt='psql'))


def enc(
        text: str
) -> str:
    """
        Verschlüsselt den Text, indem jeder Buchstabe um 1 erhöht wird.

    :param text: Text, der verschlüsselt werden soll
    """

    encrypted_text = "".join(chr(ord(i) + 1) for i in text)
    return encrypted_text


def dec(
        text: str
) -> str:
    """
        Entschlüsselt den Text, indem jeder Buchstabe um 1 verringert wird.

    :param text: Text, der entschlüsselt werden soll
    """

    decrypted_text = "".join(chr(ord(i) - 1) for i in text)
    return decrypted_text


def generate_id():
    """
        Generiert eine ID
    """

    return str(uuid.uuid4())


def split_df(
        df: pd.DataFrame
) -> tuple:
    """
        Teilt den DataFrame in 4 Teile und speichert sie als 4 Tabellen.

    :param df: DataFrame, der in 4 Teile geteilt werden soll

    :return: Tuple aus DataFrames (df_sales, df_product, df_discount, df_month_year)
    """

    # Erstellt eine Tabelle mit den Produkten und generiert eine ID
    df_product = df[["Segment", "Country", "Product"]].drop_duplicates().copy()
    df_product["Product_ID"] = df_product.apply(
        lambda x: generate_id(), axis=1)

    # Erstellt eine Tabelle mit Rabatten und generiert eine ID
    df_discount = df[["Discount Band", "Discounts"]].drop_duplicates().copy()
    df_discount["Discount_ID"] = df_discount.apply(
        lambda x: generate_id(), axis=1)

    # Erstellt eine Tabelle mit Dates und generiert eine ID
    df_date = df[["Date", "MonthYear"]].drop_duplicates().copy()
    df_date["MonthYear_ID"] = df_date.apply(lambda x: generate_id(), axis=1)

    # Erstellt eine Sales Tabelle mit FKs
    df_sales = df[["Units Sold", "Sale Price", "Gross Sales", "COGS", "Profit",
                   "Segment", "Country", "Product", "Discount Band", "MonthYear"]].copy()

    # FKs mappen
    df_sales = df_sales.merge(
        df_product, on=["Segment", "Country", "Product"], how="left")
    df_sales = df_sales.merge(df_discount, on=["Discount Band"], how="left")
    df_sales = df_sales.merge(df_date, on=["MonthYear"], how="left")

    # Benötigte Spalten auswählen
    df_sales = df_sales[["Units Sold", "Sale Price", "Gross Sales",
                         "COGS", "Profit", "Product_ID", "Discount_ID", "MonthYear_ID"]]

    return df_sales, df_product, df_discount, df_date


if __name__ == "__main__":
    # Initialisiert die Verarbeitungsklasse mit dem Pfad zur CSV-Datei.
    processor = FinancialDataProcessor(SOURCE_FILE)

    # Datumsformat umwandeln.
    processor.transform_date()
    processor.safe_to_csv()

    # Ausschnitt mit bestimmten Spalten erstellen.
    subset: pd.DataFrame = processor.create_subset()

    # Spalten zu einer neuen Datenspalte kombinieren.
    processor.combine_columns_to_date()
    processor.safe_to_csv()

    # Lokale Maxima in der Spalte "Profit" finden.
    local_maxima: list = processor.find_local_maxima()[1]

    # Gruppierten Ausschnitt erstellen.
    grouped_subset: pd.DataFrame = processor.create_grouped_subset()

    # Rabattwerte ändern.
    processor.change_discount()
    processor.safe_to_csv()

    # ---------------

    # Lesen des modifizierten CSV-Datei
    df = pd.read_csv(MODIFIED_FILE, sep=";", encoding="utf-8-sig")
    # Teilen des DataFrames in 4 Teile
    df_sales, df_product, df_discount, df_date = split_df(df)

    # DataFrames in SQLite-Datenbank speichern
    save_to_db(df_sales, DB_FILE, "Sales")
    save_to_db(df_product, DB_FILE, "Product")
    save_to_db(df_discount, DB_FILE, "Discount")
    save_to_db(df_date, DB_FILE, "Date")

    username = enc("Admin")
    password = enc("1234")
    print(f"Encoded username: {username}")
    print(f"Encoded password: {password}")

    CONFIG["USERNAME"] = username
    CONFIG["PASSWORD"] = password

    with open(CONFIG_FILE, "w") as file:
        yaml.dump(CONFIG, file)

    with open(CONFIG_FILE, "r") as file:
        CONFIG: dict = dict(yaml.safe_load(file))

    print(f'Decoded username: {dec(CONFIG.get("USERNAME"))}')
    print(f'Decoded username: {dec(CONFIG.get("PASSWORD"))}')
