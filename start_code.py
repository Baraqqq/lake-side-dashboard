# import modulen
from pathlib import Path
import json
import pprint
from database_wrapper import Database


# initialisatie

# parameters voor connectie met de database
db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark")


# ===== FUNCTIONAL REQUIREMENTS IMPLEMENTATION =====

# FR2 - Read personnel and maintenance tasks from the database
def fetch_personnel_by_id(db_connection, personnel_id):
    """
    Haal één personeelslid op uit de database op basis van ID.
    
    Args:
        db_connection: Database connectie object
        personnel_id: ID van het personeelslid
        
    Returns:
        dict: Personeelsgegevens of None als niet gevonden
    """
    print(f"[FR2] Ophalen personeelslid met ID: {personnel_id}")
    
    db_connection.connect()
    select_query = "SELECT * FROM personeelslid WHERE id = %s"
    result = db_connection.execute_query(select_query, (personnel_id,))
    db_connection.close()
    
    if result and len(result) > 0:
        personeelslid = result[0]
        print(f"[FR2] Personeelslid gevonden: {personeelslid['naam']}")
        print(f"[FR2] Details: Leeftijd={personeelslid.get('leeftijd', 'Onbekend')}, "
              f"Beroep={personeelslid.get('beroepstype', 'Onbekend')}, "
              f"Bevoegdheid={personeelslid.get('bevoegdheid', 'Onbekend')}")
        return personeelslid
    else:
        print(f"[FR2] Geen personeelslid gevonden met ID: {personnel_id}")
        return None


def fetch_all_tasks(db_connection):
    """
    Haal alle onderhoudstaken op uit de database.
    
    Args:
        db_connection: Database connectie object
        
    Returns:
        list: Lijst met alle onderhoudstaken
    """
    print("[FR2] Ophalen alle onderhoudstaken...")
    
    db_connection.connect()
    select_query = """
        SELECT id, beschrijving, duur, fysieke_belasting, prioriteit, 
               vereiste_bevoegdheid, beroepstype, is_overdekt 
        FROM onderhoudstaak
    """
    result = db_connection.execute_query(select_query)
    db_connection.close()
    
    if result:
        print(f"[FR2] {len(result)} onderhoudstaken gevonden")
        for i, taak in enumerate(result[:3]):  # Toon eerste 3 voor log
            print(f"[FR2] Taak {i+1}: {taak['beschrijving']} "
                  f"(Duur: {taak['duur']}min, Belasting: {taak['fysieke_belasting']}kg)")
        if len(result) > 3:
            print(f"[FR2] ... en {len(result)-3} meer taken")
        return result
    else:
        print("[FR2] Geen onderhoudstaken gevonden")
        return []


# FR4 - Calculate maximum physical load
def calc_max_belasting(leeftijd, override=None):
    """
    Bereken de maximale fysieke belasting op basis van leeftijd.
    
    Args:
        leeftijd: Leeftijd van het personeelslid
        override: Optionele override waarde (verlaagde_fysieke_belasting)
        
    Returns:
        int: Maximale fysieke belasting in kg
    """
    if override is not None:
        print(f"[FR4] Override toegepast: {override}kg (was {leeftijd} jaar)")
        return override
    
    if leeftijd <= 24:
        max_belasting = 25
    elif 25 <= leeftijd <= 50:
        max_belasting = 40
    else:  # >= 51
        max_belasting = 20
    
    print(f"[FR4] Maximale belasting voor leeftijd {leeftijd}: {max_belasting}kg")
    return max_belasting


# FR6 - Select suitable tasks
def selecteer_taken(personeel, taken, max_belasting):
    """
    Selecteer geschikte taken voor een personeelslid.
    
    Args:
        personeel: Dictionary met personeelsgegevens
        taken: List met alle beschikbare taken
        max_belasting: Maximale fysieke belasting voor dit personeelslid
        
    Returns:
        list: Gefilterde lijst met geschikte taken
    """
    print(f"[FR6] Filteren taken voor {personeel['naam']}")
    print(f"[FR6] Criteria: beroepstype={personeel['beroepstype']}, "
          f"bevoegdheid={personeel['bevoegdheid']}, max_belasting={max_belasting}kg")
    
    geschikte_taken = []
    
    for taak in taken:
        # Check beroepstype
        if taak['beroepstype'] != personeel['beroepstype']:
            continue
            
        # Check bevoegdheid (dit zou uitgebreider kunnen zijn met authority levels)
        # Voor nu: eenvoudige string vergelijking
        if taak['vereiste_bevoegdheid'] != personeel['bevoegdheid']:
            continue
            
        # Check fysieke belasting
        if taak['fysieke_belasting'] > max_belasting:
            continue
            
        geschikte_taken.append(taak)
    
    print(f"[FR6] {len(geschikte_taken)} geschikte taken gevonden van {len(taken)} totaal")
    for taak in geschikte_taken:
        print(f"[FR6] - {taak['beschrijving']} ({taak['duur']}min, {taak['fysieke_belasting']}kg)")
    
    return geschikte_taken


