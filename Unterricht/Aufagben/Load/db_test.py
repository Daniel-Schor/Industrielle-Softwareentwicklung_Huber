import unittest
import sqlite3
import random
import locale


class DatabaseConnectionTest(unittest.TestCase):
    """Testet, ob die Verbindung zur Datenbank erfolgreich hergestellt werden kann."""

    @classmethod
    def setUpClass(cls):
        """Datenbankverbindung herstellen"""
        cls.conn = sqlite3.connect(r"Unterricht\Aufagben\Load\FinancialSample.db")
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        """Datenbankverbindung schließen"""
        cls.conn.close()

    def test_database_connection(self):
        """Prüft, ob die Datenbankverbindung aktiv ist"""
        self.assertIsNotNone(self.conn, "Datenbankverbindung konnte nicht hergestellt werden.")


class RowCountTest(unittest.TestCase):
    """Testet die Anzahl der Zeilen in der Tabelle."""

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(r"Unterricht\Aufagben\Load\FinancialSample.db")
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_number_of_rows(self):
        """Test, ob genau 700 Zeilen in der Tabelle sind."""
        self.cursor.execute("SELECT COUNT(*) FROM FinancialSample")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 700, f"Erwartete 700 Zeilen, aber {count} gefunden.")

    def test_number_of_rows_falsch(self):
        """Test, ob die Anzahl der Zeilen NICHT ungleich 700 ist (redundant)."""
        self.cursor.execute("SELECT COUNT(*) FROM FinancialSample")
        count = self.cursor.fetchone()[0]
        self.assertFalse(count != 700, f"Erwartete 700 Zeilen, aber {count} gefunden.")


class SalesValueTest(unittest.TestCase):
    """Testet die Sales-Spalte auf maximale Werte."""

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(r"Unterricht\Aufagben\Load\FinancialSample.db")
        cls.cursor = cls.conn.cursor()
        locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')  # Deutsches Zahlenformat setzen

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_max_sales(self):
        """Test, ob der höchste Sales-Wert genau 1.159.200 beträgt."""
        self.cursor.execute("SELECT Sales FROM FinancialSample")
        sales_data = self.cursor.fetchall()
        cleaned_sales = [locale.atof(sales[0].strip().replace('$', '')) for sales in sales_data]
        max_sales = max(cleaned_sales)
        self.assertEqual(max_sales, 1159200, f"Erwartete 1159200, aber {max_sales} gefunden.")

    def test_max_sales_false(self):
        """Test, ob der höchste Sales-Wert NICHT ungleich 1.159.200 ist (redundant)."""
        self.cursor.execute("SELECT Sales FROM FinancialSample")
        sales_data = self.cursor.fetchall()
        cleaned_sales = [locale.atof(sales[0].strip().replace('$', '')) for sales in sales_data]
        max_sales = max(cleaned_sales)
        self.assertFalse(max_sales != 1159200, f"Erwartete 1159200, aber {max_sales} gefunden.")


class RandomDataCheckTest(unittest.TestCase):
    """Stichprobenartige Überprüfung zufälliger Zeilen."""

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(r"Unterricht\Aufagben\Load\FinancialSample.db")
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_random_data_check(self):
        """Prüft 5 zufällige Zeilen, ob sie gültige Daten enthalten."""
        self.cursor.execute("SELECT * FROM FinancialSample")
        rows = self.cursor.fetchall()
        self.assertGreater(len(rows), 0, "Keine Daten in der Tabelle gefunden.")

        sample_rows = random.sample(rows, min(5, len(rows)))
        for row in sample_rows:
            self.assertIsInstance(row[0], str, "Erwartete eine Zeichenkette in der ersten Spalte.")
            self.assertIsInstance(row[1], str, "Erwartete eine Zeichenkette in der zweiten Spalte.")


class ColumnIntegrityTest(unittest.TestCase):
    """Testet, ob alle wichtigen Spalten vorhanden sind."""

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(r"Unterricht\Aufagben\Load\FinancialSample.db")
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_columns_exist(self):
        """Überprüft, ob die erforderlichen Spalten existieren."""
        self.cursor.execute("PRAGMA table_info(FinancialSample)")
        columns = [column[1] for column in self.cursor.fetchall()]
        required_columns = ["Segment", "Country", "Product", "Sales", "Profit"]

        for col in required_columns:
            self.assertIn(col, columns, f"Spalte '{col}' fehlt in der Datenbank.")


if __name__ == "__main__":
    unittest.main()
