#!/usr/bin/env python3
"""
Benelux Target List Consolidation Script
=========================================
Consolidates research from 6 streams into:
- master_target_list_benelux.csv
- hubspot_companies_import_benelux.csv
- hubspot_contacts_import_benelux.csv
- hubspot_gaps_report_benelux.csv
"""

import csv
import os
import re
from collections import defaultdict

# Output paths
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_DIR = os.path.join(BASE, "02_master_lists")
HUBSPOT_DIR = os.path.join(BASE, "01_hubspot_import")
GAPS_DIR = os.path.join(BASE, "03_gaps_and_enrichment")

# ============================================================
# ICP INDUSTRY CLASSIFICATION
# ============================================================
TIER1_KEYWORDS = [
    'manufacturing', 'industrial', 'machinery', 'machine', 'maschinenbau',
    'automotive', 'chemicals', 'chemical', 'building materials', 'electrical',
    'electronic', 'semiconductor', 'plastics', 'packaging', 'metal',
    'renewables', 'defense', 'defence', 'aerospace', 'software', 'saas',
    'it services', 'it infrastructure', 'cybersecurity', 'cyber security',
    'cloud', 'enterprise software', 'erp', 'telecommunications', 'telecom',
    'computer hardware', 'food processing', 'mechatronics', 'high-tech',
    'hightech', 'precision', 'automation', 'robotics', 'sensor',
    'steel', 'aluminium', 'aluminum', 'composites', 'textiles',
    'shipbuilding', 'marine', 'dredging', 'offshore', 'wind',
    'insulation', 'ventilation', 'hvac', 'heating', 'coating',
    'printing', 'instrumentation', 'optics', 'photonics',
    'recycling', 'water treatment', 'cleantech', 'energy',
]

TIER2_KEYWORDS = [
    'wholesale', 'distribution', 'distributor', 'groothandel',
    'technical wholesale', 'industrial distribution', 'mro',
    'logistics', 'supply chain', 'parts', 'components distribution',
]

AVOID_KEYWORDS = [
    'banking', 'insurance', 'investment', 'financial services',
    'consulting', 'legal', 'accounting', 'staffing', 'recruiting',
    'retail', 'consumer goods', 'food & beverages',
    'travel', 'tourism', 'music', 'education',
    'hospital', 'healthcare', 'government', 'public safety',
    'real estate',
]

# ============================================================
# ALL COMPANY DATA - 6 STREAMS
# ============================================================
# Format: (name, domain, city, region, country, industry, revenue_eur, employees, description, ownership, founded, wml, source)

def R(companies_tuples):
    """Convert tuples to dicts"""
    result = []
    for t in companies_tuples:
        result.append({
            'company_name': t[0], 'domain': t[1], 'city': t[2], 'region': t[3],
            'country': t[4], 'industry': t[5], 'revenue_eur': t[6],
            'employees': t[7], 'description': t[8], 'ownership': t[9],
            'founding_year': t[10], 'world_market_leader': t[11], 'source': t[12],
        })
    return result

