import json
import re
from bs4 import BeautifulSoup
import os

def extract_driver_names_from_html(html_file_path):
    """Extract driver names from the Wikipedia HTML file of Formula One fatalities."""
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the table with the fatalities
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    drivers_with_fatal_accidents = []
    
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            # Skip header rows
            if row.find('th') and 'scope' in row.find('th').attrs and row.find('th')['scope'] == 'row':
                # Extract driver name from the row
                driver_cell = row.find('th')
                if driver_cell:
                    # Find the driver name link
                    driver_link = driver_cell.find('a')
                    if driver_link:
                        driver_name = driver_link.text.strip()
                        drivers_with_fatal_accidents.append(driver_name)
    
    return drivers_with_fatal_accidents

def update_drivers_json(json_file_path, drivers_with_fatal_accidents):
    """Update the drivers.json file with the 'fatal accident' statistic."""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        drivers_data = json.load(file)
    
    # Count how many drivers were updated
    updated_count = 0
    
    # Create a list of normalized driver names for better matching
    normalized_fatal_drivers = [normalize_name(name) for name in drivers_with_fatal_accidents]
    
    for driver in drivers_data:
        driver_name = driver["Name"]
        normalized_name = normalize_name(driver_name)
        
        # Check if this driver is in the fatal accidents list
        if any(normalized_name in fatal_name or fatal_name in normalized_name for fatal_name in normalized_fatal_drivers):
            driver["fatal accident"] = "Yes"
            updated_count += 1
        else:
            driver["fatal accident"] = "No"
    
    # Save the updated JSON
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(drivers_data, file, indent=4, ensure_ascii=False)
    
    return updated_count

def normalize_name(name):
    """Normalize a name for better matching."""
    # Remove special characters, convert to lowercase
    normalized = re.sub(r'[^\w\s]', '', name).lower()
    # Handle special cases like "de", "von", etc.
    normalized = re.sub(r'\s+de\s+', ' ', normalized)
    normalized = re.sub(r'\s+von\s+', ' ', normalized)
    return normalized

def main():
    # Paths
    html_file_path = r"C:\Users\GCO\Desktop\List of Formula One fatalities - Wikipedia.html"
    json_file_path = r"C:\Users\GCO\CascadeProjects\F1Project\data\drivers.json"
    
    # Create a backup of the original JSON file
    backup_path = json_file_path + ".bak"
    if not os.path.exists(backup_path):
        with open(json_file_path, 'r', encoding='utf-8') as src:
            with open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        print(f"Created backup at {backup_path}")
    
    # Extract driver names from the HTML file
    print("Extracting driver names from the Wikipedia HTML file...")
    drivers_with_fatal_accidents = extract_driver_names_from_html(html_file_path)
    print(f"Found {len(drivers_with_fatal_accidents)} drivers with fatal accidents.")
    
    # Print the first few drivers for verification
    print("Sample of drivers with fatal accidents:")
    for driver in drivers_with_fatal_accidents[:5]:
        print(f"  - {driver}")
    
    # Update the drivers.json file
    print("\nUpdating drivers.json with the 'fatal accident' statistic...")
    updated_count = update_drivers_json(json_file_path, drivers_with_fatal_accidents)
    
    print(f"Updated {updated_count} drivers with 'fatal accident' = 'Yes'")
    print(f"Added 'fatal accident' = 'No' to all other drivers")
    print(f"Updated JSON file saved to {json_file_path}")

if __name__ == "__main__":
    main()
