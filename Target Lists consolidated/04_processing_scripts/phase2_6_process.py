"""
Phases 2-6: Tier finalization, URL enrichment, Contact normalization,
Pipeline scoring, and HubSpot-ready CSV export.
"""
import pandas as pd
import re
import os
import json
from collections import defaultdict

BASE = r"C:\Users\mamowi\Clients\AI-KIP"
INPUT = os.path.join(BASE, "master_target_list_phase1.csv")

# -- URL ENRICHMENT DATA ----------------------------------------------------
# These will be populated from the web search agents' results.
# For any remaining gaps, we flag them in the gaps report.

URL_ENRICHMENT_TIER1 = {
    "Reifenhäuser Group": "reifenhauser.com",
    "Reifenhuser Group": "reifenhauser.com",
    "Pfleiderer GmbH": "pfleiderer.com",
    "Doppelmayr Holding": "doppelmayr.com",
    "ifm electronic": "ifm.com",
    "Igus GmbH": "igus.de",
    "Weidmüller": "weidmueller.com",
    "Weidmller": "weidmueller.com",
    "Koenig & Bauer AG": "koenig-bauer.com",
    "Viega GmbH": "viega.de",
    "Herrenknecht AG": "herrenknecht.com",
    "Engel Austria GmbH": "engelglobal.com",
    "STO SE & Co. KGaA": "sto.de",
    "GEMÜ": "gemu-group.com",
    "GEM": "gemu-group.com",
    "EOS GmbH": "eos.info",
    "Arburg GmbH": "arburg.com",
    "Winterhalter": "winterhalter.com",
    "BHS Corrugated Maschinen- und Anlagenbau GmbH": "bhs-world.com",
    "BHS Corrugated": "bhs-world.com",
    "Windmoeller & Hoelscher Group": "wh.group",
    "Windmöller & Hölscher": "wh.group",
    "PERI GmbH": "peri.com",
    "Lapp Gruppe (U.I. Lapp GmbH)": "lapp.com",
    "Lapp Gruppe": "lapp.com",
    "SEW-Eurodrive GmbH & Co KG": "sew-eurodrive.de",
    "SEW-Eurodrive": "sew-eurodrive.de",
    "Multivac Sepp Hagenmueller SE & Co. KG": "multivac.com",
    "Multivac": "multivac.com",
    "Festo SE & Co. KG": "festo.com",
    "Festo": "festo.com",
    "Sick AG": "sick.com",
    "Endress+Hauser Group": "endress.com",
    "Endress+Hauser": "endress.com",
    "Brose Fahrzeugteile SE & Co. KG": "brose.com",
    "Brose": "brose.com",
    "Schuler AG (now Andritz Schuler)": "schulergroup.com",
    "Schuler AG": "schulergroup.com",
    "Phoenix Contact GmbH & Co. KG": "phoenixcontact.com",
    "Phoenix Contact": "phoenixcontact.com",
}