# FR3 + NFR4 - Write JSON output
def write_dagtakenlijst_json(personeelsgegevens, weergegevens, dagtaken, filename):
    """
    Schrijf de dagtakenlijst naar JSON bestand in acceptatie formaat.
    
    Args:
        personeelsgegevens: Dictionary met personeelsgegevens
        weergegevens: Dictionary met weergegevens
        dagtaken: List met geselecteerde dagtaken
        filename: Naam van het uitvoer JSON bestand
    """
    print(f"[FR3] Genereren JSON output: {filename}")
    
    # Bereken totale duur
    totale_duur = sum(taak['duur'] for taak in dagtaken)
    
    # Maak dagtakenlijst dictionary
    dagtakenlijst = {
        "personeelsgegevens": {
            "naam": personeelsgegevens['naam'],
            "beroepstype": personeelsgegevens['beroepstype'],
            "bevoegdheid": personeelsgegevens['bevoegdheid'],
            "leeftijd": personeelsgegevens['leeftijd']
        },
        "weergegevens": weergegevens if weergegevens else {},
        "dagtaken": [
            {
                "id": taak['id'],
                "beschrijving": taak['beschrijving'],
                "duur": taak['duur'],
                "fysieke_belasting": taak['fysieke_belasting'],
                "prioriteit": taak['prioriteit'],
                "is_overdekt": taak['is_overdekt']
            } for taak in dagtaken
        ],
        "totale_duur": totale_duur
    }
    
    # Schrijf naar JSON bestand
    with open(filename, 'w', encoding='utf-8') as json_bestand:
        json.dump(dagtakenlijst, json_bestand, indent=4, ensure_ascii=False)
    
    print(f"[FR3] JSON bestand geschreven: {filename}")
    print(f"[FR3] Totale duur: {totale_duur} minuten")
    print(f"[FR3] Aantal taken: {len(dagtaken)}")
    
    return dagtakenlijst


# main

# main

print("=== DATAPUNT 8 - AFTEKENEN VOORTGANG APPLICATIE ===")
print("Implementatie van FR2, FR4, FR6, FR3+NFR4\n")

# Test FR2 - Haal personeelslid en taken op
print("1. TESTEN FR2 - Database queries")
personeelslid = fetch_personnel_by_id(db, 1)
alle_taken = fetch_all_tasks(db)

if not personeelslid:
    print("FOUT: Kon geen personeelslid ophalen. Controleer database connectie.")
    exit(1)

# Test FR4 - Bereken maximale belasting
print("\n2. TESTEN FR4 - Maximale fysieke belasting")
leeftijd = personeelslid['leeftijd']
override = personeelslid.get('verlaagde_fysieke_belasting', None)
max_belasting = calc_max_belasting(leeftijd, override)

# Test FR6 - Selecteer geschikte taken
print("\n3. TESTEN FR6 - Taken selectie")
geschikte_taken = selecteer_taken(personeel=personeelslid, taken=alle_taken, max_belasting=max_belasting)

# Test FR3+NFR4 - Schrijf JSON output
print("\n4. TESTEN FR3+NFR4 - JSON output")
weergegevens = {}  # Voor nu leeg, kan later uitgebreid worden
filename = f"dagtakenlijst_personeelslid_{personeelslid['id']}.json"
dagtakenlijst = write_dagtakenlijst_json(
    personeelsgegevens=personeelslid,
    weergegevens=weergegevens,
    dagtaken=geschikte_taken,
    filename=filename
)

print("\n=== SAMENVATTING TEST RESULTATEN ===")
print(f"Personeelslid: {personeelslid['naam']} (ID: {personeelslid['id']})")
print(f"Leeftijd: {leeftijd} jaar")
print(f"Maximale belasting: {max_belasting}kg {'(override actief)' if override else ''}")
print(f"Totaal beschikbare taken: {len(alle_taken)}")
print(f"Geschikte taken: {len(geschikte_taken)}")
print(f"Totale werktijd: {dagtakenlijst['totale_duur']} minuten")
print(f"JSON bestand: {filename}")

print("\n=== FUNCTIONELE REQUIREMENTS STATUS ===")
print("✓ FR2 - Database queries geïmplementeerd en getest")
print("✓ FR4 - Maximale belasting berekening geïmplementeerd en getest")
print("✓ FR6 - Taken selectie geïmplementeerd en getest")
print("✓ FR3+NFR4 - JSON output geïmplementeerd en getest")

# Legacy code hieronder kan worden weggehaald als alle tests slagen