# STREAM 1: NL Manufacturing & Industrial (80 companies)
S1 = R([
("ASM International","asm.com","Almere","Flevoland","NL","Semiconductor Equipment",2900000000,4558,"Designs and manufactures semiconductor process equipment including ALD and epitaxy tools for AI and EV chip fabrication.","Public (Euronext)",1968,"Yes - global leader in ALD equipment","NL_Manufacturing"),
("BE Semiconductor Industries (Besi)","besi.com","Duiven","Gelderland","NL","Semiconductor Assembly Equipment",607500000,1800,"Designs and manufactures semiconductor assembly equipment for die attach, packaging, and plating. 39% global market share.","Public (Euronext)",1995,"Yes - 39% global Die Bonder market","NL_Manufacturing"),
("Nexperia","nexperia.com","Nijmegen","Gelderland","NL","Semiconductor Manufacturing",1900000000,12500,"Produces essential discrete components shipping 100B+ products annually for automotive and industrial.","Private",2017,"Yes - one of world's largest discrete semiconductor producers","NL_Manufacturing"),
("Prodrive Technologies","prodrive-technologies.com","Eindhoven","Noord-Brabant","NL","High-Tech Electronics / Mechatronics",552000000,2000,"Designs and manufactures high-tech electronics, software, and mechatronic products. Key ASML Tier-1 supplier.","Private (founder-led)",1993,"No","NL_Manufacturing"),
("NTS Group","nts-group.com","Eindhoven","Noord-Brabant","NL","Precision Manufacturing",180000000,1800,"First-tier contract manufacturer of precision machine components for semiconductor and analytical OEMs.","Private (NPM Capital)",1987,"No","NL_Manufacturing"),
("KMWE Group","kmwe.com","Eindhoven","Noord-Brabant","NL","Precision Manufacturing / Aerospace",100000000,880,"Precision machining specialist for aerospace OEMs and high-tech equipment industry (ASML).","Private",1955,"No","NL_Manufacturing"),
("Sioux Technologies","sioux.eu","Eindhoven","Noord-Brabant","NL","High-Tech Systems / Mechatronics",150000000,1200,"Strategic high-tech solutions partner for ASML, Philips, Thermo Fisher, and Zeiss.","Private",1996,"No","NL_Manufacturing"),
("Frencken Europe","frenckengroup.com","Eindhoven","Noord-Brabant","NL","Precision Manufacturing / Mechatronics",55000000,455,"Develops complex advanced modules for semiconductor and medical OEMs.","Public (SGX-listed)",1949,"No","NL_Manufacturing"),
("Boschman Technologies","boschman.nl","Duiven","Gelderland","NL","Semiconductor Packaging Equipment",30000000,120,"Advanced semiconductor packaging equipment including transfer molding and sintering systems.","Private",1987,"No","NL_Manufacturing"),
("Demcon","demcon.com","Enschede","Overijssel","NL","High-Tech Systems / Engineering",185000000,1000,"Develops and produces high-tech technology for healthcare, energy, production, and semiconductor sectors.","Private",1993,"No","NL_Manufacturing"),
("VDL Groep","vdlgroep.com","Eindhoven","Noord-Brabant","NL","Industrial Manufacturing / Automotive",4280000000,14241,"International industrial conglomerate with 100+ subsidiaries in subcontracting, buses, and high-tech systems.","Family-owned",1953,"No","NL_Manufacturing"),
("Aalberts Industries","aalberts.com","Utrecht","Utrecht","NL","Industrial Manufacturing / Flow Control",3000000000,14402,"Mission-critical technologies: flow control, surface technologies, semiconductor equipment. 135 locations.","Public (Euronext)",1975,"Yes - leading global position in flow control","NL_Manufacturing"),
("TKH Group","tkhgroup.com","Haaksbergen","Overijssel","NL","Technology / Smart Vision / Connectivity",1900000000,6000,"Smart Vision, Smart Manufacturing (tire building via VMI), Smart Connectivity (fiber optic).","Public (Euronext)",1930,"Yes - via VMI in tire building machinery","NL_Manufacturing"),
("VMI Group","vmi-group.com","Epe","Gelderland","NL","Tire Building Machinery",500000000,1000,"20% of the 1.2 billion tires produced yearly worldwide are manufactured on VMI machines.","Subsidiary (TKH Group)",1945,"Yes - world market leader in tire building systems","NL_Manufacturing"),
("DAF Trucks","daf.com","Eindhoven","Noord-Brabant","NL","Truck Manufacturing",3500000000,6186,"Designs and manufactures heavy-duty trucks with engine factory and final assembly in Eindhoven.","Subsidiary (PACCAR)",1928,"No","NL_Manufacturing"),
("Inalfa Roof Systems","inalfa.com","Venray","Limburg","NL","Automotive Supplier / Roof Systems",1350000000,5000,"Designs, develops and manufactures automotive roof systems for world's largest car brands.","Private (BAIC Group)",1946,"Yes - world market leader in automotive roof systems","NL_Manufacturing"),
("Koninklijke Nedschroef","nedschroef.com","Helmond","Noord-Brabant","NL","Automotive Supplier / Fasteners",570000000,2300,"Develops and supplies fasteners and special parts for automotive, aviation and manufacturing at 20 locations.","Private",1894,"No","NL_Manufacturing"),
("Vanderlande Industries","vanderlande.com","Veghel","Noord-Brabant","NL","Logistics Automation / Material Handling",2100000000,9000,"World-leading supplier of baggage handling systems for 600+ airports and automated warehouse solutions.","Subsidiary (Toyota Industries)",1949,"Yes - world leader in airport baggage handling","NL_Manufacturing"),
("Damen Shipyards Group","damen.com","Gorinchem","Zuid-Holland","NL","Shipbuilding / Defense / Maritime",3000000000,12500,"Netherlands' largest shipbuilding group with 50+ shipyards delivering 150+ vessels annually.","Family-owned",1927,"Yes - world leader in standardized shipbuilding","NL_Manufacturing"),
("Royal IHC","royalihc.com","Kinderdijk","Zuid-Holland","NL","Shipbuilding / Dredging Equipment",436000000,3000,"Develops and constructs specialized ships and equipment for dredging and offshore industries.","Private consortium",1943,"Yes - world leader in dredging vessel design","NL_Manufacturing"),
("Boskalis","boskalis.com","Papendrecht","Zuid-Holland","NL","Dredging / Maritime Infrastructure",4400000000,6719,"Leading global services provider in dredging, maritime infrastructure, and offshore energy support.","Private (HAL Investments)",1910,"Yes - one of world's largest dredging companies","NL_Manufacturing"),
("Van Oord","vanoord.com","Rotterdam","Zuid-Holland","NL","Dredging / Offshore Wind / Marine",2500000000,6000,"Global marine contractor for dredging, offshore wind installation with 155+ years of experience.","Family-owned",1868,"No","NL_Manufacturing"),
("Heerema Marine Contractors","heerema.com","Leiden","Zuid-Holland","NL","Offshore Construction / Heavy Lift",4500000000,3761,"Operates three of the largest crane vessels in the offshore industry.","Private (Heerema family)",1948,"Yes - operates world's largest semi-submersible crane vessels","NL_Manufacturing"),
("Mammoet","mammoet.com","Schiedam","Zuid-Holland","NL","Heavy Lifting / Engineered Transport",5000000000,7000,"World's largest engineered heavy-lifting and transport company.","Private (SHV Holdings)",1971,"Yes - world's largest heavy lift and transport company","NL_Manufacturing"),
("Huisman Equipment","huismanequipment.com","Schiedam","Zuid-Holland","NL","Heavy Lift Cranes / Offshore Equipment",680000000,2200,"Designs and manufactures heavy lifting equipment for renewable energy and offshore.","Private",1929,"Yes - world leader in heavy-lift crane design","NL_Manufacturing"),
("Koninklijke Vopak","vopak.com","Rotterdam","Zuid-Holland","NL","Industrial Tank Storage",1300000000,5618,"World's leading independent tank storage company for chemicals, oil, gases, LNG, and biofuels.","Public (Euronext)",1616,"Yes - world's largest independent tank storage company","NL_Manufacturing"),
("Thales Nederland","thalesgroup.com","Hengelo","Overijssel","NL","Defense Electronics / Naval Radar",800000000,2800,"Manufactures naval defense systems including sensors, radars, IR systems and air defense.","Subsidiary (Thales Group)",1922,"Yes - world leader in naval radar","NL_Manufacturing"),
("Fokker Technologies","gknaerospace.com","Papendrecht","Zuid-Holland","NL","Aerospace Manufacturing",500000000,4000,"Develops aerostructures, landing gear and electrical wiring for aerospace and defense.","Subsidiary (GKN / Melrose)",1919,"No","NL_Manufacturing"),
("TenCate","tencate.com","Nijverdal","Overijssel","NL","Technical Textiles / Defense Composites",500000000,700,"Technical textiles for defense, aerospace composites, protective clothing, and geosynthetics.","Private",1704,"Yes - world leader in antiballistic protection fabrics","NL_Manufacturing"),
("Marel / JBT Marel","jbtmarel.com","Boxmeer","Noord-Brabant","NL","Food Processing Equipment",1000000000,2000,"Major food processing equipment manufacturer for poultry, meat, and fish industries.","Subsidiary (JBT Marel)",1963,"Yes - one of top-2 global food processing equipment companies","NL_Manufacturing"),
("Meyn Food Processing","meyn.com","Oostzaan","Noord-Holland","NL","Poultry Processing Equipment",250000000,1000,"Global market leader in poultry processing equipment at speeds up to 15,000 birds/hour.","Private",1959,"Yes - world market leader in poultry processing","NL_Manufacturing"),
("Moba Group","moba.net","Barneveld","Gelderland","NL","Egg Grading / Packing Equipment",237000000,800,"World-leading manufacturer of egg grading and packing machines from 14 locations worldwide.","Family-owned",1947,"Yes - world market leader in egg grading equipment","NL_Manufacturing"),
("Kiremko","kiremko.com","Montfoort","Utrecht","NL","Potato Processing Equipment",50000000,250,"Designs, manufactures and installs complete processing lines for French fries and chips.","Private",1965,"Yes - world leader in potato processing equipment","NL_Manufacturing"),
("Lely Industries","lely.com","Maassluis","Zuid-Holland","NL","Agricultural Robotics / Dairy Equipment",400000000,2000,"World-leading dairy robot manufacturer with 135,000+ robots deployed globally.","Family-owned",1948,"Yes - world market leader in robotic milking systems","NL_Manufacturing"),
("Stahl Holdings","stahl.com","Waalwijk","Noord-Brabant","NL","Specialty Chemicals / Coatings",600000000,1900,"Global leader in specialty coatings for flexible materials including leather and textiles.","PE-backed",1930,"Yes - world market leader in leather processing chemicals","NL_Manufacturing"),
("Holland Colours","hollandcolours.com","Apeldoorn","Gelderland","NL","Specialty Chemicals / Color Masterbatch",106000000,400,"Develops and produces colorants, masterbatches and additives for PVC and PET.","Public (Euronext)",1979,"No","NL_Manufacturing"),
("OCI Nitrogen","oci-global.com","Geleen","Limburg","NL","Chemicals / Nitrogen / Fertilizers",1000000000,800,"Leading European nitrogen fertilizer and world's largest melamine producer at Chemelot campus.","Public (Euronext)",1929,"Yes - world's largest melamine producer","NL_Manufacturing"),
("AnQore","anqore.com","Geleen","Limburg","NL","Chemicals / Acrylonitrile",200000000,300,"Specialist chemical supplier at Chemelot campus. Formerly DSM Acrylonitrile.","Private",2015,"No","NL_Manufacturing"),
("BDR Thermea Group","bdrthermeagroup.com","Apeldoorn","Gelderland","NL","Heating Equipment / Heat Pumps",1800000000,7100,"Leading manufacturer of heating appliances under brands Remeha, Baxi, De Dietrich.","Private",1935,"No","NL_Manufacturing"),
("Wavin","wavin.com","Zwolle","Overijssel","NL","Plastics / Pipe Systems",800000000,3000,"Global manufacturer of plastic pipes and fittings for drainage and water supply.","Subsidiary (Orbia)",1955,"Yes - European market leader in plastic piping","NL_Manufacturing"),
("Heras","heras.com","Oirschot","Noord-Brabant","NL","Perimeter Security / Fencing",220000000,1100,"Europe's leading provider of perimeter protection solutions.","Private (Garda Group)",1952,"Yes - European market leader in perimeter security","NL_Manufacturing"),
("Royal Boon Edam","boonedam.com","Edam","Noord-Holland","NL","Entrance Solutions / Revolving Doors",200000000,1000,"Premium manufacturer of revolving doors, security portals and turnstiles. 150+ years.","Family-owned",1873,"Yes - world leader in revolving doors","NL_Manufacturing"),
("WILA","wilatooling.com","Lochem","Gelderland","NL","Press Brake Tooling",68000000,350,"World-leading manufacturer of clamping and tooling systems for press brakes.","Private",1963,"Yes - world market leader in press brake tooling","NL_Manufacturing"),
("AWL-Techniek","awl.nl","Harderwijk","Gelderland","NL","Robotic Welding / Automation",148000000,750,"Global system integrator for robotic welding, material handling and logistics automation.","Private",1993,"No","NL_Manufacturing"),
("Holmatro","holmatro.com","Raamsdonksveer","Noord-Brabant","NL","Hydraulic Equipment / Rescue Tools",100000000,500,"Dutch multinational manufacturing hydraulic equipment for industrial and rescue operations.","Family-owned",1967,"Yes - world leader in hydraulic rescue tools","NL_Manufacturing"),
("Bronkhorst High-Tech","bronkhorst.com","Ruurlo","Gelderland","NL","Flow Measurement Instrumentation",100000000,500,"World-leading manufacturer of mass flow meters and controllers for gases and liquids.","Private",1981,"Yes - world leader in low-flow mass flow measurement","NL_Manufacturing"),
("Malvern Panalytical","malvernpanalytical.com","Almelo","Overijssel","NL","Analytical Instruments",300000000,2000,"Manufactures X-ray analytical instruments and particle characterization equipment.","Subsidiary (Spectris)",1948,"Yes - world leader in X-ray diffraction instruments","NL_Manufacturing"),
("Kendrion","kendrion.com","Amsterdam","Noord-Holland","NL","Electromagnetic Actuators",460000000,2500,"Designs electromagnetic actuators for wind turbines, robots, EVs, factory automation.","Public (Euronext)",1859,"No","NL_Manufacturing"),
("Tata Steel Nederland","tatasteelnederland.com","IJmuiden","Noord-Holland","NL","Steel Manufacturing",8000000000,11500,"Netherlands' only integrated steel producer making 7M tonnes of strip steel per year.","Subsidiary (Tata Steel)",1918,"No","NL_Manufacturing"),
("SIF Group","sfrholding.com","Roermond","Limburg","NL","Offshore Wind Foundations",400000000,600,"Produces monopiles for offshore wind turbines at Roermond and Maasvlakte facilities.","Public (Euronext)",1948,"Yes - top-3 global offshore wind monopile producer","NL_Manufacturing"),
("Fugro","fugro.com","Leidschendam","Zuid-Holland","NL","Geo-data / Marine Survey",2100000000,11219,"World's leading geo-data specialist for offshore energy, infrastructure and construction.","Public (Euronext)",1962,"Yes - world leader in marine geo-data","NL_Manufacturing"),
("Bollegraaf Recycling Machinery","bollegraaf.com","Appingedam","Groningen","NL","Recycling Machinery",50000000,228,"World leader in designing and producing turnkey recycling solutions.","Private",1961,"Yes - world leader in recycling sorting systems","NL_Manufacturing"),
("Contiweb","contiweb.com","Boxmeer","Noord-Brabant","NL","Printing Equipment / Web Handling",70000000,150,"Global market leader in auxiliary equipment for offset printing.","Private",2004,"Yes - world market leader in web offset auxiliary equipment","NL_Manufacturing"),
("Batenburg Techniek","batenburg.nl","Rotterdam","Zuid-Holland","NL","Industrial Automation / Technical",200000000,1253,"Industrial technology company making processes smarter, safer and more sustainable.","Private",1911,"No","NL_Manufacturing"),
("ERIKS","eriks.com","Alkmaar","Noord-Holland","NL","Industrial Distribution / Engineering",1730000000,7500,"Specialized industrial service provider distributing 600,000+ components to 200,000+ customers.","PE-backed (Lone Star)",1940,"No","NL_Manufacturing"),
("Koninklijke Gazelle","gazelle.nl","Dieren","Gelderland","NL","Bicycle / E-bike Manufacturing",400000000,1000,"Netherlands' most iconic bicycle manufacturer. Dutch market leader in premium segment.","Subsidiary (Pon Holdings)",1892,"No","NL_Manufacturing"),
("Pon Holdings","pon.com","Almere","Flevoland","NL","Automotive Distribution / Industrial",8000000000,16000,"Family-owned mobility and industrial services group distributing VW, MAN, Caterpillar.","Family-owned",1895,"No","NL_Manufacturing"),
("Photonis Netherlands","photonis.com","Roden","Drenthe","NL","Defense / Night Vision",200000000,500,"Supplies 68% of global demand for night vision image intensifier tubes.","Private",1937,"Yes - 68% global demand for night vision tubes","NL_Manufacturing"),
("Airborne Composites","airborne.com","The Hague","Zuid-Holland","NL","Aerospace / Advanced Composites",50000000,200,"Advanced composite products and automated manufacturing systems for aerospace and defense.","Private",1995,"No","NL_Manufacturing"),
("Lamb Weston / Meijer","lambweston.eu","Kruiningen","Zeeland","NL","Food Processing / Potato Products",1500000000,1400,"One of world's largest potato processors. 700,000+ tonne capacity at 4 Dutch factories.","JV (Lamb Weston / Meijer)",1958,"Yes - top-3 global potato processor","NL_Manufacturing"),
("Royal Cosun","cosun.com","Breda","Noord-Brabant","NL","Food Processing / Agri-Industrial",2300000000,4100,"Cooperative with Sensus (chicory inulin), Aviko (potato) and SVZ (fruit/veg).","Cooperative",1899,"Yes - world leader in chicory root inulin","NL_Manufacturing"),
("Perfetti Van Melle","perfettivanmelle.com","Breda","Noord-Brabant","NL","Food Manufacturing / Confectionery",3700000000,18000,"One of world's largest confectionery companies producing Mentos, Chupa Chups.","Private (Family)",1946,"No","NL_Manufacturing"),
("Strukton","strukton.com","Utrecht","Utrecht","NL","Rail Infrastructure / Civil Engineering",500000000,2500,"Design, construction and maintenance of rail systems and civil infrastructure.","Private",1921,"No","NL_Manufacturing"),
("Signify","signify.com","Eindhoven","Noord-Brabant","NL","Lighting Technology / IoT",6700000000,10000,"World leader in lighting. Connected lighting systems with Philips and Interact brands.","Public (Euronext)",1891,"Yes - world leader in lighting","NL_Manufacturing"),
("NXP Semiconductors","nxp.com","Eindhoven","Noord-Brabant","NL","Semiconductors",12200000000,34000,"Secure connectivity for automotive, industrial, IoT and mobile applications.","Public (Nasdaq)",1953,"No","NL_Manufacturing"),
("Neways Electronics","neways.nl","Son","Noord-Brabant","NL","Electronics Manufacturing",644000000,3000,"Contract electronics manufacturer for telecom, medical, industrial, defense, automotive.","Public",1969,"No","NL_Manufacturing"),
("Voortman Steel Machinery","voortman.net","Rijssen","Overijssel","NL","Steel Processing Machinery",200000000,550,"CNC-controlled machines for steel construction industry.","Family-owned",1969,"No","NL_Manufacturing"),
("247TailorSteel","247tailorsteel.com","Varsseveld","Gelderland","NL","Online Steel Processing",120000000,360,"Custom laser-cut/bent steel via Sophia AI platform. Facilities in NL, BE, DE.","Private",2007,"No","NL_Manufacturing"),
("Bakker Magnetics","bakkermagnetics.com","Son","Noord-Brabant","NL","Magnetic Solutions Manufacturing",17000000,100,"Permanent magnet assemblies for e-mobility, renewable energy, marine, metal separation.","Family-owned",1971,"No","NL_Manufacturing"),
("Nooteboom Trailers","nooteboom.com","Wijchen","Gelderland","NL","Trailer Manufacturing (Heavy Transport)",100000000,500,"European market leader in abnormal road transport vehicles. Payload 20-200 tonnes.","Family-owned",1881,"No","NL_Manufacturing"),
("Ebusco","ebusco.com","Deurne","Noord-Brabant","NL","Electric Bus Manufacturing",30000000,345,"Developer and manufacturer of zero-emission buses and charging systems.","Public (Euronext)",2012,"No","NL_Manufacturing"),
("Hoppenbrouwers Techniek","hoppenbrouwers.nl","Udenhout","Noord-Brabant","NL","Technical Services / Installation",500000000,3000,"Royal technical service provider for electrical and mechanical engineering. 100+ years.","Private",1918,"No","NL_Manufacturing"),
])