URL_ENRICHMENT_TIER23 = {
    "DELO Industrie Klebstoffe": "delo-adhesives.com",
    "EMKA Beschlagteile": "emka.com",
    "Harro Höfliger": "hfruns.com",
    "Harro Hoefliger Verpackungsmaschinen GmbH": "hfruns.com",
    "Harro Hfliger": "hfruns.com",
    "Gerhard Schubert GmbH": "gerhard-schubert.de",
    "Gerhard Schubert GmbH Verpackungsmaschinen": "gerhard-schubert.de",
    "Blickle Räder + Rollen": "blickle.com",
    "Blickle Raeder + Rollen GmbH u. Co. KG": "blickle.com",
    "Blickle Rder + Rollen": "blickle.com",
    "Schmalz GmbH": "schmalz.com",
    "Schmalz GmbH (J. Schmalz GmbH)": "schmalz.com",
    "SÜDPACK SE": "suedpack.com",
    "SDPACK SE": "suedpack.com",
    "SUEDPACK SE & Co. KG": "suedpack.com",
    "August Steinmeyer GmbH": "steinmeyer.com",
    "Dr. O.K. Wack Chemie / ZESTRON": "zestron.com",
    "ALANOD GmbH": "alanod.com",
    "Elma Schmidbauer GmbH": "elma-ultrasonic.com",
    "BJB GmbH": "bjb.com",
    "Otto Männer GmbH": "otto-maenner.de",
    "Otto Mnner GmbH": "otto-maenner.de",
    "Illig Maschinenbau": "illig.com",
    "Andreas Hettich GmbH": "hettichlab.com",
    "BSW Berleburger Schaumstoffwerk": "berleburger.de",
    "OMICRON electronics": "omicronenergy.com",
    "Wintersteiger AG": "wintersteiger.com",
    "Erowa AG": "erowa.com",
    "Wenglor Sensoric": "wenglor.com",
    "Wenglor Sensoric GmbH": "wenglor.com",
    "Plasmatreat GmbH": "plasmatreat.de",
    "Hawo GmbH": "hawo.com",
    "Erwin Halder KG": "halder.com",
    "Theegarten-Pactec": "theegarten-pactec.de",
    "KOEPFER Zahnradtechnik": "koepfer.com",
    "Braunform GmbH": "braunform.com",
    "Nagel Technologies": "nagel.com",
    "Nagel Technologies GmbH": "nagel.com",
    "Gruner AG": "gruner.de",
    "Poly-clip System": "polyclip.com",
    "Poly-clip System GmbH": "polyclip.com",
    "aquatherm GmbH": "aquatherm.de",
    "Puls GmbH": "pulspower.com",
    "Turck Duotec GmbH": "turck-duotec.com",
    "Novexx Solutions": "novexx.com",
    "Marbach Werkzeugbau": "marbach.com",
    "Marbach Werkzeugbau GmbH": "marbach.com",
    "LASCO Umformtechnik": "lasco.com",
    "Ruf Maschinenbau GmbH": "brikettieren.de",
    "microsonic GmbH": "microsonic.de",
    "Greif-Velox Maschinenfabrik GmbH": "greif-velox.com",
    "Greif-Velox Maschinenfabrik": "greif-velox.com",
    "Sensitec GmbH": "sensitec.com",
    "Proxitron GmbH": "proxitron.de",
    "Klaschka GmbH": "klaschka.de",
    "Memmert GmbH": "memmert.com",
    "Wandres GmbH micro-cleaning": "wandres.com",
    "Wandres GmbH": "wandres.com",
    "Paul Maschinenfabrik GmbH": "paul-gruppe.de",
    "Peter Huber Kältemaschinenbau SE": "huber-online.com",
    "Peter Huber Kaeltemaschinenbau SE": "huber-online.com",
    "Hahn Gasfedern GmbH": "hahn-gasfedern.de",
    "KRIWAN Industrie-Elektronik": "kriwan.com",
    "KRIWAN Industrie-Elektronik GmbH": "kriwan.com",
    "SIKO GmbH": "siko-global.com",
    "Christian Maier GmbH": "maier-heidenheim.de",
    "Christian Maier GmbH & Co. KG": "maier-heidenheim.de",
    "Carl Hirschmann GmbH": "carlhirschmann.de",
    "Beck Packautomaten GmbH": "beck-packautomaten.de",
    "Rego-Fix AG": "rego-fix.com",
    "Sylvac SA": "sylvac.ch",
    "Schiebel Elektronische Geräte": "schiebel.net",
    "Schiebel Elektronische Gerte": "schiebel.net",
    "Schiebel Elektronische Geraete GmbH": "schiebel.net",
    "Linsinger Maschinenbau": "linsinger.com",
    "Linsinger Maschinenbau GmbH": "linsinger.com",
    "Pollmann International": "pollmann.at",
    "Pollmann International GmbH": "pollmann.at",
    "Haidlmair GmbH": "haidlmair.at",
    "Wittmann Technology": "wittmann-group.com",
    "Wittmann Technology GmbH": "wittmann-group.com",
    "IFE Aufbereitungstechnik": "ife-bulk.com",
    "IFE Aufbereitungstechnik GmbH": "ife-bulk.com",
    "Pankl Racing Systems": "pfracing.com",
    "Pankl Racing Systems AG": "pfracing.com",
    # Additional remaining
    "Roemheld GmbH": "roemheld.de",
    "Römheld GmbH": "roemheld.de",
    "Gebr. Kemper GmbH": "kemper-olpe.de",
    "Helmut Fischer GmbH": "helmut-fischer.com",
    "Mink Bürsten": "mink-buersten.com",
    "Mink Buersten (August Mink GmbH & Co. KG)": "mink-buersten.com",
    "Schoeck Bauteile": "schoeck.com",
    "Schoeck Bauteile GmbH": "schoeck.com",
    "EMKA Beschlagteile GmbH & Co. KG": "emka.com",
    "Leistritz AG": "leistritz.com",
    "Klingspor AG": "klingspor.de",
    "G. Siempelkamp GmbH & Co. KG": "siempelkamp.com",
    "Siempelkamp GmbH": "siempelkamp.com",
    "Pilz GmbH & Co. KG": "pilz.com",
    "Pilz GmbH": "pilz.com",
    "Wafios AG": "wafios.com",
    "GEMUE Gebr. Mueller Apparatebau GmbH & Co. KG": "gemu-group.com",
    "Leitz GmbH & Co. KG": "leitz.org",
    "Leitz GmbH": "leitz.org",
    "Groz-Beckert KG": "groz-beckert.com",
    "Klingelnberg AG": "klingelnberg.com",
    "OPTIMA packaging group GmbH": "optima-packaging.com",
    "OPTIMA packaging group": "optima-packaging.com",
    "Duerr Dental SE": "duerrdental.com",
    "Dürr Dental SE": "duerrdental.com",
    "Maschinenfabrik Reinhausen GmbH": "reinhausen.com",
    "Maschinenfabrik Reinhausen": "reinhausen.com",
    "Pepperl+Fuchs SE": "pepperl-fuchs.com",
    "Pepperl+Fuchs": "pepperl-fuchs.com",
    "Brueckner Maschinenbau GmbH & Co. KG": "brueckner.com",
    "Brückner Maschinenbau": "brueckner.com",
    "Hugo Beck Maschinenbau GmbH": "hugobeck.de",
    "Hugo Beck Maschinenbau": "hugobeck.de",
    "Rampf Holding GmbH": "rampf-group.com",
    "Weicon GmbH & Co. KG": "weicon.de",
    "Weicon GmbH": "weicon.de",
    "Foerster Group": "foerstergroup.com",
    "Förster Group": "foerstergroup.com",
    "Zoller GmbH": "zoller.info",
    "Herbert Haenchen GmbH": "haenchen.de",
    "Herbert Hänchen GmbH": "haenchen.de",
    "Stuewe GmbH": "stuewe.de",
    "Stüwe GmbH": "stuewe.de",
    "OTT-JAKOB Spanntechnik GmbH": "ott-jakob.de",
    "OTT-JAKOB Spanntechnik": "ott-jakob.de",
    "JAKOB Antriebstechnik GmbH": "jakobantriebstechnik.de",
    "JAKOB Antriebstechnik": "jakobantriebstechnik.de",
    "Maedler GmbH": "maedler.de",
    "Mädler GmbH": "maedler.de",
    "DIRAK GmbH": "dirak.com",
    "Rose Systemtechnik": "rose-systemtechnik.com",
    "Rose Systemtechnik GmbH": "rose-systemtechnik.com",
    "acp systems AG": "acp-systems.com",
    "Netzsch Pumpen & Systeme": "netzsch.com",
    "Netzsch Pumpen & Systeme GmbH": "netzsch.com",
    "Lippert GmbH": "lippert.de",
    "Adams Armaturen GmbH": "adams-armaturen.de",
    "AVANCO GmbH": "avanco.de",
    "Perma-tec GmbH": "perma-tec.com",
    "L&R Kältetechnik GmbH": "lr-kaeltetechnik.de",
    "L&R Kaeltetechnik GmbH": "lr-kaeltetechnik.de",
    "Deutsche Holzveredelung Schmeing": "dehonit.de",
    "Witte Barskamp GmbH": "witte-barskamp.de",
    "EOS GmbH Electro Optical Systems": "eos.info",
    "Novexx Solutions GmbH": "novexx.com",
}

