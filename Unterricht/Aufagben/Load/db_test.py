import unittest
import sqlite3
import random
from sqlalchemy import create_engine, Column, String, Integer, Float, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class FinancialSample(Base):
    __tablename__ = 'FinancialSample'
    Country = Column(String, primary_key=True)
    Segment = Column(String)
    Product = Column(String)
    Units_Sold = Column(Integer, name="Units Sold")
    Discount_Band = Column(String, name="Discount Band")
    Manufacturing_Price = Column(Float, name="Manufacturing Price")
    Sale_Price = Column(Float, name="Sale Price")
    Gross_Sales = Column(Float, name="Gross Sales")
    Discounts = Column(Float)
    Sales = Column(Float)
    COGS = Column(Float)
    Profit = Column(Float)
    Date = Column(String)
    MonthYear = Column(String)

class TestFinancialSampleDatabase(unittest.TestCase):
    def setUp(self):
        # Verbindung zur Datenbank herstellen
        self.connection = sqlite3.connect(r'Unterricht\Aufagben\Load\FinancialSample.db')
        self.cursor = self.connection.cursor()
        self.engine = create_engine('sqlite:///Unterricht/Aufagben/Load/FinancialSample.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        # Verbindung zur Datenbank schließen
        self.connection.close()
        self.session.close()

    def test_sample_data(self):
        # Liste der Länder
        countries = ['United States', 'Mexico', 'France', 'Germany', 'Canada']
        
        # Zufälliges Land auswählen
        random_country = random.choice(countries)
        
        # Abfrage mit dem zufälligen Land ausführen
        self.cursor.execute("SELECT * FROM FinancialSample WHERE Country = ?", (random_country,))
        rows = self.cursor.fetchall()
        print(len(rows))
        # Überprüfen, ob die Anzahl der Zeilen korrekt ist
        
        if len(rows) != 140:
            self.fail(f'Die Daten für {random_country} sind nicht korrekt')
        else:
            self.assertTrue(True)
        
    def test_number_of_rows(self):
        # Anzahl der Zeilen in der Tabelle FinancialSample
        self.cursor.execute("SELECT COUNT(*) FROM FinancialSample")
        count = self.cursor.fetchone()[0]
        
        # Überprüfen, ob die Anzahl der Zeilen korrekt ist
        if count != 700:
            self.fail('Die Anzahl der Zeilen in der Tabelle FinancialSample ist nicht korrekt')
        else:
            self.assertTrue(True)

    def test_mont_ger(self):
        # Überprüfe, ob der Eintrag mit Segment = Channel Partners und Country = Germany und Product = Montana 1545 als Wert bei Units Sold hat
        query = select(
            FinancialSample
        ).where(
            FinancialSample.Country == 'Germany',
            FinancialSample.Segment == 'Channel Partners',
            FinancialSample.Product == 'Montana',
            FinancialSample.__table__.c["Units Sold"] == 1545
        )
        
        result = self.session.execute(query).fetchone()
        if result is None:
            self.fail('Eintrag nicht gefunden')
        else:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()