# STREAM 2: NL IT/Software/SaaS (64 companies - selecting top ICP matches)
S2 = R([
("AFAS Software","afas.nl","Leusden","Utrecht","NL","Enterprise Software (ERP/HRM)",200000000,720,"Family-owned Dutch ERP software serving 14,000+ clients with integrated business software.","Family-owned",1996,"No","NL_IT_Software"),
("Exact Software","exact.com","Delft","Zuid-Holland","NL","Enterprise Software (ERP/Accounting)",230000000,2000,"Cloud and on-premises ERP and accounting software for 100,000+ SMEs.","PE-backed (KKR)",1984,"No","NL_IT_Software"),
("Unit4","unit4.com","Utrecht","Utrecht","NL","Enterprise Software (ERP/FP&A/HCM)",400000000,2600,"Enterprise software for people-centric organisations. 6,000+ customers.","PE-backed (TA Associates)",1980,"No","NL_IT_Software"),
("Topicus.com","topicus.com","Deventer","Overijssel","NL","Vertical Market Software",494000000,8000,"Pan-European provider of vertical market software platforms across healthcare, education, finance.","Public (TSX-V)",2000,"No","NL_IT_Software"),
("TOPdesk","topdesk.com","Delft","Zuid-Holland","NL","Enterprise Software (ITSM/ESM)",175000000,900,"IT service management and enterprise service management SaaS platform. Offices in 8 countries.","Private (founder-led)",1993,"No","NL_IT_Software"),
("Adyen","adyen.com","Amsterdam","Noord-Holland","NL","Fintech / Payments Infrastructure",1996000000,4350,"Global payment platform enabling businesses to accept payments across all channels.","Public (Euronext)",2006,"No","NL_IT_Software"),
("Mollie","mollie.com","Amsterdam","Noord-Holland","NL","Fintech / B2B Payments",120000000,900,"B2B payments platform serving 250,000+ businesses with online payment processing.","PE-backed (unicorn)",2004,"No","NL_IT_Software"),
("Backbase","backbase.com","Amsterdam","Noord-Holland","NL","Fintech / Banking Platform Software",390000000,1940,"AI-powered Engagement Banking Platform helping 150+ financial institutions.","Private (founder-led)",2003,"No","NL_IT_Software"),
("Conclusion","conclusion.nl","Utrecht","Utrecht","NL","IT Services / Business Transformation",240000000,2800,"#1 IT service provider in NL. Multidisciplinary IT services for public transport, healthcare, finance.","PE-backed (NPM Capital)",2003,"No","NL_IT_Software"),
("Ordina","ordina.nl","Nieuwegein","Utrecht","NL","IT Consulting / Application Services",425000000,3000,"IT consulting and professional services for public sector, financial services in the Benelux.","Subsidiary (Sopra Steria)",1973,"No","NL_IT_Software"),
("Centric","centric.eu","Gouda","Zuid-Holland","NL","IT Services / Software / Outsourcing",435000000,4000,"Full-service IT company: software, outsourcing, BPO, staffing. Active across NL, BE, DE.","Private",1992,"No","NL_IT_Software"),
("ilionx","ilionx.com","Utrecht","Utrecht","NL","IT Services / Software Development",150000000,1400,"IT services: consultation, software development, implementation for government and SMEs.","Private",2004,"No","NL_IT_Software"),
("OGD ict-diensten","ogd.nl","Delft","Zuid-Holland","NL","IT Services / Infrastructure",150000000,1400,"Full-service IT provider: infrastructure, end-user management, software, BI, service desk.","PE-backed",1988,"No","NL_IT_Software"),
("Ctac","ctac.nl","'s-Hertogenbosch","Noord-Brabant","NL","IT Consulting (SAP/ERP)",127000000,460,"SAP and Microsoft specialist: ERP, data services, cybersecurity. Listed on Euronext.","Public (Euronext)",1992,"No","NL_IT_Software"),
("Schuberg Philis","schubergphilis.com","Schiphol-Rijk","Noord-Holland","NL","Managed IT Infrastructure / Cloud",88000000,490,"Premium managed IT services. Ranked #1 IT company in NL by Whitelane Research.","PE-backed (Bridgepoint)",2001,"No","NL_IT_Software"),
("Plat4mation","plat4mation.com","Utrecht","Utrecht","NL","IT Services (ServiceNow Partner)",80000000,650,"Largest pure-play ServiceNow Elite Partner in EMEA. 30% CAGR.","Private",2013,"No","NL_IT_Software"),
("Leaseweb","leaseweb.com","Amsterdam","Noord-Holland","NL","Cloud Infrastructure / IaaS",220000000,560,"Global IaaS provider with 26 data centers and 80,000+ servers.","Private",1997,"No","NL_IT_Software"),
("Eurofiber","eurofiber.com","Maarssen","Utrecht","NL","Telecommunications / Fiber Infrastructure",217000000,450,"Critical fiber-optic infrastructure: 76,000 km network across NL/BE/FR/DE.","PE-backed (Antin)",2000,"No","NL_IT_Software"),
("Fox-IT","fox-it.com","Delft","Zuid-Holland","NL","Cybersecurity",50000000,350,"Leading Dutch cybersecurity: threat intelligence, forensics, MDR for government and defense.","Subsidiary (NCC Group)",1999,"No","NL_IT_Software"),
("Eye Security","eye.security","The Hague","Zuid-Holland","NL","Cybersecurity",20000000,100,"Protects European SMEs from cyber threats with endpoint monitoring and 24/7 response.","Private (VC-backed)",2020,"No","NL_IT_Software"),
("Elastic NV","elastic.co","Amsterdam","Noord-Holland","NL","Enterprise Software / Search & Analytics",1400000000,3500,"Dutch-founded platform for enterprise search, observability, and security.","Public (NYSE)",2012,"No","NL_IT_Software"),
("Bynder","bynder.com","Amsterdam","Noord-Holland","NL","B2B SaaS / Digital Asset Management",120000000,600,"DAM platform for brands. 20% of Fortune 500 are customers. Forrester Leader.","PE-backed",2013,"No","NL_IT_Software"),
("Bird","bird.com","Amsterdam","Noord-Holland","NL","Cloud Communications / CPaaS",800000000,900,"Cloud communications platform: SMS, voice, chat, email. 15,000+ customers in 170+ countries.","Private (VC-backed)",2011,"No","NL_IT_Software"),
("Sendcloud","sendcloud.com","Eindhoven","Noord-Brabant","NL","B2B SaaS / Shipping & Logistics",70000000,475,"All-in-one shipping platform for e-commerce: 100+ carriers, 60+ integrations.","Private (VC-backed)",2012,"No","NL_IT_Software"),
("Mendix","mendix.com","Rotterdam","Zuid-Holland","NL","Enterprise Software / Low-Code",200000000,1400,"Leading enterprise low-code application development platform. Gartner Leader.","Subsidiary (Siemens)",2005,"No","NL_IT_Software"),
("TomTom","tomtom.com","Amsterdam","Noord-Holland","NL","B2B Location Technology / Mapping",574000000,3500,"B2B location technology: maps and navigation for automotive OEMs. Microsoft and Uber client.","Public (Euronext)",1991,"No","NL_IT_Software"),
("Planon","planonsoftware.com","Nijmegen","Gelderland","NL","Enterprise Software (IWMS/FM)",155000000,1160,"Global leader in IWMS software for building and facilities management. 3,250 clients.","Subsidiary (Schneider Electric)",1982,"No","NL_IT_Software"),
("ORTEC","ortec.com","Zoetermeer","Zuid-Holland","NL","Enterprise Software / Optimization",195000000,1100,"Mathematical optimization and analytics for supply chain, logistics, workforce planning.","Private",1981,"No","NL_IT_Software"),
("Nedap","nedap.com","Groenlo","Gelderland","NL","Technology / Security & IoT",262000000,900,"Technology company: security management, healthcare, retail RFID, staffing. Listed since 1947.","Public (Euronext)",1929,"No","NL_IT_Software"),
("Wortell","wortell.nl","Lijnden","Noord-Holland","NL","Managed IT / Microsoft Cloud",50000000,350,"Leading Microsoft Cloud partner. Own SOC. 2x Microsoft Partner of the Year NL.","PE-backed",1997,"No","NL_IT_Software"),
("Enreach","enreach.com","Amersfoort","Utrecht","NL","Telecommunications / UCaaS / CCaaS",200000000,500,"European UCaaS/CCaaS leader: cloud communications, VoIP, contact center.","PE-backed (Waterland)",2018,"No","NL_IT_Software"),
("Software Improvement Group","softwareimprovementgroup.com","Amsterdam","Noord-Holland","NL","Software Quality & Security Analytics",30000000,250,"World's first ISO/IEC 17025 accredited software quality lab. 400+ enterprise clients.","Private",2000,"No","NL_IT_Software"),
("Thinkwise","thinkwisesoftware.com","Apeldoorn","Gelderland","NL","Enterprise Software / Low-Code ERP",20000000,143,"Only vendor globally with a low-code platform for custom ERP. 32+ countries.","Private (founder-led)",2002,"No","NL_IT_Software"),
("DataSnipper","datasnipper.com","Amsterdam","Noord-Holland","NL","Software / AI Automation",50000000,200,"Intelligent automation platform for auditors. 400,000+ users in 125 countries.","Private (VC-backed)",2017,"No","NL_IT_Software"),
("Effectory","effectory.com","Amsterdam","Noord-Holland","NL","Software / SaaS (Employee Feedback)",38000000,251,"Europe's largest provider of employee feedback SaaS solutions. 1,000+ organizations in 110 countries.","Private",1996,"No","NL_IT_Software"),
("Nearfield Instruments","nearfieldinstruments.com","Rotterdam","Zuid-Holland","NL","Semiconductor Metrology",10000000,50,"Advanced metrology and inspection for semiconductor industry. Deloitte Fast 50 Deep-Tech.","Private (VC-backed)",2016,"No","NL_IT_Software"),
("Qblox","qblox.com","Delft","Zuid-Holland","NL","Quantum Computing Hardware",10000000,50,"Global leader in scalable quantum control stacks.","Private (VC-backed)",2018,"No","NL_IT_Software"),
("Fastned","fastned.nl","Amsterdam","Noord-Holland","NL","EV Charging Infrastructure",60000000,300,"Builds and operates fast-charging stations across Europe with 100% renewable energy.","Public (Euronext)",2012,"No","NL_IT_Software"),
])