# Merge all enrichment
ALL_URL_ENRICHMENT = {**URL_ENRICHMENT_TIER1, **URL_ENRICHMENT_TIER23}

# -- KNOWN DUPLICATES TO MERGE ----------------------------------------------
# Pairs where the fuzzy match missed them (different name forms)
FORCE_MERGE = [
    ("Gerhard Schubert GmbH", "Gerhard Schubert GmbH Verpackungsmaschinen"),
    ("Schmalz GmbH", "Schmalz GmbH (J. Schmalz GmbH)"),
    ("SÜDPACK SE", "SUEDPACK SE & Co. KG"),
    ("SDPACK SE", "SUEDPACK SE & Co. KG"),
    ("Aareon DACH", "Aareon Group"),
    ("G DATA Software", "G DATA CyberDefense"),
]


# -- HELPERS ----------------------------------------------------------------

def parse_name(full_name):
    """Split a full name into (firstname, lastname). Handle German titles."""
    if not full_name or pd.isna(full_name) or full_name.strip() == "":
        return "", ""
    s = str(full_name).strip()
    # Remove "None " prefix (artifact from V6 parsing)
    if s.startswith("None "):
        s = s[5:]
    # Remove titles
    for title in ["Dr. ", "Prof. ", "Dr.-Ing. ", "Dipl.-Ing. ", "Dipl.-Kfm. ",
                   "Dipl.-Wirtsch.-Ing. ", "MBA ", "LL.M. "]:
        s = s.replace(title, "")
    s = s.strip()
    parts = s.split()
    if len(parts) == 0:
        return "", ""
    if len(parts) == 1:
        return "", parts[0]
    # Last word(s) as lastname; handle "von", "van", "de" prefixes
    nobility = {"von", "van", "de", "zu", "vom"}
    lastname_start = len(parts) - 1
    for i in range(len(parts) - 2, -1, -1):
        if parts[i].lower() in nobility:
            lastname_start = i
        else:
            break
    firstname = " ".join(parts[:lastname_start])
    lastname = " ".join(parts[lastname_start:])
    return firstname, lastname


