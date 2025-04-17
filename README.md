https://movesmart.dschor.tech/recommendations

# Cost of living and income Analysis Dashboard
---

## Beschreibung
Dies ist ein Projekt für ein Dashboard zur analyse der CostOfLivingAndIncome Datenbasis.

--- 
## Installation und Start
### Projekt installation:
> **Virtuale Umgebung erzeugen**
``` python -m venv env ```

> **env Verzeichnis aktivieren**
``` env\Scripts\activate ```

> **Requirements installieren**
``` pip install -r requirements.txt ```

### Datenbank aufbauen:
> **env Verzeichnis aktivieren**
``` env\Scripts\activate ```

> **ETL ausführen**
``` python src\database\ETL\ETL.py ```

### Projekt starten:
> **env Verzeichnis aktivieren**
``` env\Scripts\activate ```

> **backend (FastAPI) starten** (Man muss im <Industrielle-Softwareentwicklung_Huber> Ordnerverzeichnis sein)
``` uvicorn src.main:app --reload ```

> **frontend (streamlit) starten**
``` streamlit run src\frontend\frontend.py ```

---

FastAPI Swagger UI
http://127.0.0.1:8000/docs


## Credits

> **MODUL:** 
Industrielle Softwareentwickling
> **PRÜFER:** 
Gabriel Huber
> **SEMESTER:**
WiSe 2024/25
> **TEILNEHMER:**
Esrom Johannes, Davide Pedergnana, Daniel Schor, Mavin-Moris Scholl

https://studfrauasde-my.sharepoint.com/:w:/g/personal/uas0021351_stud_fra-uas_de/EWAX0KTq0r5BkuKpy9nOgo8Bo8BAi4kUTt5rwEwdZH8ahQ?e=Qucr5Z

---

# Geschrieben von Daniel Schor und Esrom Johannes und ergänzt von Davide Pedergnana und Mavin-Moris Scholl