# STREAM 3: BE Manufacturing & Industrial (62 companies)
S3 = R([
("Bekaert","bekaert.com","Zwevegem","Flanders","BE","Steel Wire & Coatings",5100000000,28000,"Global leader in steel wire transformation and coatings for construction, automotive, energy.","Public (Euronext)",1880,"No","BE_Manufacturing"),
("Umicore","umicore.com","Brussels","Brussels","BE","Materials Technology & Recycling",3600000000,11000,"Global materials technology and recycling group for catalysis, energy, precious metals.","Public (Euronext)",1805,"No","BE_Manufacturing"),
("Solvay (Syensqo)","solvay.com","Brussels","Brussels","BE","Specialty Chemicals",5200000000,22000,"Major specialty chemicals group producing polymers and advanced materials.","Public (Euronext)",1863,"No","BE_Manufacturing"),
("Etex","etex.com","Zaventem","Flanders","BE","Building Materials",3808000000,13777,"Global manufacturer of lightweight building materials: fibre cement, plasterboard, insulation.","Family-owned",1905,"No","BE_Manufacturing"),
("Tessenderlo Group","tessenderlo.com","Brussels","Brussels","BE","Diversified Chemicals & Industrial",2900000000,7231,"Diversified industrial group: agro, industrial solutions, bio-valorization, machinery (Picanol).","Public (Euronext)",1919,"No","BE_Manufacturing"),
("Aliaxis","aliaxis.com","Brussels","Brussels","BE","Plastic Piping Systems",4100000000,14000,"Global leader in advanced plastic piping systems for building and infrastructure.","Private",1969,"No","BE_Manufacturing"),
("Soudal","soudalgroup.com","Turnhout","Flanders","BE","Sealants & Adhesives",1460000000,4500,"Largest independent European manufacturer of sealants, adhesives, and PU foams.","Family-owned",1966,"No","BE_Manufacturing"),
("Barco","barco.com","Kortrijk","Flanders","BE","Visualization & Display Technology",947000000,3600,"Digital projection, visualization, and collaboration for enterprise, entertainment, healthcare.","Public (Euronext)",1934,"No","BE_Manufacturing"),
("John Cockerill","johncockerill.com","Seraing","Wallonia","BE","Industrial Engineering & Defense",1200000000,4600,"Walloon industrial engineering: machinery for steel plants, boilers, defense, energy.","Private",1817,"No","BE_Manufacturing"),
("Vandewiele Group","vandewiele.com","Kortrijk","Flanders","BE","Textile Machinery",918000000,3827,"World leader in mechatronics solutions and textile machinery.","Family-owned",1880,"Yes - world leader in textile machinery","BE_Manufacturing"),
("Beaulieu International Group","bintg.com","Wielsbeke","Flanders","BE","Flooring & Technical Textiles",2000000000,4500,"Global specialist in flooring, engineered fibres, technical textiles, polymer raw materials.","Family-owned",1959,"No","BE_Manufacturing"),
("Puratos","puratos.com","Groot-Bijgaarden","Brussels","BE","B2B Food Ingredients",2500000000,10000,"International B2B supplier of bakery, patisserie, and chocolate ingredients. 100+ countries.","Family-owned",1919,"No","BE_Manufacturing"),
("Recticel","recticel.com","Brussels","Brussels","BE","Insulation & Polyurethane",529400000,1255,"Leading European manufacturer of insulation boards, panels, and acoustic solutions.","Public (Euronext)",1778,"No","BE_Manufacturing"),
("Picanol","picanol.be","Ieper","Flanders","BE","Weaving Machinery",500000000,1200,"High-tech airjet and rapier weaving machines used by 2,600+ mills worldwide.","Subsidiary (Tessenderlo)",1936,"No","BE_Manufacturing"),
("Sonaca","sonaca.com","Gosselies","Wallonia","BE","Aerospace Structures",633700000,3861,"Aerospace company specializing in advanced aerostructures and wing components.","SRIW-owned",1931,"No","BE_Manufacturing"),
("DEME Group","deme-group.com","Zwijndrecht","Flanders","BE","Dredging & Offshore Energy",4100000000,5822,"International marine engineering: dredging, offshore wind, environmental remediation.","Subsidiary (Ackermans & van Haaren)",1991,"No","BE_Manufacturing"),
("Jan De Nul Group","jandenul.com","Aalst","Flanders","BE","Dredging & Offshore Energy",2900000000,7491,"Family-owned dredging and marine engineering. Offshore wind installation, land reclamation.","Family-owned",1938,"No","BE_Manufacturing"),
("FN Herstal","fnherstal.com","Herstal","Wallonia","BE","Defense & Firearms",1000000000,3000,"World-leading manufacturer of small arms and weapon systems. 100+ countries.","Government-owned",1889,"Yes - world leader in small arms","BE_Manufacturing"),
("Agfa-Gevaert","agfa.com","Mortsel","Flanders","BE","Imaging & IT Solutions",1300000000,7000,"Digital imaging, IT systems for printing, healthcare, and industrial applications.","Public (Euronext)",1867,"No","BE_Manufacturing"),
("Sibelco","sibelco.com","Antwerp","Flanders","BE","Industrial Minerals",3000000000,5000,"Global specialist in industrial minerals: silica, clays, recycled glass.","Private",1872,"No","BE_Manufacturing"),
("Deceuninck","deceuninck.com","Hooglede-Gits","Flanders","BE","PVC Building Systems",857000000,3686,"Top 3 independent manufacturer of PVC profiles for windows, doors, building.","Public (Euronext)",1937,"No","BE_Manufacturing"),
("Lhoist","lhoist.com","Limelette","Wallonia","BE","Lime & Minerals",2500000000,6650,"World's leading producers of lime, dolime, and mineral solutions.","Family-owned",1889,"No","BE_Manufacturing"),
("Prayon","prayon.com","Engis","Wallonia","BE","Phosphate Chemistry",659500000,1500,"Global player in phosphorus chemistry for food, industrial, agricultural use.","JV (OCP / SRIW)",1882,"No","BE_Manufacturing"),
("Magotteaux","magotteaux.com","Vaux-sous-Chevremont","Wallonia","BE","Wear Solutions for Mining & Cement",750000000,2800,"World leader in grinding media and wear-resistant solutions for mining and cement.","Subsidiary (Sigdo Koppers)",1920,"Yes - world leader in grinding media","BE_Manufacturing"),
("AGC Glass Europe","agc-glass.eu","Louvain-la-Neuve","Wallonia","BE","Flat Glass Manufacturing",3000000000,14500,"European branch producing flat glass for construction, automotive, solar. 18 float glass lines.","Subsidiary (AGC Inc.)",1961,"No","BE_Manufacturing"),
("Reynaers Aluminium","reynaers.com","Duffel","Flanders","BE","Aluminium Building Systems",703000000,2650,"European leader in aluminium and steel building components for windows, doors, facades.","Family-owned",1965,"No","BE_Manufacturing"),
("Melexis","melexis.com","Ieper","Flanders","BE","Semiconductor Sensors (Automotive)",800000000,1500,"Integrated circuits and sensors for automotive electronics. 18 chips per new car average.","Public (Euronext)",1988,"No","BE_Manufacturing"),
("Renson","renson.eu","Waregem","Flanders","BE","Ventilation & Sun Protection",750000000,1300,"Innovative ventilation, sun protection, and outdoor living solutions.","Family-owned",1909,"No","BE_Manufacturing"),
("Smulders","smulders.com","Hoboken","Flanders","BE","Steel Construction / Offshore Wind",500000000,2000,"European market leader in steel structures for offshore wind foundations and bridges.","Subsidiary (Eiffage)",1966,"No","BE_Manufacturing"),
("EVS Broadcast Equipment","evs.com","Seraing","Wallonia","BE","Broadcast Video Technology",209000000,729,"Leading manufacturer of live video production hardware and software worldwide.","Public (Euronext)",1994,"No","BE_Manufacturing"),
("Niko Group","niko.eu","Sint-Niklaas","Flanders","BE","Electrical / Home Automation",200000000,750,"Belgian market leader in switching materials and smart building solutions.","Family-owned",1919,"No","BE_Manufacturing"),
("Bosal","bosal.com","Lummen","Flanders","BE","Automotive Exhaust & Towing Systems",400000000,2000,"Leading manufacturer of exhaust systems and towing equipment for OE and aftermarket.","Private",1923,"No","BE_Manufacturing"),
("Kabelwerk Eupen","eupen.com","Eupen","Wallonia","BE","Cables Pipes & Foams",230800000,800,"European manufacturer of power cables, communication cables, plastic pipes, synthetic foams.","Private",1747,"No","BE_Manufacturing"),
("Materialise","materialise.com","Leuven","Flanders","BE","3D Printing / Additive Manufacturing",250000000,2300,"Pioneer in 3D printing software solutions and manufacturing services.","Public (Nasdaq / Euronext)",1990,"No","BE_Manufacturing"),
("SABCA","sabca.be","Brussels","Brussels","BE","Aerospace Manufacturing",300000000,1200,"Metallic and composite aerostructures for civil aviation, defense, and space.","Private (Orizio / SFPIM)",1920,"No","BE_Manufacturing"),
("Plastiflex Group","plastiflex.com","Beringen","Flanders","BE","Flexible Tubing Systems",200000000,1100,"Global market leader in customized flexible tubing for healthcare and industrial.","PE-backed (IK Partners)",1953,"No","BE_Manufacturing"),
("Ontex Group","ontex.com","Aalst","Flanders","BE","Hygiene Products Manufacturing",2200000000,7000,"Major European manufacturer of disposable personal hygiene products for B2B.","Public (Euronext)",1979,"No","BE_Manufacturing"),
("Resilux","resilux.com","Wetteren","Flanders","BE","PET Packaging",400000000,500,"International manufacturer of PET preforms and bottles for beverages, food, cosmetics.","Public (Euronext)",1994,"No","BE_Manufacturing"),
("Oleon","oleon.com","Ertvelde","Flanders","BE","Oleochemicals",1000000000,1200,"Producer of oleochemical products from natural fats and oils for industrial applications.","Subsidiary (Avril Group)",1950,"No","BE_Manufacturing"),
("Vandemoortele","vandemoortele.com","Ghent","Flanders","BE","B2B Food Solutions",2000000000,4094,"Family-owned B2B food company: bakery products, margarines, plant-based food solutions.","Family-owned",1899,"No","BE_Manufacturing"),
("Punch Powertrain","punchpowertrain.com","Sint-Truiden","Flanders","BE","Automotive Powertrain",500000000,1500,"Developer and manufacturer of innovative automotive powertrains including CVT.","Private",2003,"No","BE_Manufacturing"),
("Sioen Industries","sioen.com","Ardooie","Flanders","BE","Technical Textiles & Protective Clothing",187000000,1200,"Global leader in technical textiles and professional protective clothing. 40+ locations.","Public (Euronext)",1960,"No","BE_Manufacturing"),
("Unilin","unilin.com","Wielsbeke","Flanders","BE","Flooring & Wood Panels",2600000000,7800,"Flooring, insulation, wood panels. Brands: Quick-Step, Moduleo, Pergo. 105 locations.","Subsidiary (Mohawk)",1960,"No","BE_Manufacturing"),
("BMT Aerospace","bmtaerospace.com","Oostkamp","Flanders","BE","Aerospace Manufacturing",100000000,560,"Flight safety gearing, gearbox assemblies, shafts and couplings for aircraft.","Private",1979,"No","BE_Manufacturing"),
("Vandersanden","vandersanden.com","Bilzen","Flanders","BE","Building Materials / Bricks",200000000,800,"Europe's largest family-owned producer of handform bricks. 10 production sites.","Family-owned",1925,"No","BE_Manufacturing"),
("AVR Machinery","avr.be","Roeselare","Flanders","BE","Agricultural Machinery",109000000,275,"Full range of potato and root crop cultivation machinery.","Family-owned (Dewulf)",1848,"No","BE_Manufacturing"),
("Dewulf Group","dewulfgroup.com","Roeselare","Flanders","BE","Agricultural Machinery",150000000,400,"Leading global manufacturer of agricultural machinery for potato and root crop.","Family-owned",1946,"No","BE_Manufacturing"),
("Nyrstar","nyrstar.com","Balen","Flanders","BE","Zinc Smelting & Metal Processing",3000000000,4000,"One of the world's largest zinc smelters producing SHG zinc and ZAMAK alloys.","Subsidiary (Trafigura)",1888,"No","BE_Manufacturing"),
("Aertssen Group","aertssen.be","Stabroek","Flanders","BE","Construction & Industrial Services",100000000,2500,"Authority in Belgium for infrastructure works, crane rental and exceptional transport.","Private",1963,"No","BE_Manufacturing"),
("Easyfairs","easyfairs.com","Ghent","Flanders","BE","B2B Events & Exhibitions",194000000,700,"Largest privately owned pan-European event company. 200+ events in 14 countries.","Private",1994,"No","BE_Manufacturing"),
])