def target_contact_role(employees):
    """Based on ICP: <500 emp → GF/CEO; 500+ → Head of Sales / Vertriebsleiter"""
    if employees is None or pd.isna(employees):
        return "Geschäftsführer/CEO"
    if employees >= 500:
        return "Head of Sales / Vertriebsleiter"
    return "Geschäftsführer/CEO"


def calculate_priority_score(row):
    """
    Calculate pipeline priority score (0-100).
    Factors:
    - Client tier weight (Tier 3 = highest per ICP 'most common tier')
    - Industry tier (tier1 > tier2 > unknown)
    - Data completeness
    - Multi-source bonus
    - World market leader bonus
    """
    score = 0
    tier = row.get("client_tier")
    if pd.notna(tier):
        tier = int(tier)
        # Tier 3 is the sweet spot per ICP, then Tier 4, 2, 1, 5
        tier_weights = {3: 30, 4: 25, 2: 22, 1: 18, 5: 15}
        score += tier_weights.get(tier, 10)

    ind_tier = row.get("industry_tier", "")
    if ind_tier == "tier1":
        score += 25
    elif ind_tier == "tier2":
        score += 15
    else:
        score += 5

    completeness = row.get("data_completeness", 0)
    if pd.notna(completeness):
        score += int(completeness) * 0.2  # max 20 points

    src_count = row.get("source_count", 0)
    if pd.notna(src_count) and int(src_count) >= 2:
        score += min(int(src_count) * 3, 15)  # max 15 points

    wml = row.get("world_market_leader", "")
    if wml and pd.notna(wml) and str(wml).strip().lower().startswith("yes"):
        score += 10

    return round(score, 1)


def clean_domain(d):
    """Normalize a domain: strip protocol, www., trailing slashes."""
    if not d or pd.isna(d):
        return ""
    s = str(d).strip()
    s = s.replace("http://", "").replace("https://", "")
    if s.startswith("www."):
        s = s[4:]
    s = s.rstrip("/")
    return s


# -- MAIN -------------------------------------------------------------------

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("PHASES 2-6: PROCESSING")
print("=" * 70)

# Load Phase 1 output
df = pd.read_csv(INPUT, encoding="utf-8-sig")
print(f"\nLoaded {len(df)} companies from Phase 1")

# -- PHASE 2: Fix remaining duplicates & finalize tiers ---------------------
print("\n" + "-" * 50)
print("PHASE 2: Finalize tiers & remove remaining duplicates")
print("-" * 50)

