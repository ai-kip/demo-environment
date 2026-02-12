#!/usr/bin/env python3
"""
Benelux Contact Enrichment Script
==================================
Integrates researched contact data into:
- master_target_list_benelux.csv (adds contact columns)
- hubspot_contacts_import_benelux.csv (updates with actual names/LinkedIn)
- hubspot_gaps_report_benelux.csv (updates gap status)
"""

import csv
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_DIR = os.path.join(BASE, "02_master_lists")
HUBSPOT_DIR = os.path.join(BASE, "01_hubspot_import")
GAPS_DIR = os.path.join(BASE, "03_gaps_and_enrichment")

# ============================================================
# CONTACT DATA FROM RESEARCH (144 companies from 4 batches)
# Format: (domain, first_name, last_name, job_title, linkedin_url)
# ============================================================

CONTACTS = [
    # --- Batch 3 (37 companies) ---
    ("aertssen.be", "Koen", "Vroman", "Sales Professional", "https://www.linkedin.com/in/koenvroman/"),
    ("unifiedpostgroup.com", "Chrystele", "Dumont", "Chief Revenue Officer", "https://www.linkedin.com/in/chrysteledumont/"),
    ("efficy.com", "Thomas", "Bierry", "Head of Sales & Account Management", "https://www.linkedin.com/in/thomas-bierry/"),
    ("euro-composites.com", "Gunnar", "Ziwes", "Vice President Sales", "https://www.linkedin.com/in/gunnar-ziwes-393432142/"),
    ("severfield.eu", "Robert", "Evans", "Managing Director", "https://uk.linkedin.com/in/robert-evans-2b025085"),
    ("brenntag.com", "Jan Joop", "Alberts", "Director Brenntag Nederland", "https://www.linkedin.com/in/jan-joop-alberts-a8b35685/"),
    ("cebeo.be", "Gerard", "Cloes", "Directeur Commercial", "https://be.linkedin.com/in/gerard-cloes-a72b7b113"),
    ("itsme.eu", "Tom", "Van Den Bosch", "CEO", ""),
    ("thermaflex.com", "Hans", "de Haas", "Group CEO", "https://nl.linkedin.com/in/hansdehaas"),
    ("daf.com", "Michiel", "Kuijs", "European Sales Director", "https://www.linkedin.com/in/michiel-kuijs-1867a627/"),
    ("moba.net", "Paul", "Deschouwer", "Sales Director", "https://www.linkedin.com/in/paul-deschouwer-485b9782/"),
    ("holmatro.com", "Rob", "Loonen", "Commercial Manager", "https://www.linkedin.com/in/rob-loonen-857ab12b/"),
    ("batenburg.nl", "Max", "Deckers", "Sales Team Leader", "https://www.linkedin.com/in/max-deckers-62762018/"),
    ("gazelle.nl", "Ewoud", "van Leeuwen", "Commercieel Directeur / CCO", "https://www.linkedin.com/in/ewoud-van-leeuwen-64018512/"),
    ("unit4.com", "Tony", "Tajkarimi", "VP Sales", "https://www.linkedin.com/in/tony-tajkarimi-35316314b"),
    ("topicus.com", "Daan", "Dijkhuizen", "CEO Topicus Operating Group", "https://nl.linkedin.com/in/daandijkhuizen"),
    ("conclusion.nl", "Paul", "Zevenboom", "Commercial Director", "https://www.linkedin.com/in/paulzevenboom/"),
    ("centric.eu", "Michiel", "Vunderink", "Commercieel Directeur", "https://www.linkedin.com/in/michiel-vunderink/"),
    ("mendix.com", "Erwin", "de Groot", "Sales Director", "https://www.linkedin.com/in/erwindegro/"),
    ("materialise.com", "Koen", "Bas", "Sr. Sales Director Software", "https://www.linkedin.com/in/koen-bas/"),
    ("avr.be", "Stefan", "Top", "Managing Director", "https://www.linkedin.com/in/stefan-top-b507243/"),
    ("dewulfgroup.com", "Hendrik", "Decramer", "CEO", "https://www.linkedin.com/in/hendrik-decramer-32820163/"),
    ("showpad.com", "Hendrik", "Isebaert", "CEO", "https://be.linkedin.com/in/hendrikisebaert"),
    ("lansweeper.com", "Dave", "Goossens", "CEO", "https://be.linkedin.com/in/dave-goossens-721b631"),
    ("circuitfoil.com", "Fabienne", "Bozet", "Former CEO", "https://www.linkedin.com/in/fabienne-bozet-53666311/"),
    ("ampacet.com", "Marcello", "Bergamo", "Managing Director EMEA", "https://www.linkedin.com/in/marcello-bergamo-54917a29/"),
    ("technischeunie.nl", "Bas", "Schroder", "Director of Sales", ""),
    ("bmn.nl", "Jan-Willem", "Dockheer", "Managing Director", "https://www.linkedin.com/in/jan-willem-dockheer-342115/"),
    ("royalbrinkman.com", "Jan", "Schuttrups", "Commercial Director", "https://nl.linkedin.com/in/jan-schuttrups-72976040"),
    ("prodrive-technologies.com", "Niek", "Martens", "Commercial Director", "https://www.linkedin.com/in/niekmartens/"),
    ("vdlgroep.com", "Armando", "Risi", "Commercial Lead", "https://www.linkedin.com/in/armandorisi/"),
    ("nedschroef.com", "Richard", "van den Dungen", "VP Sales & Business Development", "https://www.linkedin.com/in/richard-dungen-van-den-5110837/"),
    ("vanoord.com", "Carlos", "Mollet", "Commercial Director Dredging & Infra", "https://www.linkedin.com/in/carlos-mollet-5b11596/"),
    ("gknaerospace.com", "Leon", "Kouters", "VP Sales & Marketing", "https://www.linkedin.com/in/leon-kouters-846b976/"),
    ("kiremko.com", "Gerardo", "Chiaia", "President & CEO", "https://lu.linkedin.com/in/gerardo-chiaia-86377937"),
    ("bdrthermeagroup.com", "Xavier", "Andreu", "Global Sales Director", "https://www.linkedin.com/in/xavier-andreu-9613204/"),
    ("wilatooling.com", "Hans", "Willemsen", "Managing Director", "https://www.linkedin.com/in/hans-willemsen-88403814/"),

    # --- Batch 4 (37 companies) ---
    ("tatasteelnederland.com", "Peter", "Bernscher", "Chief Commercial Officer", "https://www.linkedin.com/in/peter-bernscher-6b5448155/"),
    ("eriks.com", "Henriette", "Ravesloot", "Commercial Director", "https://www.linkedin.com/in/henriette-ravesloot-a93a3b66/"),
    ("pon.com", "Jochem", "Neuteboom", "Commercial Director", "https://www.linkedin.com/in/jochem-neuteboom-b6b7846/"),
    ("perfettivanmelle.com", "Bartlomiej", "Sedlak", "Global Head of RTM", "https://www.linkedin.com/in/bartlomiej-sedlak-533b181/"),
    ("nxp.com", "Olivier", "Cottereau", "SVP EMEA Sales and Marketing", "https://de.linkedin.com/in/olivier-cottereau-5b30191"),
    ("neways.nl", "Nanda", "Vonk-Seele", "Global Sales Director", "https://www.linkedin.com/in/nanda-vonk-seele/"),
    ("elastic.co", "Wibke", "Laier", "Area VP EMEA Central", "https://www.linkedin.com/in/wibke-laier-59554b53/"),
    ("bintg.com", "Jefrem", "Jennard", "Sales Director Industrial Fibres", "https://www.linkedin.com/in/jefrem-jennard-b337498/"),
    ("recticel.com", "Benedikt", "Van Roosmalen", "Commercial Director", "https://www.linkedin.com/in/benediktvanroosmalen/"),
    ("picanol.be", "Johan", "Verstraete", "VP Marketing, Sales & Service", "https://www.linkedin.com/in/johanverstraete/"),
    ("melexis.com", "Gianluigi", "Morello", "Sales Director", "https://www.linkedin.com/in/gianluigi-morello-8628327/"),
    ("renson.eu", "Andre", "Kerckhof", "Commercial Director", "https://be.linkedin.com/in/andrekerckhof"),
    ("bosal.com", "Gert", "Van Meerbeeck", "Global Customer Director", "https://be.linkedin.com/in/gertvanmeerbeeck"),
    ("sabca.be", "Thibauld", "Jongen", "CEO", "https://www.linkedin.com/in/thibauld-jongen-b902404a/"),
    ("oleon.com", "Jan", "Vervoort", "General Manager Benelux", "https://www.linkedin.com/in/jan-vervoort/"),
    ("punchpowertrain.com", "Sebastien", "Mazoyer", "CEO", "https://www.linkedin.com/in/sebastien-mazoyer-48465b6/"),
    ("odoo.com", "Sebastien", "Bruyr", "Chief Commercial Officer", "https://be.linkedin.com/in/s%C3%A9bastien-bruyr-ba529839"),
    ("collibra.com", "Steve", "Neat", "VP Sales EMEA", "https://uk.linkedin.com/in/steveneat"),
    ("esko.com", "Margaret", "Thurston", "VP Sales", "https://www.linkedin.com/in/margaret-thurston-20551a6/"),
    ("iee.lu", "Gianluca", "Favalli", "Director of Sales", "https://www.linkedin.com/in/favalli-gianluca-849b66117/"),
    ("vanmossel.com", "Marco", "van de Werken", "Commercial Director", "https://nl.linkedin.com/in/marcovandewerken"),
    ("vanleeuwen.com", "Michael", "van Etten", "Head of Sales", "https://www.linkedin.com/in/michael-van-etten-95075750/"),
    ("imcdgroup.com", "Andreas", "Igerl", "Managing Director EMEA", ""),
    ("caldic.com", "Pieter", "Naessens", "Commercial Director Benelux", "https://www.linkedin.com/in/pieter-naessens-9390601/"),
    ("boschman.nl", "Frank", "Boschman", "Managing Director", "https://www.linkedin.com/in/frank-boschman-42789611/"),
    ("meyn.com", "Robbert", "Birkhoff", "Director of Sales & Projects", ""),
    ("heras.com", "Werner", "Ghitti", "National Sales Manager", "https://nl.linkedin.com/in/wernerghitti"),
    ("boonedam.com", "Ian", "Goldsmith", "Global Head of Sales", "https://www.linkedin.com/in/ian-goldsmith-99ab3947/"),
    ("malvernpanalytical.com", "Andreas", "Ludwig", "Head of Sales", "https://www.linkedin.com/in/andreas-ludwig-581341b0/"),
    ("bakkermagnetics.com", "Geert-Jan", "Bakker", "CEO / Owner", "https://www.linkedin.com/in/geert-jan-gj-bakker-1a924a6a/"),
    ("eye.security", "Job", "Kuijpers", "CEO & Co-Founder", "https://www.linkedin.com/in/job-kuijpers-98bb20/"),
    ("thinkwisesoftware.com", "Victor", "Klaren", "Co-Founder & CVO", "https://www.linkedin.com/in/vklaren/"),
    ("nearfieldinstruments.com", "Hamed", "Sadeghian", "CEO & Co-Founder", "https://www.linkedin.com/in/hamed-sadeghian-76490ab/"),
    ("bekaert.com", "Torsten", "Eichhorn", "Director Sales & Marketing", "https://www.linkedin.com/in/torsten-eichhorn-12b27b116/"),
    ("umicore.com", "Karl", "Goertz", "Global Sales Director", "https://www.linkedin.com/in/karl-goertz-4828484/"),
    ("solvay.com", "Stavros", "Vasilakis", "Senior Sales & Marketing Director", "https://www.linkedin.com/in/stavros-vasilakis-88301032/"),
    ("etex.com", "Jochen", "Friedrichs", "Head of Division Building Performance", "https://www.linkedin.com/in/jochen-friedrichs-a8b34b/"),

    # --- Batch 5 (37 companies) ---
    ("tessenderlo.com", "Jan", "Vandendriessche", "VP", "https://www.linkedin.com/in/vandendriessche-jan-61313a7/"),
    ("johncockerill.com", "Laurent", "de Schaetzen", "Head of Sales Metals", "https://www.linkedin.com/in/laurent-de-schaetzen-085556a/"),
    ("sonaca.com", "Thibault", "Carrier", "Group Chief Commercial Officer", "https://be.linkedin.com/in/thibaultcarrier"),
    ("deme-group.com", "Kassem", "Maged", "Business Development Director", "https://www.linkedin.com/in/kassem-m-12179519/"),
    ("jandenul.com", "An", "Smet", "Chief Commercial Officer", "https://be.linkedin.com/in/an-smet-4853727"),
    ("sibelco.com", "Francisco", "Millar", "VP Operations & Commercial Western Europe", "https://www.linkedin.com/in/franciscomillar/"),
    ("agc-glass.eu", "Olivier", "Hansen", "Commercial Director", "https://www.linkedin.com/in/olivier-hansen-a9a5ab12/"),
    ("reynaers.com", "Andreas", "Wilsdorf", "Chief Sales Officer", "https://be.linkedin.com/in/andreas-wilsdorf-436b99bb"),
    ("smulders.com", "Wim", "Vaes", "Commercial Director", "https://www.linkedin.com/in/wim-vaes-aa8a6666/"),
    ("ontex.com", "Arnaud", "Evrard", "Head of Sales & Marketing", "https://www.linkedin.com/in/arnaud-evrard-98a4a783/"),
    ("nyrstar.com", "Simon", "Dent", "Global Head Commercial", "https://sg.linkedin.com/in/simon-dent-82226076"),
    ("cegeka.com", "Josef", "Szekeres", "Sales & Marketing Director", ""),
    ("cronos-groep.be", "Evelyne", "Dhaenens", "Chief Commercial Officer", "https://www.linkedin.com/in/evelynedhaenens/"),
    ("nrb.be", "Pierre", "Dumont", "Chief Commercial Officer", "https://be.linkedin.com/in/pierre-dumont-629739"),
    ("team.blue", "Stephen", "Ewart", "Chief Revenue Officer", "https://www.linkedin.com/in/stephen-ewart-658a6453/"),
    ("arcelormittal.com", "Laurent", "Plasman", "CMO / Head of Sales", "https://www.linkedin.com/in/laurent-plasman-2192214/"),
    ("aperam.com", "Joeri", "Vandewinkel", "Commercial Director", "https://www.linkedin.com/in/joeri-vandewinkel-5b389093/"),
    ("ses.com", "John-Paul", "Hemingway", "Chief Commercial Officer", "https://www.linkedin.com/in/john-paul-hemingway-7934788/"),
    ("construsteel.com", "Jos", "Bonte", "CEO / Owner", "https://www.linkedin.com/in/josbonte/"),
    ("nmbrs.com", "Michiel", "Chevalier", "CEO / Founder", "https://nl.linkedin.com/in/michielchevalier"),
    ("berdal.com", "Bas", "van Kamperdijk", "CEO", "https://nl.linkedin.com/in/bas-van-kamperdijk-4773a613"),
    ("prowise.com", "Michael", "Ahrens", "CEO / Founder", "https://nl.linkedin.com/in/michael-a-266534a"),
    ("barilcoatings.com", "Jeroen", "Duijghuisen", "CEO", "https://www.linkedin.com/in/jeroen-duijghuisen-598aa610a/"),
    ("bengglas.nl", "Youri", "Creutzberg", "Directeur / Co-Founder", "https://www.linkedin.com/in/youri-creutzberg/"),
    ("tvh.com", "Kristof", "Bolle", "Chief Commercial Officer", "https://www.linkedin.com/in/kristof-bolle-997aa76/"),
    ("azelis.com", "Evy", "Hellinckx", "CEO EMEA", "https://www.linkedin.com/in/evy-hellinckx/"),
    ("tkhgroup.com", "Dick", "Hoekstra", "Business Development Director", "https://nl.linkedin.com/in/dick-hoekstra-056b9a142"),
    ("mammoet.com", "Jeremy", "Asher", "VP Sales and Marketing", "https://ca.linkedin.com/in/jeremy-asher-30bbb729"),
    ("signify.com", "Koen", "Huijbregts", "Commercial Director Benelux", "https://www.linkedin.com/in/koenhuijbregts/"),
    ("mollie.com", "Ken", "Serdons", "Chief Commercial Officer", "https://www.linkedin.com/in/kenserdons/"),
    ("nedap.com", "Woltherus", "Karsijns", "Global Sales Director", "https://www.linkedin.com/in/woltherus-karsijns-45319226/"),
    ("techwolf.ai", "Andreas", "De Neve", "Co-Founder & CEO", "https://be.linkedin.com/in/andreasdeneve"),
    ("guardsquare.com", "Roel", "Caers", "CEO", "https://be.linkedin.com/in/roelcaers"),
    ("intigriti.com", "Stijn", "Jans", "Founder & CEO", "https://be.linkedin.com/in/stijnjans"),
    ("brightanalytics.eu", "Merijn", "Demuynck", "Co-Founder", "https://be.linkedin.com/in/merijndemuynck"),
    ("azumuta.com", "Batist", "Leman", "CEO & Co-Founder", "https://be.linkedin.com/in/batistleman"),
    ("xeryon.com", "Jan", "Peirs", "Co-Founder & CEO", "https://be.linkedin.com/in/jan-peirs-288b91b"),

    # --- Batch 6 (33 companies) ---
    ("vertuoza.com", "Dominique", "Pellegrino", "CEO & Co-founder", "https://be.linkedin.com/in/dominiquepellegrino"),
    ("otiv.ai", "Sam", "De Smet", "Co-founder & CEO", "https://www.linkedin.com/in/samdsmet/"),
    ("luxtrust.com", "Fabrice", "Aresu", "CEO", "https://www.linkedin.com/in/fabrice-aresu/"),
    ("iscal.be", "Steven", "De Cuyper", "CEO", ""),
    ("munckhof.nl", "Marc", "Hollemans", "Commercial Director", "https://www.linkedin.com/in/marchollemans/"),
    ("kramp.com", "Rutger", "Bruijnen", "Chief Commercial Officer", "https://www.linkedin.com/in/rutgerbruijnen/"),
    ("fastned.nl", "Michiel", "Langezaal", "Co-founder and CEO", "https://nl.linkedin.com/in/michiellangezaal"),
    ("magotteaux.com", "Lionel", "Van Obbergh", "Head of Sales", ""),
    ("evs.com", "Nicolas", "Bourdon", "Chief Commercial Officer", "https://be.linkedin.com/in/nicolas-bourdon-19502b6"),
    ("eupen.com", "Mike", "Goblet", "Commercial Director", ""),
    ("easyfairs.com", "Matt", "Benyon", "Group CEO", "https://uk.linkedin.com/in/matthew-benyon-48569b4"),
    ("televic.com", "Kirk", "Klug", "Director of Sales & Business Development", "https://www.linkedin.com/in/kirk-klug-b01587b/"),
    ("royal-ingredients.com", "Mark", "Weverink", "Managing Director", "https://www.linkedin.com/in/mark-weverink-22ba135/"),
    ("kendrion.com", "Dirk", "Schons", "Global Sales Director", "https://www.linkedin.com/in/dirk-schons-467749106/"),
    ("b-close.be", "Eric", "Maertens", "Managing Director", "https://www.linkedin.com/in/eric-maertens-5790674/"),
    ("strukton.com", "Rob", "van Wingerden", "CEO a.i.", ""),
    ("hoppenbrouwers.nl", "Raymond", "Nicolaas", "Commercieel Manager", "https://www.linkedin.com/in/raymondnicolaas/"),
    ("adyen.com", "Roelant", "Prins", "Chief Commercial Officer", "https://nl.linkedin.com/in/roelantprins"),
    ("tomtom.com", "Mike", "Schoofs", "Chief Revenue Officer", "https://www.linkedin.com/in/mike-schoofs/"),
    ("prayon.com", "Joel", "Cerfontaine", "Sales Director", "https://be.linkedin.com/in/jo%C3%ABl-cerfontaine-a1b8497"),
    ("plastiflex.com", "Yves", "Vanhauwaert", "VP Sales Europe", "https://be.linkedin.com/in/yvesvanhauwaert"),
    ("rotarex.com", "Philippe", "Schang", "Sales Director", "https://www.linkedin.com/in/philippe-schang/"),
    ("qblox.com", "Niels", "Bultink", "CEO & Co-founder", "https://www.linkedin.com/in/niels-bultink-6a752630/"),
    ("aliaxis.com", "Spencer", "Maynard", "Commercial Director", ""),
    ("soudalgroup.com", "Koen", "Anthierens", "Head of International Business Development", "https://www.linkedin.com/in/koen-anthierens-55b1857b/"),
    ("barco.com", "Wouter", "Bonte", "VP Global Sales", "https://be.linkedin.com/in/wouterbonte"),
    ("puratos.com", "Roman", "Gruber", "Head of Sales", "https://www.linkedin.com/in/roman-gruber-1b175715b/"),
    ("agfa.com", "Herman", "Raats", "Marketing and Sales Director", "https://be.linkedin.com/in/herman-raats-1619775"),
    ("deceuninck.com", "Peter", "Dyer", "Head of Commercial Sales", "https://www.linkedin.com/in/peter-dyer-83128719/"),
    ("lhoist.com", "Mark", "Milner", "VP Commercial", "https://www.linkedin.com/in/mark-milner-06242436a"),
    ("vandemoortele.com", "Helena", "Vanhoutte", "Managing Director PBFS", "https://www.linkedin.com/in/helena-vanhoutte-1756a25/"),
    ("unilin.com", "Jan", "Coppin", "Global Sales Director", "https://be.linkedin.com/in/jancoppin"),
    ("ceratizit.com", "Supriya", "Salian", "Director of Global Sales", "https://www.linkedin.com/in/supriya-salian-11291786/"),
]