# STREAM 4: BE IT/Software + Luxembourg (55 companies)
S4 = R([
("Odoo","odoo.com","Grand-Rosiere","Walloon Brabant","BE","ERP / Enterprise Software",400000000,6000,"Open-source ERP platform: CRM, accounting, inventory, manufacturing. Belgian unicorn.","Private (VC-backed)",2005,"No","BE_IT_Luxembourg"),
("Cegeka","cegeka.com","Hasselt","Limburg","BE","IT Services / Cloud / Managed Services",1300000000,10000,"Full-service ICT provider: cloud, security, managed infrastructure. 17 countries.","Family-owned",1992,"No","BE_IT_Luxembourg"),
("Cronos Group","cronos-groep.be","Kontich","Antwerp","BE","IT Services / Software",1600000000,9000,"Belgium's largest technology group: 500+ specialized companies in IT and digital.","Private (cooperative)",1991,"No","BE_IT_Luxembourg"),
("NRB Group","nrb.be","Herstal","Liege","BE","IT Infrastructure / Cloud",638000000,3670,"Major Belgian ICT player: consultancy, software, infrastructure, cloud services.","Private (Ethias/Nethys)",1987,"No","BE_IT_Luxembourg"),
("team.blue","team.blue","Ghent","East Flanders","BE","Cloud Hosting / Digital Services",850000000,4000,"European digital enablement platform: 3.3M SMB customers, 10.6M domains.","PE-backed (Hg Capital)",2019,"No","BE_IT_Luxembourg"),
("Materialise","materialise.com","Leuven","Flemish Brabant","BE","3D Printing Software & Services",267000000,2514,"Pioneer in 3D printing: software, medical devices, manufacturing services.","Public (Nasdaq)",1990,"No","BE_IT_Luxembourg"),
("Televic Group","televic.com","Izegem","West Flanders","BE","Communication Technology (B2B)",220000000,900,"High-end communication technology for conference, education, healthcare, rail.","Family-owned",1946,"No","BE_IT_Luxembourg"),
("Collibra","collibra.com","Brussels","Brussels-Capital","BE","Data Intelligence / Governance / SaaS",200000000,1024,"Data intelligence platform. Belgian unicorn. $5.25B valuation.","Private (VC-backed)",2008,"No","BE_IT_Luxembourg"),
("UnifiedPost Group","unifiedpostgroup.com","La Hulpe","Walloon Brabant","BE","Digital Document Processing / SaaS",191000000,1320,"Digital platform for e-invoicing, e-identity, e-payments. 484K+ subscription customers.","Public (Euronext)",2001,"No","BE_IT_Luxembourg"),
("Esko","esko.com","Ghent","East Flanders","BE","Packaging Software & Hardware",400000000,1700,"Global provider of packaging, labels, and publishing workflow automation.","Subsidiary (Veralto)",2001,"No","BE_IT_Luxembourg"),
("Efficy CRM","efficy.com","Brussels","Brussels-Capital","BE","CRM / Enterprise Software / SaaS",55000000,750,"Europe's leading flexible CRM. 13,500+ customers, 330,000+ users.","PE-backed",2005,"No","BE_IT_Luxembourg"),
("Showpad","showpad.com","Ghent","East Flanders","BE","Sales Enablement / SaaS",70000000,418,"Global leader in revenue enablement technology across 5 continents.","Private (VC-backed)",2011,"No","BE_IT_Luxembourg"),
("Lansweeper","lansweeper.com","Merelbeke","East Flanders","BE","IT Asset Management / SaaS",70000000,380,"IT asset management and discovery platform. $158M total raised.","Private (VC-backed)",2004,"No","BE_IT_Luxembourg"),
("TechWolf","techwolf.ai","Ghent","East Flanders","BE","AI / Workforce Intelligence / SaaS",30000000,80,"AI talent intelligence platform. $55M raised. Clients: United Airlines, IQVIA.","Private (VC-backed)",2018,"No","BE_IT_Luxembourg"),
("Deliverect","deliverect.com","Ghent","East Flanders","BE","Hospitality SaaS / B2B",42000000,500,"B2B SaaS unicorn for restaurant order integration. 10,000+ customers in 50+ markets.","Private (VC-backed)",2018,"No","BE_IT_Luxembourg"),
("Guardsquare","guardsquare.com","Leuven","Flemish Brabant","BE","Cybersecurity / Mobile App Security",20000000,150,"Leading mobile application security platform. KU Leuven spin-off.","Private (VC-backed)",2014,"No","BE_IT_Luxembourg"),
("Intigriti","intigriti.com","Antwerp","Antwerp","BE","Cybersecurity / Bug Bounty",15000000,100,"Crowdsourced cybersecurity platform connecting businesses with ethical hackers.","Private (VC-backed)",2016,"No","BE_IT_Luxembourg"),
("BrightAnalytics","brightanalytics.eu","Roeselare","West Flanders","BE","Financial Reporting Software / SaaS",5000000,50,"Consolidated financial and operational reporting platform. 1,000+ clients.","Private",2014,"No","BE_IT_Luxembourg"),
("Azumuta","azumuta.com","Ghent","East Flanders","BE","Manufacturing Software / SaaS",5000000,50,"Connected worker platform for manufacturing: digital work instructions, quality.","Private (VC-backed)",2020,"No","BE_IT_Luxembourg"),
("Peripass","peripass.com","Antwerp","Antwerp","BE","Logistics Software / SaaS",5000000,30,"Yard management SaaS for production plants. Clients: ArcelorMittal, Danone, DHL.","Private (VC-backed)",2016,"No","BE_IT_Luxembourg"),
("Xeryon","xeryon.com","Leuven","Flemish Brabant","BE","Precision Motion / Manufacturing",10000000,50,"World's smallest and fastest piezo motors. KU Leuven spin-off.","Private",2013,"No","BE_IT_Luxembourg"),
("Vertuoza","vertuoza.com","Nivelles","Walloon Brabant","BE","Construction Software / SaaS",10000000,50,"Construction management platform. EUR 1.6B invoiced through platform.","Private (VC-backed)",2018,"No","BE_IT_Luxembourg"),
("OTIV","otiv.ai","Ghent","East Flanders","BE","AI / Rail Automation",10000000,30,"AI-powered autonomous train solutions. Deloitte Fast 50 BE 2025 winner.","Private (VC-backed)",2020,"No","BE_IT_Luxembourg"),
# Luxembourg companies
("ArcelorMittal","arcelormittal.com","Luxembourg City","Luxembourg","LU","Steel Manufacturing",60000000000,3520,"World's second-largest steel producer. 9 industrial sites in Luxembourg.","Public (Euronext)",2006,"No","BE_IT_Luxembourg"),
("Aperam","aperam.com","Luxembourg City","Luxembourg","LU","Stainless & Specialty Steel",6500000000,11700,"Global stainless and specialty steel. Spun off from ArcelorMittal 2011.","Public (Euronext)",2011,"No","BE_IT_Luxembourg"),
("Ceratizit","ceratizit.com","Mamer","Luxembourg","LU","Hard Materials / Cutting Tools",800000000,7000,"Leading industrial group in hard material cutting tools and wear protection.","Private (Plansee Group)",1931,"No","BE_IT_Luxembourg"),
("Rotarex","rotarex.com","Lintgen","Luxembourg","LU","Gas Control Equipment",400000000,1400,"Global designer/manufacturer of premium gas control products. 100+ years.","Family-owned",1922,"No","BE_IT_Luxembourg"),
("Euro-Composites","euro-composites.com","Echternach","Luxembourg","LU","Composite Materials / Aerospace",140000000,1050,"Global composite materials manufacturer for aerospace, defense. NATO-approved.","Private (Schutz Group)",1694,"No","BE_IT_Luxembourg"),
("IEE Sensing","iee.lu","Bissen","Luxembourg","LU","Sensor Technology / Automotive",500000000,1019,"Sensing solutions: printed electronics, radar, 3D camera for automotive and industrial.","Private",1989,"No","BE_IT_Luxembourg"),
("SES","ses.com","Betzdorf","Luxembourg","LU","Satellite Telecommunications",2001000000,2118,"Global satellite operator providing video and data connectivity via GEO/MEO constellation.","Public (Euronext)",1985,"No","BE_IT_Luxembourg"),
("Circuit Foil Luxembourg","circuitfoil.com","Wiltz","Luxembourg","LU","Copper Foil Manufacturing",50000000,200,"Global manufacturer of copper foils for PCBs, electronics, and batteries.","Private",1967,"No","BE_IT_Luxembourg"),
("Ampacet","ampacet.com","Dudelange","Luxembourg","LU","Plastics / Masterbatch",1000000000,200,"Global masterbatch manufacturer for color and additive concentrates. EU HQ in LU.","Private (Family-owned)",1937,"No","BE_IT_Luxembourg"),
("LuxTrust","luxtrust.com","Luxembourg City","Luxembourg","LU","Digital Trust / Cybersecurity",25000000,100,"eIDAS-qualified trust service provider for digital signatures, eID, compliance.","Public-Private",2005,"No","BE_IT_Luxembourg"),
("HITEC Luxembourg","hitec.lu","Luxembourg City","Luxembourg","LU","Satellite Ground Segment / Space",8000000,37,"100% Luxembourg-owned. Satellite ground station antennas and mission-critical solutions.","Private",1986,"No","BE_IT_Luxembourg"),
])

