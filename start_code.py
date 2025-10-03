# import modulen
from pathlib import Path
import json
import pprint
from database_wrapper import Database


# initialisatie

# parameters voor connectie met de database
db = Database(host="localhost", gebruiker="root", wachtwoord="14April2005!?", database="attractiepark")


# Functies voor database operaties

def haal_personeelslid_op(personeelslid_id):
    # Haal één personeelslid op uit de database
    db.connect()
    query = "SELECT * FROM personeelslid WHERE id = " + str(personeelslid_id)
    personeelslid = db.execute_query(query)
    db.close()
    
    if personeelslid:
        print("Personeelslid gevonden:", personeelslid[0]['naam'])
        return personeelslid[0]
    else:
        print("Geen personeelslid gevonden")
        return None

def haal_alle_taken_op():
    # Haal alle onderhoudstaken op uit de database
    db.connect()
    query = "SELECT id, omschrijving, duur, fysieke_belasting, prioriteit, bevoegdheid, beroepstype, is_buitenwerk FROM onderhoudstaak"
    taken = db.execute_query(query)
    db.close()
    
    if taken:
        print("Aantal taken gevonden:", len(taken))
        return taken
    else:
        print("Geen taken gevonden")
        return []


# Functie om maximale belasting te berekenen
def bereken_max_belasting(leeftijd, verlaagde_belasting=None):
    # Als er een verlaagde belasting is ingesteld, gebruik die
    if verlaagde_belasting != None and verlaagde_belasting > 0:
        print("Verlaagde fysieke belasting toegepast:", verlaagde_belasting, "kg")
        return verlaagde_belasting
    
    # Anders bereken op basis van leeftijd
    if leeftijd <= 24:
        max_belasting = 25
    elif leeftijd >= 25 and leeftijd <= 50:
        max_belasting = 40
    else:  # 51 en ouder
        max_belasting = 20
    
    print("Maximale belasting voor leeftijd", leeftijd, "is", max_belasting, "kg")
    return max_belasting


def filter_geschikte_taken(personeelslid, alle_taken, max_belasting):
    # Filter taken die geschikt zijn voor dit personeelslid
    geschikte_taken = []
    
    print("Filteren taken voor", personeelslid['naam'])
    print("Criteria: beroepstype =", personeelslid['beroepstype'], 
          ", bevoegdheid =", personeelslid['bevoegdheid'],
          ", max belasting =", max_belasting, "kg")
    
    for taak in alle_taken:
        # Check 1: Beroepstype moet hetzelfde zijn
        if taak['beroepstype'] != personeelslid['beroepstype']:
            continue
        
        # Check 2: Bevoegdheid moet kloppen
        if taak['bevoegdheid'] != personeelslid['bevoegdheid']:
            continue
        
        # Check 3: Fysieke belasting mag niet te zwaar zijn
        if taak['fysieke_belasting'] > max_belasting:
            continue
        
        # Als alle checks slagen, voeg taak toe
        geschikte_taken.append(taak)
    
    print("Aantal geschikte taken:", len(geschikte_taken))
    return geschikte_taken


def maak_json_bestand(personeelslid, taken, bestandsnaam):
    # Bereken totale duur van alle taken
    totale_duur = 0
    for taak in taken:
        totale_duur = totale_duur + taak['duur']
    
    # Maak de data structuur
    dagtakenlijst = {
        "personeelsgegevens": {
            "naam": personeelslid['naam'],
            "beroepstype": personeelslid['beroepstype'],
            "bevoegdheid": personeelslid['bevoegdheid'],
            "leeftijd": personeelslid['leeftijd']
        },
        "weergegevens": {
            # Hier komen later weergegevens
        },
        "dagtaken": [],
        "totale_duur": totale_duur
    }
    
    # Voeg alle taken toe aan de lijst
    for taak in taken:
        taak_info = {
            "id": taak['id'],
            "omschrijving": taak['omschrijving'],
            "duur": taak['duur'],
            "fysieke_belasting": taak['fysieke_belasting'],
            "prioriteit": taak['prioriteit'],
            "is_buitenwerk": taak['is_buitenwerk']
        }
        dagtakenlijst["dagtaken"].append(taak_info)
    
    # Schrijf naar JSON bestand
    with open(bestandsnaam, 'w') as bestand:
        json.dump(dagtakenlijst, bestand, indent=4)
    
    print("JSON bestand gemaakt:", bestandsnaam)
    print("Totale duur:", totale_duur, "minuten")
    
    return dagtakenlijst


# main

# main

# main

print("Start programma...")

# Stap 1: Haal personeelslid op uit database
personeelslid_id = 1  # We nemen personeelslid met ID 1
personeelslid = haal_personeelslid_op(personeelslid_id)

if personeelslid == None:
    print("FOUT: Geen personeelslid gevonden!")
    exit()

# Stap 2: Haal alle taken op uit database
alle_taken = haal_alle_taken_op()

if len(alle_taken) == 0:
    print("FOUT: Geen taken gevonden!")
    exit()

# Stap 3: Bereken maximale belasting voor dit personeelslid
leeftijd = personeelslid['leeftijd']
verlaagde_belasting = personeelslid['verlaagde_fysieke_belasting']
max_belasting = bereken_max_belasting(leeftijd, verlaagde_belasting)

# Stap 4: Filter taken die geschikt zijn
geschikte_taken = filter_geschikte_taken(personeelslid, alle_taken, max_belasting)

# Stap 5: Maak JSON bestand
bestandsnaam = 'dagtakenlijst_personeelslid_' + str(personeelslid_id) + '.json'
dagtakenlijst = maak_json_bestand(personeelslid, geschikte_taken, bestandsnaam)

# Print samenvatting
print("\n--- SAMENVATTING ---")
print("Personeelslid:", personeelslid['naam'])
print("Leeftijd:", leeftijd, "jaar")
print("Maximale belasting:", max_belasting, "kg")
print("Aantal beschikbare taken:", len(alle_taken))
print("Aantal geschikte taken:", len(geschikte_taken))
print("Totale werktijd:", dagtakenlijst['totale_duur'], "minuten")
print("Bestand gemaakt:", bestandsnaam)

print("Programma voltooid.")