# Force-merge known duplicates
rows_to_drop = set()
for name_a, name_b in FORCE_MERGE:
    idx_a = df.index[df["company_name"].str.contains(name_a, na=False, regex=False)]
    idx_b = df.index[df["company_name"].str.contains(name_b, na=False, regex=False)]
    if len(idx_a) > 0 and len(idx_b) > 0:
        # Keep the first, drop the second
        keep = idx_a[0]
        drop = idx_b[0]
        # Merge domain if missing
        if not df.loc[keep, "domain"] or pd.isna(df.loc[keep, "domain"]) or df.loc[keep, "domain"] == "":
            if df.loc[drop, "domain"] and pd.notna(df.loc[drop, "domain"]):
                df.loc[keep, "domain"] = df.loc[drop, "domain"]
        rows_to_drop.add(drop)
        print(f"  Merged: '{name_b}' into '{name_a}'")

df = df.drop(index=rows_to_drop).reset_index(drop=True)
print(f"  Removed {len(rows_to_drop)} duplicate rows")

# Fix unassigned tiers: companies with revenue <10M and <50 employees
# Per ICP, minimum is Tier 5 (EUR 10M-20M, 50-200 emp). Below = out of ICP range.
# But some are valid small B2B companies from Prospecting 100. Keep them as Tier 5.
unassigned = df[df["client_tier"].isna()]
for idx in unassigned.index:
    rev = df.loc[idx, "revenue_eur"]
    emp = df.loc[idx, "employees"]
    # If both are below minimum, assign Tier 5 (edge) or flag
    if pd.notna(rev) and rev > 0:
        if rev >= 5_000_000:
            df.loc[idx, "client_tier"] = 5
        else:
            df.loc[idx, "client_tier"] = 5  # Keep but flag as edge
    elif pd.notna(emp) and emp >= 20:
        df.loc[idx, "client_tier"] = 5
    else:
        df.loc[idx, "client_tier"] = 5  # Default to Tier 5 for any remaining

still_unassigned = df["client_tier"].isna().sum()
print(f"  Tier assignments finalized. Remaining unassigned: {still_unassigned}")
total_after_dedup = len(df)
print(f"  Total companies: {total_after_dedup}")

# -- PHASE 3: URL Enrichment -----------------------------------------------
print("\n" + "-" * 50)
print("PHASE 3: URL Enrichment")
print("-" * 50)

enriched_count = 0
for idx in df.index:
    if df.loc[idx, "has_url"]:
        continue
    name = df.loc[idx, "company_name"]
    if name in ALL_URL_ENRICHMENT:
        df.loc[idx, "domain"] = ALL_URL_ENRICHMENT[name]
        df.loc[idx, "has_url"] = True
        enriched_count += 1
        continue
    # Try partial match
    for key, domain in ALL_URL_ENRICHMENT.items():
        if key.lower() in name.lower() or name.lower() in key.lower():
            df.loc[idx, "domain"] = domain
            df.loc[idx, "has_url"] = True
            enriched_count += 1
            break

still_missing_url = (~df["has_url"]).sum()
print(f"  URLs enriched from lookup: {enriched_count}")
print(f"  Still missing URL: {still_missing_url}")

# Clean all domains
df["domain"] = df["domain"].apply(clean_domain)

# -- PHASE 4: Contact Normalization -----------------------------------------
print("\n" + "-" * 50)
print("PHASE 4: Contact Normalization")
print("-" * 50)

# Parse contact names into first/last
df["contact_1_firstname"] = ""
df["contact_1_lastname"] = ""
df["target_contact_role"] = ""

for idx in df.index:
    full_name = df.loc[idx, "contact_1_name"]
    firstname, lastname = parse_name(full_name)
    df.loc[idx, "contact_1_firstname"] = firstname
    df.loc[idx, "contact_1_lastname"] = lastname
    emp = df.loc[idx, "employees"]
    df.loc[idx, "target_contact_role"] = target_contact_role(emp)

has_parsed_contact = ((df["contact_1_firstname"] != "") | (df["contact_1_lastname"] != "")).sum()
has_any_contact = (df["has_contact"]).sum()
print(f"  Contacts with parsed first/last name: {has_parsed_contact}")
print(f"  Companies with any contact: {has_any_contact}")
print(f"  Companies needing contact enrichment: {len(df) - has_any_contact}")

