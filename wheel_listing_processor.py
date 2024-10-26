import csv
import os

def format_price(price):
    """Format price string to numeric value"""
    if not price:
        return "Preis auf Anfrage"
    return price.replace('€', '').strip()

def format_profile_depth(depth):
    """Format profile depth consistently"""
    if not depth:
        return "k.A."
    # Remove 'mm' and standardize format
    depth = str(depth).replace('mm', '').strip()
    if ',' in depth:
        parts = depth.split(',')
        if len(parts) > 1:
            return f"{parts[0].strip()},{parts[1].strip()} mm"
    return f"{depth} mm"

def safe_value(value, default="k.A."):
    """Handle missing or empty values"""
    if not value or value.strip() == '':
        return default
    return str(value).strip()

def create_description(row):
    """Create a detailed description for a wheel/tire set"""
    # Convert row dictionary keys to match CSV headers
    price = format_price(safe_value(row.get('BuyItNowPrice', '')))
    
    template = f"""Hallo und herzlich willkommen bei einem Angebot von R&S Ihr Autohaus.
Kommen Sie gerne vorbei und holen den Artikel direkt bei uns im Lager ab.

Artikelbeschreibung:
Zustand: Gebraucht
Anzahl: {safe_value(row.get('Anzahl'))} Kompletträder

Felgen:
Material: {safe_value(row.get('Felgenmaterial'))}
Hersteller: {safe_value(row.get('Felgenhersteller'))}
Teilenummer: {safe_value(row.get('Herstellernummer_Felge'))}
Felgenmaße: {safe_value(row.get('Felgenbreite'))}J x {safe_value(row.get('Zoll'))} ET{safe_value(row.get('Einpresstiefe'))}
Lochkreis: {safe_value(row.get('Lochzahl'))}x {safe_value(row.get('Lochkreis'))}
Farbe: {safe_value(row.get('Felgenfarbe'))}

Reifen:
Jahreszeit: {safe_value(row.get('Reifenspezifikation'))}
Hersteller: {safe_value(row.get('Reifenhersteller'))}
Modell: {safe_value(row.get('Reifenmodell'))}
Reifengröße: {safe_value(row.get('Reifenbreite'))}/{safe_value(row.get('Reifenquerschnitt'))} R{safe_value(row.get('Zoll'))} {safe_value(row.get('Tragfaehigkeitsindex'))}{safe_value(row.get('Geschwindigkeitsindex'))}
Profiltiefe: {format_profile_depth(row.get('Profiltiefe'))}
DOT: {safe_value(row.get('DOT'))}
Schneeflocken-Symbol: {safe_value(row.get('C:Schneeflocken-Symbol'), 'Nein')}

Fahrzeugtyp: {safe_value(row.get('Fahrzeugtyp'))}
Preis: {price}€ 
Versand: 50€


(INTERN: {safe_value(row.get('VAT'))})\n"""
    
    return template

def process_csv(filename):
    """Process the CSV file and generate descriptions"""
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists('output'):
            os.makedirs('output')
        
        descriptions = []
        
        # Read CSV file using csv module
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            # Process each row
            for index, row in enumerate(csv_reader, 1):
                try:
                    # Create description
                    description = create_description(row)
                    descriptions.append(description)
                    
                    # Generate unique filename based on characteristics
                    safe_manufacturer = safe_value(row.get('Felgenhersteller', '')).replace(' ', '_')
                    filename = f"output/rad_{safe_value(row.get('Reifenbreite', ''))}_{safe_value(row.get('Zoll', ''))}_{safe_manufacturer}_{index}.txt"
                    filename = filename.replace(' ', '_').replace('/', '_').lower()
                    
                    # Write to file
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(description)
                        
                except Exception as e:
                    print(f"Error processing row {index}: {str(e)}")
                    
        return descriptions
    
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return []

def main():
    """Main function to run the program"""
    import sys
    
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = 'ebay_vorlage_kompletträder.csv'
    
    print(f"Processing file: {csv_file}")
    descriptions = process_csv(csv_file)
    print(f"\nGenerated {len(descriptions)} descriptions in the 'output' directory")

if __name__ == "__main__":
    main()