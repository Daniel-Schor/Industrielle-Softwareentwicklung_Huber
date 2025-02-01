import unittest
import sqlite3

class TestNumberRows(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Verbindung zur Datenbank herstellen
        cls.conn = sqlite3.connect(r"Unterricht\Aufagben\Load\FinancialSample.db")
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        # Verbindung schließen
        cls.conn.close()

    def test_number_of_rows(self):
        """Test, ob die Anzahl der Zeilen in FinancialSample genau 700 ist."""
        self.cursor.execute("SELECT COUNT(*) FROM FinancialSample")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 700, f"Erwartete 700 Zeilen, aber {count} gefunden.")

    def test_number_of_rows_falsch(self):
        """Test, ob die Anzahl der Zeilen NICHT ungleich 700 ist (redundant, aber korrekt)."""
        self.cursor.execute("SELECT COUNT(*) FROM FinancialSample")
        count = self.cursor.fetchone()[0]
        self.assertFalse(count != 700, f"Erwartete 700 Zeilen, aber {count} gefunden.")


class HIGH_VALUE(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Verbindung zur Datenbank herstellen
        cls.conn = sqlite3.connect(r"Unterricht\Aufagben\Load\FinancialSample.db") 
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        # Verbindung schließen
        cls.conn.close()
    
    def test_max_sales(self):
        """Test, ob der größte Wert in der Spalte 'Sales' 1159200 ist."""
        self.cursor.execute("SELECT Sales FROM FinancialSample")
        sales_data = self.cursor.fetchall()
        cleaned_sales = [float(sales[0].strip().replace('$', '').replace('.', '').replace(',', '.')) for sales in sales_data]
        
        max_sales = max(cleaned_sales)
        self.assertEqual(max_sales, 1159200, f"Erwartete 1159200, aber {max_sales} gefunden.")
       
    def test_max_sales_false(self):
        """Test, ob der größte Wert in der Spalte 'Sales' NICHT ungleich 1159200 ist (redundant, aber korrekt)."""
        self.cursor.execute("SELECT Sales FROM FinancialSample")
        sales_data = self.cursor.fetchall()
        cleaned_sales = [float(sales[0].strip().replace('$', '').replace('.', '').replace(',', '.')) for sales in sales_data]
        
        max_sales = max(cleaned_sales)
        self.assertFalse(max_sales != 1159200, f"Erwartete 1159200, aber {max_sales} gefunden.")

if __name__ == "__main__":
    unittest.main()