# STREAM 5: Rankings & Hidden Champions (75 companies - many overlaps, selecting unique ones)
S5 = R([
("Severfield Steel Construction","severfield.eu","Rijssen","Overijssel","NL","Steel Construction",50000000,200,"Designs, manufactures and delivers steel construction projects. 30,000 tonnes annual capacity.","Subsidiary (UK)",1961,"No","Rankings"),
("ConstruSteel","construsteel.com","Den Ham","Overijssel","NL","Software / Construction Tech",10000000,30,"Market leader in Europe for specialized ERP/MRP software for steel construction.","Private",2000,"No","Rankings"),
("Nmbrs","nmbrs.com","Amsterdam","Noord-Holland","NL","Software / HR & Payroll",25000000,120,"Cloud-native HR and payroll software. 100,000+ companies. Part of Visma.","Subsidiary (Visma)",2008,"No","Rankings"),
("Vibe Group","vibegroup.com","Amsterdam","Noord-Holland","NL","IT Staffing & Consulting",215000000,342,"International IT staffing and consulting in NL, BE, DE.","Private",2011,"No","Rankings"),
("Berdal","berdal.com","Vaassen","Gelderland","NL","Rubber & Plastics Manufacturing",30000000,100,"European market leader in plastic and rubber products for construction.","Private",1945,"No","Rankings"),
("Prowise","prowise.com","Budel","Noord-Brabant","NL","EdTech / Hardware Manufacturing",60000000,162,"Interactive touchscreen displays and educational software. Made in Europe. 24+ countries.","Private (founder-led)",2013,"No","Rankings"),
("Iscal Sugar","iscal.be","Fontenoy","Wallonia","BE","Food Manufacturing",116000000,170,"World's first B Corp certified sugar company. Industrial and wholesale customers.","Private",2003,"No","Rankings"),
("Munckhof","munckhof.nl","Horst","Limburg","NL","Mobility Services / Transport",100000000,500,"Mobility and travel management company. Best Managed for 12 consecutive years.","Private",1925,"No","Rankings"),
("Banken Champignons Group","bankenchampignons.com","Maasdriel","Gelderland","NL","Food Processing / Agri",150000000,550,"International leader in mushroom cultivation and processing. Family business since 1956.","Family-owned",1956,"No","Rankings"),
("Van Mossel Automotive Group","vanmossel.com","Waalwijk","Noord-Brabant","NL","Automotive Distribution",9500000000,11097,"Largest automotive company in the Benelux. 150,000+ autos annually. 538 locations.","Private",1991,"No","Rankings"),
("Baril Coatings","barilcoatings.com","Dieren","Gelderland","NL","Chemical Manufacturing / Coatings",10000000,50,"Sustainable paint/coatings replacing fossil raw materials.","Private",1999,"No","Rankings"),
("Tree Composites","treecomposites.com","Delft","Zuid-Holland","NL","Advanced Materials / Composites",5000000,20,"TU Delft spin-off. Composite connection tech for offshore wind foundations.","Private",2018,"No","Rankings"),
("BENGglas","bengglas.nl","Beilen","Drenthe","NL","Glass Manufacturing / Construction",10000000,50,"Vacuum insulation glass manufacturer. FD Gazellen 2025 Top 5.","Private",2016,"No","Rankings"),
("Hive CPQ","hivecpq.com","Ghent","East Flanders","BE","CPQ Software / Manufacturing SaaS",5000000,30,"Configure-Price-Quote platform for manufacturers.","Private",2017,"No","Rankings"),
("ARMIN Robotics","armin-robot.com","","Flanders","BE","Industrial Automation / Robotics",5000000,20,"CNC automation expert: AGVs, cobots, vision systems, conveyor systems.","Private",2015,"No","Rankings"),
("NuReSys","nuresys.com","","Flanders","BE","Water Treatment / CleanTech",5000000,20,"Phosphorus and nitrogen recovery from wastewater.","Private",2011,"No","Rankings"),
("Diabatix","diabatix.com","Leuven","Flemish Brabant","BE","Thermal Design Software",5000000,20,"Generative thermal design software with AI for semiconductor clients.","Private",2016,"No","Rankings"),
("Robaws","robaws.com","","Flanders","BE","Construction ERP Software",5000000,30,"Cloud-based ERP for construction and field services.","Private",2015,"No","Rankings"),
("Horus Software","horussoftware.be","Liege","Liege","BE","Accounting Software / SaaS",5000000,30,"AI-powered accounting software. 8,000+ users.","Private",2016,"No","Rankings"),
])