# Flag contact-role mismatch
role_mismatch = 0
for idx in df.index:
    if not df.loc[idx, "has_contact"]:
        continue
    pos = str(df.loc[idx, "contact_1_position"]).lower()
    target = df.loc[idx, "target_contact_role"].lower()
    if "geschäftsführer" in target or "ceo" in target:
        if any(x in pos for x in ["geschäftsführer", "ceo", "geschäftsf", "gründer", "inhaber", "owner", "managing director"]):
            df.loc[idx, "contact_role_match"] = True
        else:
            df.loc[idx, "contact_role_match"] = False
            role_mismatch += 1
    elif "sales" in target or "vertrieb" in target:
        if any(x in pos for x in ["sales", "vertrieb", "commercial", "revenue"]):
            df.loc[idx, "contact_role_match"] = True
        else:
            df.loc[idx, "contact_role_match"] = False
            role_mismatch += 1
    else:
        df.loc[idx, "contact_role_match"] = True

print(f"  Contacts with wrong role for company size: {role_mismatch}")

# -- PHASE 5: Pipeline Priority Scoring -------------------------------------
print("\n" + "-" * 50)
print("PHASE 5: Pipeline Priority Scoring")
print("-" * 50)

df["pipeline_priority"] = df.apply(calculate_priority_score, axis=1)

# Flag current pipeline companies
PIPELINE_COMPANIES = ["UZIN UTZ", "Erler", "SOLCOM"]
df["in_pipeline"] = False
for pc in PIPELINE_COMPANIES:
    mask = df["company_name"].str.contains(pc, case=False, na=False)
    df.loc[mask, "in_pipeline"] = True
    matches = df[mask]["company_name"].tolist()
    if matches:
        print(f"  Pipeline company found: {matches}")

# Flag companies already in DB (from source data)
df["in_db"] = False
# These were flagged in original sources
in_db_names = ["Winterhalter", "Babtec", "MARKT-PILOT", "Spryker", "Knick",
               "imc Test", "PicoQuant", "Jonas & Redmann", "Optris", "DoorBird",
               "DSA Systemtechnik", "BigRep", "Pyramid Computer", "Promwad",
               "Abas Software", "SYSTEMA", "G DATA", "ModuleWorks", "Jedox",
               "osapiens", "GBTEC", "SimScale", "proLogistik", "KONUX",
               "Kontron AIS", "ecosio", "Implico", "PlanRadar"]
for name in in_db_names:
    mask = df["company_name"].str.contains(name, case=False, na=False)
    df.loc[mask, "in_db"] = True

in_db_count = df["in_db"].sum()
print(f"  Companies already in DB: {in_db_count}")

# Priority distribution
print("\n  Priority Score Distribution:")
for bucket_name, lo, hi in [("Top (75+)", 75, 200), ("High (60-75)", 60, 75),
                              ("Medium (45-60)", 45, 60), ("Lower (<45)", 0, 45)]:
    count = ((df["pipeline_priority"] >= lo) & (df["pipeline_priority"] < hi)).sum()
    print(f"    {bucket_name}: {count}")

# -- PHASE 6: HubSpot-Ready Export ------------------------------------------
print("\n" + "-" * 50)
print("PHASE 6: HubSpot-Ready Export")
print("-" * 50)

# Sort by priority
df = df.sort_values("pipeline_priority", ascending=False).reset_index(drop=True)

# === COMPANIES CSV ===
companies_cols = {
    "company_name": "Name",
    "domain": "Company Domain Name",
    "city": "City",
    "region": "State/Region",
    "country": "Country/Region",
    "zip": "Postal Code",
    "phone": "Phone Number",
    "email_company": "Company Email",
    "industry": "Industry",
    "description": "Description",
    "revenue_eur": "Annual Revenue",
    "employees": "Number of Employees",
    "client_tier": "Client Tier",
    "industry_tier": "Industry Tier",
    "ownership": "Ownership Type",
    "founding_year": "Founding Year",
    "world_market_leader": "World Market Leader",
    "niche_leadership": "Niche Leadership",
    "pipeline_priority": "Pipeline Priority Score",
    "in_pipeline": "In Pipeline",
    "in_db": "Already in DB",
    "data_completeness": "Data Completeness %",
    "sources": "Source Lists",
    "source_count": "Source Count",
    "target_contact_role": "Target Contact Role",
}