def main():
    # Build contact lookup by domain
    contact_map = {}
    for domain, first, last, title, linkedin in CONTACTS:
        contact_map[domain.lower()] = {
            "first_name": first,
            "last_name": last,
            "job_title": title,
            "linkedin_url": linkedin,
        }

    print(f"Contact data loaded: {len(contact_map)} companies")

    # --- 1. Read master list ---
    master_path = os.path.join(MASTER_DIR, "master_target_list_benelux.csv")
    with open(master_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        master_fields = reader.fieldnames
        master_rows = list(reader)
    print(f"Master list loaded: {len(master_rows)} companies")

    # Add contact columns to master if not present
    contact_cols = ["contact_1_firstname", "contact_1_lastname", "contact_1_position", "contact_1_linkedin"]
    for col in contact_cols:
        if col not in master_fields:
            master_fields.append(col)

    # Update master rows with contact data
    matched = 0
    unmatched_domains = []
    for row in master_rows:
        domain = row.get("domain", "").lower().strip()
        if domain in contact_map:
            c = contact_map[domain]
            row["contact_1_firstname"] = c["first_name"]
            row["contact_1_lastname"] = c["last_name"]
            row["contact_1_position"] = c["job_title"]
            row["contact_1_linkedin"] = c["linkedin_url"]
            matched += 1
        else:
            row["contact_1_firstname"] = ""
            row["contact_1_lastname"] = ""
            row["contact_1_position"] = ""
            row["contact_1_linkedin"] = ""
            unmatched_domains.append((row.get("company_name", ""), domain))

    print(f"Contacts matched: {matched}/{len(master_rows)}")
    print(f"Still missing: {len(unmatched_domains)}")

    # Write updated master list
    with open(master_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=master_fields)
        writer.writeheader()
        writer.writerows(master_rows)
    print(f"Updated: {master_path}")

    # --- 2. Generate HubSpot contacts CSV ---
    contacts_path = os.path.join(HUBSPOT_DIR, "hubspot_contacts_import_benelux.csv")
    hs_contact_fields = [
        "First Name", "Last Name", "Email", "Job Title",
        "LinkedIn URL", "Associated Company Domain", "Associated Company Name"
    ]
    hs_rows = []
    for row in master_rows:
        domain = row.get("domain", "").lower().strip()
        c = contact_map.get(domain, {})
        hs_rows.append({
            "First Name": c.get("first_name", ""),
            "Last Name": c.get("last_name", ""),
            "Email": "",
            "Job Title": c.get("job_title", "") if c else row.get("target_contact_role", ""),
            "LinkedIn URL": c.get("linkedin_url", ""),
            "Associated Company Domain": row.get("domain", ""),
            "Associated Company Name": row.get("company_name", ""),
        })

    with open(contacts_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=hs_contact_fields)
        writer.writeheader()
        writer.writerows(hs_rows)
    print(f"Updated: {contacts_path}")

    # --- 3. Generate gaps report ---
    gaps_path = os.path.join(GAPS_DIR, "hubspot_gaps_report_benelux.csv")
    gap_fields = ["Company", "Domain", "City", "Country", "Client Tier", "Gap Type", "Action Required", "Priority"]
    gap_rows = []
    for row in master_rows:
        domain = row.get("domain", "").lower().strip()
        c = contact_map.get(domain, {})
        gaps = []

        # Check if contact is missing entirely
        if not c:
            gaps.append(("MISSING_CONTACT", f"Find {row.get('target_contact_role', 'contact')}", "HIGH"))
        else:
            # Check if LinkedIn URL is missing
            if not c.get("linkedin_url"):
                gaps.append(("MISSING_LINKEDIN", f"Find LinkedIn URL for {c.get('first_name', '')} {c.get('last_name', '')}", "MEDIUM"))

        for gap_type, action, priority in gaps:
            gap_rows.append({
                "Company": row.get("company_name", ""),
                "Domain": domain,
                "City": row.get("city", ""),
                "Country": row.get("country", ""),
                "Client Tier": row.get("client_tier", ""),
                "Gap Type": gap_type,
                "Action Required": action,
                "Priority": priority,
            })

    with open(gaps_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=gap_fields)
        writer.writeheader()
        writer.writerows(gap_rows)
    print(f"Updated: {gaps_path}")

    # --- Summary ---
    total = len(master_rows)
    with_contact = matched
    with_linkedin = sum(1 for d, f, l, t, li in CONTACTS if li)
    missing_contact = total - with_contact
    missing_linkedin = with_contact - with_linkedin

    print(f"\n{'='*60}")
    print(f"ENRICHMENT SUMMARY")
    print(f"{'='*60}")
    print(f"Total companies:          {total}")
    print(f"With contact found:       {with_contact} ({with_contact*100//total}%)")
    print(f"  - With LinkedIn URL:    {with_linkedin}")
    print(f"  - Missing LinkedIn URL: {missing_linkedin}")
    print(f"Missing contact entirely: {missing_contact}")
    print(f"Total gaps:               {len(gap_rows)}")
    print(f"{'='*60}")

    if unmatched_domains:
        print(f"\nCompanies still needing contacts ({len(unmatched_domains)}):")
        for name, domain in unmatched_domains:
            print(f"  - {name} ({domain})")


if __name__ == "__main__":
    main()
