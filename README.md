- Virtuale Umgebung nur einmalig erzeugen im ..\project Ordner mit:
python -m venv env

- env Verzeichnis aktivieren mit:
env\Scripts\activate

- requirements installieren mit:
pip install -r requirements.txt

- frontend (streamlit) starten mit:
streamlit run src\frontend\frontend.py

- run ETL
python src\database\ETL\ETL.py