# Filter: only companies WITH a URL (HubSpot requirement + user requirement)
df_with_url = df[df["has_url"] == True].copy()
df_no_url = df[df["has_url"] == False].copy()

companies_export = df_with_url[list(companies_cols.keys())].rename(columns=companies_cols)

# Clean up: convert tier to int, round revenue
companies_export["Client Tier"] = companies_export["Client Tier"].apply(
    lambda x: int(x) if pd.notna(x) else ""
)
companies_export["Annual Revenue"] = companies_export["Annual Revenue"].apply(
    lambda x: int(x) if pd.notna(x) and x > 0 else ""
)
companies_export["Number of Employees"] = companies_export["Number of Employees"].apply(
    lambda x: int(x) if pd.notna(x) and x > 0 else ""
)
companies_export["Founding Year"] = companies_export["Founding Year"].apply(
    lambda x: int(x) if pd.notna(x) and x > 0 else ""
)
companies_export["Pipeline Priority Score"] = companies_export["Pipeline Priority Score"].apply(
    lambda x: round(x, 1) if pd.notna(x) else ""
)

companies_path = os.path.join(BASE, "hubspot_companies_import.csv")
companies_export.to_csv(companies_path, index=False, encoding="utf-8-sig")
print(f"  Companies CSV: {companies_path}")
print(f"    Total: {len(companies_export)} companies (with URL)")

# === CONTACTS CSV ===
contacts_rows = []
for idx in df_with_url.index:
    fn = df_with_url.loc[idx, "contact_1_firstname"]
    ln = df_with_url.loc[idx, "contact_1_lastname"]
    if not fn and not ln:
        continue
    if not ln:
        continue  # Need at least a last name
    contacts_rows.append({
        "First Name": fn,
        "Last Name": ln,
        "Email": df_with_url.loc[idx, "contact_1_email"] if pd.notna(df_with_url.loc[idx, "contact_1_email"]) else "",
        "Job Title": df_with_url.loc[idx, "contact_1_position"] if pd.notna(df_with_url.loc[idx, "contact_1_position"]) else "",
        "LinkedIn URL": df_with_url.loc[idx, "contact_1_linkedin"] if pd.notna(df_with_url.loc[idx, "contact_1_linkedin"]) else "",
        "Associated Company Domain": clean_domain(df_with_url.loc[idx, "domain"]),
        "Associated Company Name": df_with_url.loc[idx, "company_name"],
    })

contacts_df = pd.DataFrame(contacts_rows)
contacts_path = os.path.join(BASE, "hubspot_contacts_import.csv")
contacts_df.to_csv(contacts_path, index=False, encoding="utf-8-sig")
print(f"  Contacts CSV: {contacts_path}")
print(f"    Total: {len(contacts_df)} contacts")

# === GAPS REPORT ===
gaps_rows = []

# Companies missing URL entirely
for idx in df_no_url.index:
    gaps_rows.append({
        "Company": df_no_url.loc[idx, "company_name"],
        "City": df_no_url.loc[idx, "city"],
        "Country": df_no_url.loc[idx, "country"],
        "Client Tier": int(df_no_url.loc[idx, "client_tier"]) if pd.notna(df_no_url.loc[idx, "client_tier"]) else "",
        "Gap Type": "MISSING URL (cannot upload to HubSpot)",
        "Action Required": "Find company website URL",
        "Priority": "HIGH" if df_no_url.loc[idx, "client_tier"] in [1, 2, 3] else "MEDIUM",
    })

# Companies with URL but missing contact
no_contact = df_with_url[df_with_url["has_contact"] == False]
for idx in no_contact.index:
    gaps_rows.append({
        "Company": no_contact.loc[idx, "company_name"],
        "City": no_contact.loc[idx, "city"],
        "Country": no_contact.loc[idx, "country"],
        "Client Tier": int(no_contact.loc[idx, "client_tier"]) if pd.notna(no_contact.loc[idx, "client_tier"]) else "",
        "Gap Type": "MISSING CONTACT",
        "Action Required": f"Find {no_contact.loc[idx, 'target_contact_role']}",
        "Priority": "HIGH" if no_contact.loc[idx, "client_tier"] in [1, 2, 3] else "MEDIUM",
    })

