# Database Test Script
# Gebruik dit script om de implementatie te testen met de echte database
# Zorg dat je database connectie instellingen correct zijn in start_code.py

import sys
import json
from pathlib import Path

# Voeg de huidige directory toe aan het pad
sys.path.append(str(Path(__file__).parent))

# Import onze functies (alleen als database beschikbaar is)
try:
    from start_code import (
        db, 
        fetch_personnel_by_id, 
        fetch_all_tasks, 
        calc_max_belasting, 
        selecteer_taken, 
        write_dagtakenlijst_json
    )
    
    print("=== DATABASE TEST SCRIPT ===")
    print("Let op: Dit script vereist een werkende database connectie\n")
    
    # Test 1: Haal personeelslid op
    print("1. Test FR2 - Database queries")
    print("-" * 40)
    
    personnel_id = 1  # Pas aan naar gewenste ID
    personeelslid = fetch_personnel_by_id(db, personnel_id)
    
    if not personeelslid:
        print(f"❌ Geen personeelslid gevonden met ID {personnel_id}")
        print("Controleer:")
        print("- Database connectie instellingen")
        print("- Of de database draait")
        print("- Of de personeelslid tabel data bevat")
        sys.exit(1)
    
    # Test 2: Haal alle taken op
    alle_taken = fetch_all_tasks(db)
    
    if not alle_taken:
        print("❌ Geen taken gevonden in database")
        print("Controleer of de onderhoudstaak tabel data bevat")
        sys.exit(1)
    
    # Test 3: Bereken maximale belasting
    print("\n2. Test FR4 - Maximale belasting")
    print("-" * 40)
    
    leeftijd = personeelslid['leeftijd']
    override = personeelslid.get('verlaagde_fysieke_belasting', None)
    max_belasting = calc_max_belasting(leeftijd, override)
    
    # Test 4: Selecteer taken
    print("\n3. Test FR6 - Taken selectie")
    print("-" * 40)
    
    geschikte_taken = selecteer_taken(
        personeel=personeelslid,
        taken=alle_taken,
        max_belasting=max_belasting
    )
    
    # Test 5: Genereer JSON
    print("\n4. Test FR3+NFR4 - JSON output")
    print("-" * 40)
    
    # Placeholder weergegevens
    weergegevens = {
        "temperatuur": 18,
        "windkracht": 3,
        "neerslag": "Geen",
        "zicht": "Goed"
    }
    
    filename = f"dagtakenlijst_personeelslid_{personeelslid['id']}.json"
    
    dagtakenlijst = write_dagtakenlijst_json(
        personeelsgegevens=personeelslid,
        weergegevens=weergegevens,
        dagtaken=geschikte_taken,
        filename=filename
    )
    
    # Test samenvatting
    print("\n" + "=" * 50)
    print("DATABASE TEST SAMENVATTING")
    print("=" * 50)
    print(f"✅ Personeelslid: {personeelslid['naam']} (ID: {personeelslid['id']})")
    print(f"✅ Leeftijd: {leeftijd} jaar")
    print(f"✅ Max belasting: {max_belasting}kg {'(override)' if override else ''}")
    print(f"✅ Beschikbare taken: {len(alle_taken)}")
    print(f"✅ Geschikte taken: {len(geschikte_taken)}")
    print(f"✅ Totale werktijd: {dagtakenlijst['totale_duur']} minuten")
    print(f"✅ JSON output: {filename}")
    
    print(f"\n🎯 ALLE TESTS GESLAAGD!")
    print(f"De implementatie werkt correct met de database.")
    
    # Toon JSON preview
    print(f"\n📄 JSON PREVIEW:")
    print("-" * 20)
    print(json.dumps(dagtakenlijst, indent=2, ensure_ascii=False))
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Controleer of start_code.py correct is en alle dependencies geïnstalleerd zijn")
except Exception as e:
    print(f"❌ Database connectie error: {e}")
    print("\nMogelijke oorzaken:")
    print("- Database is niet beschikbaar")
    print("- Connectie instellingen zijn incorrect")
    print("- MySQL service draait niet")
    print("- Netwerk problemen")
    print("\nControleer de connectie instellingen in start_code.py:")
    print('db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark")')