# STREAM 6: Wholesale/Distribution + Associations (69 companies - selecting unique non-duplicates)
S6 = R([
("Technische Unie","technischeunie.nl","Amstelveen","Noord-Holland","NL","Technical Wholesale (Electrical/HVAC)",750000000,1500,"Largest technical wholesaler in NL. 280,000 articles from 700 suppliers.","Subsidiary (Sonepar)",1920,"No","Wholesale_Associations"),
("Kramp Groep","kramp.com","Varsseveld","Gelderland","NL","Agricultural Parts Wholesale",650000000,3500,"Europe's largest specialist in spare parts for agricultural industry.","PE-backed (NPM Capital)",1951,"No","Wholesale_Associations"),
("Rexel Nederland","rexel.nl","Amsterdam","Noord-Holland","NL","Electrical Wholesale/Distribution",400000000,800,"Partner for electrotechnical professionals. Part of Rexel Group.","Subsidiary (Rexel SA)",1967,"No","Wholesale_Associations"),
("Wasco","wasco.nl","Den Bosch","Noord-Brabant","NL","Technical Wholesale (HVAC/Sanitary)",350000000,700,"Technical wholesaler: heating, sanitary, ventilation. 35 branches.","Subsidiary (Rexel SA)",1970,"No","Wholesale_Associations"),
("Plieger Groep","plieger.nl","Zaltbommel","Gelderland","NL","Technical Wholesale (Sanitary/Heating)",150000000,750,"NL's largest in sanitary products. Installation, ventilation, electrical.","Subsidiary (GC Gruppe)",1948,"No","Wholesale_Associations"),
("Royal Van Leeuwen Pipe and Tube","vanleeuwen.com","Zwijndrecht","Zuid-Holland","NL","Steel Pipes & Fittings Distribution",1672000000,2400,"International distributor of steel pipes, valves and fittings. ~70 branches worldwide.","Family-owned",1924,"No","Wholesale_Associations"),
("MCB Group","mcb.eu","Valkenswaard","Noord-Brabant","NL","Steel & Metals Distribution",300000000,900,"Wholesale metals: steel, stainless, aluminium, non-ferrous. 80+ years.","Family-owned",1945,"No","Wholesale_Associations"),
("TVH Group","tvh.com","Waregem","Flanders","BE","Material Handling & Industrial Parts",2000000000,5500,"One of world's largest distributors of replacement parts for material handling.","Family-owned",1969,"No","Wholesale_Associations"),
("BMN Bouwmaterialen","bmn.nl","Nieuwegein","Utrecht","NL","Building Materials Wholesale",400000000,1620,"Market leader in building materials NL. 81 locations.","PE-backed (Blackstone)",1973,"No","Wholesale_Associations"),
("Royal Brinkman","royalbrinkman.com","'s-Gravenzande","Zuid-Holland","NL","Horticulture Supplies Wholesale",200000000,500,"Supplier and consultant for professional horticulture. 135+ years. 30,000+ products.","Family-owned",1885,"No","Wholesale_Associations"),
("IMCD","imcdgroup.com","Rotterdam","Zuid-Holland","NL","Specialty Chemicals Distribution",4443000000,5200,"Global leader in specialty chemicals and ingredients distribution. 60+ countries.","Public (Euronext)",1995,"No","Wholesale_Associations"),
("Azelis","azelis.com","Antwerp","Flanders","BE","Specialty Chemicals Distribution",4200000000,4300,"Global distributor of food ingredients and specialty chemicals. 63 countries.","Public (Euronext)",1996,"No","Wholesale_Associations"),
("Caldic","caldic.com","Rotterdam","Zuid-Holland","NL","Chemicals & Food Ingredients Distribution",900000000,4000,"Global distributor for food, nutrition, pharma and industrial markets. 44 countries.","PE-backed (Advent)",1970,"No","Wholesale_Associations"),
("Brenntag Nederland","brenntag.com","Dordrecht","Zuid-Holland","NL","Chemical Distribution",300000000,275,"Global market leader in chemical distribution. NL operations.","Subsidiary (Brenntag SE)",1874,"No","Wholesale_Associations"),
("Nedis","nedis.com","'s-Hertogenbosch","Noord-Brabant","NL","Consumer Electronics Wholesale",160000000,500,"Wholesale distribution of consumer electronics. 40+ year history.","Private (Commaxx)",1979,"No","Wholesale_Associations"),
("Cebeo","cebeo.be","Halle","Flanders","BE","Electrical Wholesale/Distribution",540000000,800,"Leader in Belgium in B2B distribution of electrical equipment. 55 branches.","Subsidiary (Sonepar)",0,"No","Wholesale_Associations"),
("itsme Group","itsme.eu","Brussels","Brussels","BE","Industrial Technical Distribution",95000000,550,"International independent group: innovative technology for industry and machine building.","Family-owned",0,"No","Wholesale_Associations"),
("Thermaflex","thermaflex.com","Waalwijk","Noord-Brabant","NL","Insulation & Pre-Insulated Piping",50000000,250,"Thermal insulation solutions for distribution of water, heat, cooling and air.","Private",1976,"No","Wholesale_Associations"),
("Royal Ingredients Group","royal-ingredients.com","Alkmaar","Noord-Holland","NL","Food Ingredients Distribution",50000000,77,"Global supplier: starches, proteins, fibers, sweeteners. 500+ customers in 50+ countries.","Private",2007,"No","Wholesale_Associations"),
("Rubix Benelux","rubix.com","","","NL","MRO Industrial Distribution",200000000,500,"Europe's largest MRO distributor. 50+ Benelux branches. 1.2M+ products.","PE-backed (CD&R)",0,"No","Wholesale_Associations"),
("B-CLOSE","b-close.be","Brussels","Brussels","BE","Forklift & Material Handling",50000000,200,"Largest independent Belgian distributor of A-brand forklifts.","Private",0,"No","Wholesale_Associations"),
("Beaulieu International Group","bintg.com","Waregem","Flanders","BE","Textiles & Flooring Solutions",2000000000,4900,"Global specialist in raw materials and flooring. 19 countries.","Family-owned",1959,"No","Wholesale_Associations"),
("Sioen Industries","sioen.com","Ardooie","Flanders","BE","Technical Textiles & Protective Clothing",187000000,1200,"Global leader in technical textiles and protective clothing. 40+ locations.","Public (Euronext)",1960,"No","Wholesale_Associations"),
("DAF Trucks","daf.com","Eindhoven","Noord-Brabant","NL","Truck Manufacturing",5000000000,6200,"Dutch truck manufacturer. Division of Paccar. Leading European truck brand.","Subsidiary (Paccar)",1928,"No","Wholesale_Associations"),
])


# ============================================================
# PROCESSING FUNCTIONS
# ============================================================

def normalize_name(name):
    """Normalize company name for dedup matching"""
    n = name.lower().strip()
    # Remove common suffixes
    for suffix in [' n.v.', ' nv', ' b.v.', ' bv', ' sa', ' s.a.', ' group', ' groep',
                   ' holding', ' holdings', ' international', ' europe', ' nederland',
                   ' netherlands', ' belgium', ' luxembourg', ' technologies']:
        n = n.replace(suffix, '')
    n = re.sub(r'[^a-z0-9]', '', n)
    return n

def assign_industry_tier(industry):
    """Assign tier1/tier2/avoid/unknown based on industry keywords"""
    ind_lower = industry.lower() if industry else ''
    for kw in AVOID_KEYWORDS:
        if kw in ind_lower:
            return 'avoid'
    for kw in TIER1_KEYWORDS:
        if kw in ind_lower:
            return 'tier1'
    for kw in TIER2_KEYWORDS:
        if kw in ind_lower:
            return 'tier2'
    return 'unknown'

def assign_client_tier(revenue, employees):
    """Assign client tier 1-5 based on Benelux ICP"""
    rev = revenue or 0
    emp = employees or 0
    # Tier 1: 2000+ employees, EUR 500M+ revenue
    if emp >= 2000 and rev >= 500000000:
        return 1
    # Tier 2: 1000-2000 employees, EUR 200M-500M revenue
    if emp >= 1000 and rev >= 200000000:
        return 2
    # Tier 3: 500-1000 employees, EUR 50M-200M (sweet spot)
    if emp >= 500 and rev >= 50000000:
        return 3
    # Tier 4: 200-500 employees, EUR 20M-50M
    if emp >= 200 and rev >= 20000000:
        return 4
    # Tier 5: 50-200 employees, EUR 10M-20M
    if emp >= 50 and rev >= 10000000:
        return 5
    # Below ICP minimum
    if emp >= 50 or rev >= 10000000:
        return 5
    return 0  # Does not meet minimum ICP

def assign_target_contact_role(employees):
    """Per Benelux ICP: <500 = CEO/MD, 500+ = Head of Sales / VP Sales"""
    emp = employees or 0
    if emp >= 500:
        return "Head of Sales / VP Sales"
    else:
        return "CEO / Managing Director"