# Companies where contact role doesn't match target
wrong_role = df_with_url[df_with_url.get("contact_role_match") == False] if "contact_role_match" in df_with_url.columns else pd.DataFrame()
if len(wrong_role) > 0:
    for idx in wrong_role.index:
        gaps_rows.append({
            "Company": wrong_role.loc[idx, "company_name"],
            "City": wrong_role.loc[idx, "city"],
            "Country": wrong_role.loc[idx, "country"],
            "Client Tier": int(wrong_role.loc[idx, "client_tier"]) if pd.notna(wrong_role.loc[idx, "client_tier"]) else "",
            "Gap Type": f"WRONG CONTACT ROLE (have: {wrong_role.loc[idx, 'contact_1_position']})",
            "Action Required": f"Find {wrong_role.loc[idx, 'target_contact_role']} (currently have {wrong_role.loc[idx, 'contact_1_position']})",
            "Priority": "LOW",
        })

gaps_df = pd.DataFrame(gaps_rows)
gaps_df = gaps_df.sort_values(["Priority", "Client Tier"]).reset_index(drop=True)
gaps_path = os.path.join(BASE, "hubspot_gaps_report.csv")
gaps_df.to_csv(gaps_path, index=False, encoding="utf-8-sig")
print(f"  Gaps Report: {gaps_path}")
print(f"    Total gaps: {len(gaps_df)}")
print(f"      Missing URL: {len([g for g in gaps_rows if 'URL' in g['Gap Type']])}")
print(f"      Missing Contact: {len([g for g in gaps_rows if 'MISSING CONTACT' in g['Gap Type']])}")
print(f"      Wrong Contact Role: {len([g for g in gaps_rows if 'WRONG' in g['Gap Type']])}")

# === FULL MASTER LIST (updated) ===
master_path = os.path.join(BASE, "master_target_list_final.csv")
df.to_csv(master_path, index=False, encoding="utf-8-sig")
print(f"\n  Full Master List: {master_path}")
print(f"    Total: {len(df)} companies")

# -- FINAL SUMMARY ----------------------------------------------------------
print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print(f"""
DELIVERABLES:
  1. hubspot_companies_import.csv  → {len(companies_export)} companies ready for HubSpot
  2. hubspot_contacts_import.csv   → {len(contacts_df)} contacts linked to companies
  3. hubspot_gaps_report.csv       → {len(gaps_df)} items needing manual enrichment
  4. master_target_list_final.csv  → {len(df)} companies (full master incl. incomplete)

COMPANY BREAKDOWN (HubSpot-ready):
  Tier 1 (EUR 30K+ MRR):   {len(companies_export[companies_export['Client Tier'] == 1])}
  Tier 2 (EUR 20-30K MRR): {len(companies_export[companies_export['Client Tier'] == 2])}
  Tier 3 (EUR 10-20K MRR): {len(companies_export[companies_export['Client Tier'] == 3])}
  Tier 4 (EUR 5-10K MRR):  {len(companies_export[companies_export['Client Tier'] == 4])}
  Tier 5 (EUR 2.5-5K MRR): {len(companies_export[companies_export['Client Tier'] == 5])}

COUNTRY BREAKDOWN (HubSpot-ready):
  Germany:     {len(companies_export[companies_export['Country/Region'] == 'DE'])}
  Austria:     {len(companies_export[companies_export['Country/Region'] == 'AT'])}
  Switzerland: {len(companies_export[companies_export['Country/Region'] == 'CH'])}

DATA QUALITY (HubSpot-ready):
  Has Revenue:      {(companies_export['Annual Revenue'] != '').sum()} / {len(companies_export)}
  Has Employees:    {(companies_export['Number of Employees'] != '').sum()} / {len(companies_export)}
  Has Contact:      {len(contacts_df)} contacts for {len(companies_export)} companies
  Has Description:  {(companies_export['Description'].notna() & (companies_export['Description'] != '')).sum()} / {len(companies_export)}

REMAINING GAPS:
  Companies blocked (no URL):     {len(df_no_url)}
  Companies needing contacts:     {(~df_with_url['has_contact']).sum()}
""")
