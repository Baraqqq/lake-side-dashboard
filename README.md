# Lake Side Dashboard - Dagtakenlijst Generator

Een Python applicatie voor het genereren van dagtakenlijsten voor medewerkers van attractiepark Lake Side Mania.

## 📋 Wat doet deze applicatie?

Deze applicatie genereert automatisch een dagtakenlijst voor een personeelslid op basis van:
- Hun persoonlijke gegevens (leeftijd, beroepstype, bevoegdheid)
- Beschikbare onderhoudstaken in de database
- Fysieke belasting limieten per leeftijdsgroep
- Taken filtering op basis van geschiktheid

## 🚀 Functionaliteiten

- **Database connectie**: Haalt personeelsgegevens en taken op uit MySQL database
- **Belasting berekening**: Automatische berekening van maximale fysieke belasting op basis van leeftijd
- **Taken filtering**: Selecteert alleen geschikte taken op basis van beroepstype, bevoegdheid en fysieke belasting
- **JSON export**: Genereert een gestructureerd JSON bestand met de dagtakenlijst

## 📁 Project Structuur

```
lake-side-dashboard/
├── start_code.py                              # Hoofdapplicatie
├── database_wrapper.py                        # Database connectie class
├── Database_onderhoudstaken_en_personeelsleden.sql  # Database schema
├── dagtakenlijst_personeelslid_1.json        # Voorbeeld output
└── README.md                                  # Deze documentatie
```

## 🛠️ Installatie & Setup

### 1. Vereisten
- Python 3.8+
- MySQL Server
- mysql-connector-python package

### 2. Database Setup
```sql
# Log in op MySQL als root
mysql -u root -p

# Voer het database script uit
source Database_onderhoudstaken_en_personeelsleden.sql
```

### 3. Python Dependencies
```bash
pip install mysql-connector-python
```

### 4. Database Configuratie
Pas in `start_code.py` de database instellingen aan:
```python
db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark")
```

## ▶️ Gebruik

1. **Start de applicatie:**
```bash
python start_code.py
```

2. **Output:**
   - Console output met stap-voor-stap proces
   - JSON bestand: `dagtakenlijst_personeelslid_X.json`

### Voorbeeld Console Output:
```
Start programma...
Personeelslid gevonden: Piet de Jong
Aantal taken gevonden: 3
Verlaagde fysieke belasting toegepast: 30 kg
Filteren taken voor Piet de Jong
Criteria: beroepstype = Mechanisch Monteur , bevoegdheid = Senior , max belasting = 30 kg
Aantal geschikte taken: 1
JSON bestand gemaakt: dagtakenlijst_personeelslid_1.json
```

## 📄 JSON Output Formaat

```json
{
    "personeelsgegevens": {
        "naam": "Piet de Jong",
        "beroepstype": "Mechanisch Monteur",
        "bevoegdheid": "Senior", 
        "leeftijd": 45
    },
    "weergegevens": {},
    "dagtaken": [
        {
            "id": 3,
            "omschrijving": "Mechanisch onderhoud aan scharnieren",
            "duur": 45,
            "fysieke_belasting": 25,
            "prioriteit": "hoog",
            "is_buitenwerk": 0
        }
    ],
    "totale_duur": 45
}
```

## ⚙️ Configuratie

### Personeelslid wijzigen
Pas in `start_code.py` regel 140 aan:
```python
personeelslid_id = 1  # Verander naar gewenste ID
```

### Fysieke Belasting Regels
- **≤24 jaar**: 25 kg
- **25-50 jaar**: 40 kg  
- **≥51 jaar**: 20 kg
- **Override**: Gebruikt `verlaagde_fysieke_belasting` uit database indien ingesteld

## 🗃️ Database Schema

### Tabel: `personeelslid`
- `id`, `naam`, `werktijd`, `beroepstype`, `bevoegdheid`
- `specialist_in_attracties`, `pauze_opsplitsen`, `leeftijd`
- `verlaagde_fysieke_belasting`

### Tabel: `onderhoudstaak`  
- `id`, `omschrijving`, `duur`, `prioriteit`, `beroepstype`
- `bevoegdheid`, `fysieke_belasting`, `attractie`
- `is_buitenwerk`, `afgerond`, `x_coord`, `y_coord`

## 🔧 Troubleshooting

### Database Connectie Problemen
- Controleer of MySQL service draait
- Verificeer gebruiker/wachtwoord combinatie
- Zorg dat database `attractiepark` bestaat

### Geen Taken Gevonden
- Controleer of onderhoudstaak tabel data bevat
- Verificeer filter criteria (beroepstype/bevoegdheid match)

## 👨‍💻 Ontwikkeling

Dit project is ontwikkeld voor Datapunt 8 van de studie.
Implementeert functionele requirements FR2, FR4, FR6, en FR3+NFR4.

**Auteur**: Ilias  
**Versie**: 1.0  
**Datum**: Oktober 2025