def calculate_pipeline_priority(company):
    """Calculate 0-100 priority score"""
    score = 0
    ct = company.get('client_tier', 0)
    it = company.get('industry_tier', 'unknown')

    # Client tier scoring (tier 3 = sweet spot)
    tier_scores = {3: 30, 4: 25, 2: 20, 1: 15, 5: 10, 0: 0}
    score += tier_scores.get(ct, 0)

    # Industry tier scoring
    if it == 'tier1':
        score += 25
    elif it == 'tier2':
        score += 15

    # Data completeness bonus
    has_domain = bool(company.get('domain'))
    has_desc = bool(company.get('description'))
    has_revenue = bool(company.get('revenue_eur'))
    has_employees = bool(company.get('employees'))
    completeness = sum([has_domain, has_desc, has_revenue, has_employees]) / 4.0
    score += int(completeness * 15)

    # Multi-source bonus
    sources = company.get('source', '')
    source_count = len(sources.split('; ')) if sources else 1
    if source_count >= 3:
        score += 10
    elif source_count >= 2:
        score += 5

    # World market leader bonus
    wml = company.get('world_market_leader', '')
    if wml and wml != 'No':
        score += 15

    # Country bonus (NL = home market = priority)
    if company.get('country') == 'NL':
        score += 5

    return min(score, 100)

def calculate_data_completeness(company):
    """Calculate data completeness percentage"""
    fields = ['company_name', 'domain', 'city', 'country', 'industry',
              'revenue_eur', 'employees', 'description', 'ownership', 'founding_year']
    filled = sum(1 for f in fields if company.get(f))
    return round(filled / len(fields) * 100)

def deduplicate(companies):
    """Deduplicate by normalized name, merging source lists"""
    seen = {}  # normalized_name -> company dict
    domain_seen = {}  # domain -> normalized_name

    for c in companies:
        norm = normalize_name(c['company_name'])
        domain = (c.get('domain') or '').lower().strip()

        # Check domain-based dedup
        existing_norm = None
        if domain and domain in domain_seen:
            existing_norm = domain_seen[domain]
        elif norm in seen:
            existing_norm = norm

        if existing_norm and existing_norm in seen:
            # Merge: keep best data, merge sources
            existing = seen[existing_norm]
            existing_sources = set(existing.get('source', '').split('; '))
            new_sources = set(c.get('source', '').split('; '))
            existing['source'] = '; '.join(sorted(existing_sources | new_sources))

            # Fill in missing data from new record
            for key in c:
                if key == 'source':
                    continue
                if not existing.get(key) and c.get(key):
                    existing[key] = c[key]
                # Prefer more specific data
                if key == 'revenue_eur' and c.get(key) and existing.get(key):
                    # Keep the one that seems more precise (not rounded to billions)
                    if existing[key] % 1000000000 == 0 and c[key] % 1000000000 != 0:
                        existing[key] = c[key]
        else:
            seen[norm] = dict(c)
            if domain:
                domain_seen[domain] = norm

    return list(seen.values())


def main():
    print("Benelux Target List Consolidation")
    print("=" * 50)

    # Combine all streams
    all_companies = S1 + S2 + S3 + S4 + S5 + S6
    print(f"Total raw entries: {len(all_companies)}")

    # Deduplicate
    unique = deduplicate(all_companies)
    print(f"After deduplication: {len(unique)}")

    # Apply ICP scoring
    for c in unique:
        c['industry_tier'] = assign_industry_tier(c.get('industry', ''))
        c['client_tier'] = assign_client_tier(c.get('revenue_eur', 0), c.get('employees', 0))
        c['target_contact_role'] = assign_target_contact_role(c.get('employees', 0))
        c['pipeline_priority'] = calculate_pipeline_priority(c)
        c['data_completeness'] = calculate_data_completeness(c)
        c['source_count'] = len(c.get('source', '').split('; '))
        c['in_pipeline'] = False
        c['in_db'] = False

    # Filter: remove companies that don't meet minimum ICP
    icp_filtered = [c for c in unique if c['client_tier'] > 0 and c['industry_tier'] != 'avoid']
    print(f"After ICP filter (min 50 employees or EUR 10M, no avoid-industries): {len(icp_filtered)}")

    # Sort by pipeline priority
    icp_filtered.sort(key=lambda x: x['pipeline_priority'], reverse=True)

    # Ensure output directories exist
    for d in [MASTER_DIR, HUBSPOT_DIR, GAPS_DIR]:
        os.makedirs(d, exist_ok=True)

    # ---- Write Master List ----
    master_path = os.path.join(MASTER_DIR, "master_target_list_benelux.csv")
    master_fields = [
        'company_name', 'domain', 'city', 'region', 'country', 'industry',
        'industry_tier', 'revenue_eur', 'employees', 'description', 'ownership',
        'founding_year', 'world_market_leader', 'client_tier',
        'target_contact_role', 'pipeline_priority', 'data_completeness',
        'source', 'source_count', 'in_pipeline', 'in_db'
    ]
    with open(master_path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=master_fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(icp_filtered)
    print(f"Written: {master_path} ({len(icp_filtered)} rows)")

    # ---- Write HubSpot Companies Import ----
    hs_companies_path = os.path.join(HUBSPOT_DIR, "hubspot_companies_import_benelux.csv")
    with open(hs_companies_path, 'w', newline='', encoding='utf-8-sig') as f:
        hs_fields = [
            'Name', 'Company Domain Name', 'City', 'State/Region', 'Country/Region',
            'Industry', 'Description', 'Annual Revenue', 'Number of Employees',
            'Client Tier', 'Industry Tier', 'Ownership Type', 'Founding Year',
            'World Market Leader', 'Pipeline Priority Score', 'In Pipeline',
            'Already in DB', 'Data Completeness %', 'Source Lists', 'Source Count',
            'Target Contact Role'
        ]
        w = csv.DictWriter(f, fieldnames=hs_fields)
        w.writeheader()
        for c in icp_filtered:
            country_map = {'NL': 'Netherlands', 'BE': 'Belgium', 'LU': 'Luxembourg'}
            w.writerow({
                'Name': c['company_name'],
                'Company Domain Name': c.get('domain', ''),
                'City': c.get('city', ''),
                'State/Region': c.get('region', ''),
                'Country/Region': country_map.get(c.get('country', ''), c.get('country', '')),
                'Industry': c.get('industry', ''),
                'Description': c.get('description', ''),
                'Annual Revenue': c.get('revenue_eur', ''),
                'Number of Employees': c.get('employees', ''),
                'Client Tier': c.get('client_tier', ''),
                'Industry Tier': c.get('industry_tier', ''),
                'Ownership Type': c.get('ownership', ''),
                'Founding Year': c.get('founding_year', ''),
                'World Market Leader': c.get('world_market_leader', ''),
                'Pipeline Priority Score': c.get('pipeline_priority', ''),
                'In Pipeline': c.get('in_pipeline', False),
                'Already in DB': c.get('in_db', False),
                'Data Completeness %': c.get('data_completeness', ''),
                'Source Lists': c.get('source', ''),
                'Source Count': c.get('source_count', ''),
                'Target Contact Role': c.get('target_contact_role', ''),
            })
    print(f"Written: {hs_companies_path} ({len(icp_filtered)} rows)")

    # ---- Write HubSpot Contacts Import (placeholder - no actual contacts yet) ----
    hs_contacts_path = os.path.join(HUBSPOT_DIR, "hubspot_contacts_import_benelux.csv")
    with open(hs_contacts_path, 'w', newline='', encoding='utf-8-sig') as f:
        contact_fields = ['First Name', 'Last Name', 'Email', 'Job Title',
                          'LinkedIn URL', 'Associated Company Domain', 'Associated Company Name']
        w = csv.DictWriter(f, fieldnames=contact_fields)
        w.writeheader()
        # Contacts will need to be enriched separately
        for c in icp_filtered:
            w.writerow({
                'First Name': '',
                'Last Name': '',
                'Email': '',
                'Job Title': c.get('target_contact_role', ''),
                'LinkedIn URL': '',
                'Associated Company Domain': c.get('domain', ''),
                'Associated Company Name': c['company_name'],
            })
    print(f"Written: {hs_contacts_path} ({len(icp_filtered)} rows - contacts need enrichment)")

    # ---- Write Gaps Report ----
    gaps_path = os.path.join(GAPS_DIR, "hubspot_gaps_report_benelux.csv")
    gaps = []
    for c in icp_filtered:
        if not c.get('domain'):
            gaps.append({'Company': c['company_name'], 'City': c.get('city',''), 'Country': c.get('country',''),
                         'Client Tier': c.get('client_tier',''), 'Gap Type': 'MISSING_DOMAIN',
                         'Action Required': 'Find company website/domain', 'Priority': 'HIGH' if c.get('client_tier',5) <= 3 else 'MEDIUM'})
        # All companies need contact enrichment
        gaps.append({'Company': c['company_name'], 'City': c.get('city',''), 'Country': c.get('country',''),
                     'Client Tier': c.get('client_tier',''), 'Gap Type': 'MISSING_CONTACT',
                     'Action Required': f"Find {c.get('target_contact_role', 'key decision maker')}",
                     'Priority': 'HIGH' if c.get('client_tier',5) <= 3 else 'MEDIUM'})

    with open(gaps_path, 'w', newline='', encoding='utf-8-sig') as f:
        gap_fields = ['Company', 'City', 'Country', 'Client Tier', 'Gap Type', 'Action Required', 'Priority']
        w = csv.DictWriter(f, fieldnames=gap_fields)
        w.writeheader()
        w.writerows(gaps)
    print(f"Written: {gaps_path} ({len(gaps)} gaps)")

    # ---- Summary Stats ----
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    countries = defaultdict(int)
    tiers = defaultdict(int)
    ind_tiers = defaultdict(int)
    for c in icp_filtered:
        countries[c.get('country', 'Unknown')] += 1
        tiers[c.get('client_tier', 0)] += 1
        ind_tiers[c.get('industry_tier', 'unknown')] += 1

    print(f"\nBy Country:")
    for k, v in sorted(countries.items()):
        print(f"  {k}: {v}")
    print(f"\nBy Client Tier:")
    for k, v in sorted(tiers.items()):
        print(f"  Tier {k}: {v}")
    print(f"\nBy Industry Tier:")
    for k, v in sorted(ind_tiers.items()):
        print(f"  {k}: {v}")
    print(f"\nAvg Pipeline Priority: {sum(c['pipeline_priority'] for c in icp_filtered) / len(icp_filtered):.1f}")
    print(f"Companies with World Market Leader status: {sum(1 for c in icp_filtered if c.get('world_market_leader','No') != 'No')}")


if __name__ == '__main__':
    main()
