import pandas as pd
import datetime as dt


class FinancialDataProcessor:
    """Klasse, um Daten aus einer CSV-Datei zu verarbeiten."""

    def __init__(self, file_path: str):
        """Initialisiert die Klasse mit dem Pfad zur CSV-Datei."""
        self.file_path = file_path
        self.data_frame = pd.read_csv(
            self.file_path,
            sep=";",  # Trennzeichen in der CSV-Datei
            encoding="utf-8-sig"  # Kodierung der Datei, um Umlaute korrekt darzustellen
        )
        # Entfernt überflüssige Leerzeichen aus den Spaltennamen
        self.data_frame.columns = self.data_frame.columns.str.strip()

    def print_tail(self, num_rows: int = 10):
        """Gibt die letzten Zeilen des Datenrahmens auf der Konsole aus."""
        print(self.data_frame.tail(num_rows))

    def print_date_column(self):
        """Konvertiert die Datumswerte in ein anderes Format und gibt sie aus."""
        if "Date" in self.data_frame.columns:
            for date in self.data_frame["Date"]:
                # Konvertiert das Datum von "dd.mm.yyyy" in "mm.dd.yyyy"
                formatted_date = dt.datetime.strptime(date, "%d.%m.%Y").strftime("%m.%d.%Y")
                print(formatted_date)
        else:
            print("Fehler: 'Date'-Spalte wurde nicht gefunden.")

    def create_subset(self):
        """Erstellt und gibt einen neuen Datenrahmen mit ausgewählten Spalten aus."""
        # Wählt die Spalten "Product", "Profit", "COGS" und "Sales" aus
        subset = self.data_frame[["Product", "Profit", "COGS", "Sales"]]
        print(subset.head(5))  # Gibt die ersten 5 Zeilen des neuen Datenrahmens aus

    def combine_columns_to_date(self):
        """Kombiniert die Spalten 'Month Number', 'Month Name' und 'Year' zu einer neuen Datenspalte."""
        # Prüft, ob die erforderlichen Spalten im Datenrahmen existieren
        if all(col in self.data_frame.columns for col in ["Month Number", "Month Name", "Year"]):
            # Erstellt die neue Spalte 'Datum' durch Kombination der anderen Spalten
            self.data_frame["Datum"] = (
                self.data_frame["Month Number"].astype(str)  # Monat als Zahl
                + "." +
                self.data_frame["Month Name"]  # Monatsname
                + "." +
                self.data_frame["Year"].astype(str)  # Jahr
            )
            print(self.data_frame["Datum"])  # Gibt die neue Spalte auf der Konsole aus
        else:
            print("Fehler: Die erforderlichen Spalten für 'Datum' wurden nicht gefunden.")

    def find_local_maxima(self, column: str = "Profit"):
        """Findet und gibt die Positionen der lokalen Maxima in einer bestimmten Spalte aus."""
        if column in self.data_frame.columns:
            maxima = []
            # Iteriert über die Werte und prüft, ob ein lokales Maximum vorliegt
            for i in range(1, len(self.data_frame[column]) - 1):
                if self.data_frame[column][i] > self.data_frame[column][i - 1] and self.data_frame[column][i] > self.data_frame[column][i + 1]:
                    maxima.append(i)
            print(maxima)
        else:
            print(f"Fehler: Spalte '{column}' wurde nicht gefunden.")

    def create_grouped_subset(self, group_number: int):
        """Erstellt und gibt einen Datenrahmen aus, der jede X-te Zeile enthält."""
        if group_number > 0:
            grouped_subset = self.data_frame.iloc[::group_number, :]
            print(grouped_subset)
        else:
            print("Fehler: Gruppennummer muss größer als 0 sein.")

    def change_discount(self, column: str = "Discounts"):
        """Ändert den Rabattwert in der Spalte 'Discounts'."""
        if column in self.data_frame.columns:
            # Ausgabe der Zeilen vor der Umwandlung, als Vergleich.
            print(self.data_frame[column][52:62])

            def categorize_discount(discount):
                discount = discount.replace("$", "").replace("-", "0").replace(".", "").replace(",", ".").strip()
                discount = float(discount)
                if discount < 200:
                    return "Low"
                elif 200 < discount < 2000:
                    return "Medium"
                else:
                    return "High"
            
            self.data_frame[column] = self.data_frame[column].apply(categorize_discount)
            # Ausgabe der gewählten Zeilen der Spalte 'Discounts' nach der Umwandlung.
            print(self.data_frame[column][52:62])
            

if __name__ == "__main__":
    # Initialisiert die Verarbeitungsklasse mit dem Pfad zur CSV-Datei.
    processor = FinancialDataProcessor("Aufagben/Transformation/FinancialSample.csv")

    # Aufgabe 1: Letzte Zeilen ausgeben.
    processor.print_tail()

    # Aufgabe 2: Datumsformat umwandeln.
    processor.print_date_column()

    # Aufgabe 3: Ausschnitt mit bestimmten Spalten erstellen.
    processor.create_subset()

    # Aufgabe 4: Spalten zu einer neuen Datenspalte kombinieren.
    processor.combine_columns_to_date()

    # Aufgabe 5: Lokale Maxima in der Spalte "Profit" finden.
    processor.find_local_maxima()

    # Aufgabe 6: Gruppierten Ausschnitt erstellen.
    group_number = int(input("Gib eine beliebige Gruppennummer ein: "))
    processor.create_grouped_subset(group_number)

    #Aufgabe 7: Rabattwerte ändern.
    processor.change_discount()
