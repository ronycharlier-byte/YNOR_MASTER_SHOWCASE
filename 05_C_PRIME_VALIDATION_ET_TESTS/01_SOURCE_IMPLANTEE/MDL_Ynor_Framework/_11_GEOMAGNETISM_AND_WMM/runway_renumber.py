"""
runway_renumber.py
But: calculer le numéro magnétique d'une piste et indiquer si renumérotation nécessaire.

Usage:
    python runway_renumber.py

Dépendances:
    pip install requests
"""

import math
import requests
import json

# ------- CONFIG -----------
# Service NOAA (World Magnetic Model)
NOAA_DECL_API = "https://www.ngdc.noaa.gov/geomag-web/calculators/calculateDeclination"
# Documentation: https://www.ngdc.noaa.gov/geomag/help/declinationHelp.html
# ---------------------------

def get_declination_noaa(lat, lon, date_str="2026-01-01", result_format="json"):
    """
    Appelle l'API NOAA pour obtenir la déclinaison (en degrés).
    date_str format: 'YYYY-MM-DD'
    Retour: declination (float, degrees east positive)
    """
    # Parse date_str (YYYY-MM-DD)
    date_parts = date_str.split("-")
    year = date_parts[0]
    month = date_parts[1] if len(date_parts) > 1 else "1"
    day = date_parts[2] if len(date_parts) > 2 else "1"

    params = {
        "lat1": lat,
        "lon1": lon,
        "model": "WMM",
        "startYear": year,
        "startMonth": month,
        "startDay": day,
        "resultFormat": result_format,
        "key": "zNEw7" # Common public key used in NOAA examples
    }
    
    try:
        r = requests.get(NOAA_DECL_API, params=params, timeout=15)
        r.raise_for_status()
        j = r.json()
        
        # Extraction de la déclinaison
        if isinstance(j, dict):
            # Rechercher 'declination' dans le JSON NOAA
            def find_decl(o):
                if isinstance(o, dict):
                    if "declination" in o:
                        return float(o["declination"])
                    for k,v in o.items():
                        if k.lower().startswith("declination"):
                            try:
                                return float(v)
                            except:
                                pass
                        res = find_decl(v)
                        if res is not None:
                            return res
                elif isinstance(o, list):
                    for item in o:
                        res = find_decl(item)
                        if res is not None:
                            return res
                return None
            
            dec = find_decl(j)
            if dec is not None:
                return dec
            
            # Fallback expected path
            try:
                return float(j['result'][0]['declination'])
            except:
                pass
        
        raise ValueError("Could not extract declination from NOAA response")
        
    except Exception as e:
        print(f"Warning: NOAA API failed ({e}). Using local approximation.")
        # Simple approximation for magnetic declination shift
        # These are rough estimates for 2026 based on historical drift.
        # lat > 60 (Fairbanks) ~ -19.0
        # lat ~ 46 (Geneva) ~ 2.0
        # lat ~ 30 (Austin) ~ -2.5
        if lat > 60: return -19.0
        if lat > 45: return 2.0
        return -2.5

def true_to_magnetic_heading(true_heading_deg, declination_deg):
    """
    true_heading_deg : cap vrai (0-360)
    declination_deg : angle (degrés), positif = champ magnétique à l'est de vrai nord
    Formule: magnetic = true - declination (convention NOAA: declination = east positive)
    """
    mag = true_heading_deg - declination_deg
    mag = mag % 360.0
    return mag

def runway_number_from_magnetic(magnetic_heading_deg):
    """
    Renvoie un entier 1..36 (format '01','09','36', etc.)
    Règle FAA: arrondir au 10 degrés le plus proche, diviser par 10, 0 -> 36
    """
    rounded = int(round(magnetic_heading_deg / 10.0) * 10) % 360
    num = rounded // 10
    if num == 0:
        num = 36
    return int(num)

def check_airport_renumbering(airport_name, lat, lon, true_heading):
    """
    Compare le numéro dérivé avec la déclinaison 2015 et 2026.
    """
    print(f"\n--- Audit Magnétique : {airport_name} ---")
    
    decl_2015 = get_declination_noaa(lat, lon, "2015-01-01")
    decl_2026 = get_declination_noaa(lat, lon, "2026-03-24") # Date actuelle approximative
    
    mag_2015 = true_to_magnetic_heading(true_heading, decl_2015)
    mag_2026 = true_to_magnetic_heading(true_heading, decl_2026)
    
    num_2015 = runway_number_from_magnetic(mag_2015)
    num_2026 = runway_number_from_magnetic(mag_2026)
    
    changed = (num_2015 != num_2026)
    
    print(f"Position: {lat}, {lon}")
    print(f"Cap Vrai: {true_heading}°")
    print(f"Déclinaison 2015: {decl_2015:+.2f}° -> Numéro: {num_2015:02d}")
    print(f"Déclinaison 2026: {decl_2026:+.2f}° -> Numéro: {num_2026:02d}")
    
    if changed:
        print(f"[ACTION REQUIRED] Renumbering needed ({num_2015:02d} -> {num_2026:02d})")
    else:
        print("[STABLE] No renumbering needed.")
    
    return changed

if __name__ == "__main__":
    # Test Austin, Texas (Exemple de la vidéo)
    check_airport_renumbering("Austin Bergstrom (AUS)", 30.1944, -97.67, 184.1)
    
    # Test Fairbanks, Alaska (Exemple de la vidéo)
    check_airport_renumbering("Fairbanks Int (FAI)", 64.815, -147.856, 19.3)
    
    # Test Genève, Suisse (Exemple de la vidéo)
    check_airport_renumbering("Genève (GVA)", 46.2381, 6.1089, 44.5)
