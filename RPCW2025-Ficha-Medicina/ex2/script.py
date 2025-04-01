import csv
from collections import defaultdict

def parse__syntoms_csv(file_path):
    data = defaultdict(set)
    
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # headers = next(reader)  # Read the header row
        next(reader)  # Ignore the header row
        
        for row in reader:
            disease = row[0]
            # TODO: Add a symptoms set to add all the symptoms to the ontology
            symptoms = [symptom.strip() for symptom in row[1:] if symptom.strip()]
            data[disease].update(symptoms)
    
    return data

# Example usage
if __name__ == "__main__":
    file_path = "Disease_Syntoms.csv"
    diseaseAndSyntoms = parse__syntoms_csv(file_path)

    for disease, symptoms in diseaseAndSyntoms.items():
        print(f"Disease: {disease}")
        print(f"Symptoms: {(symptoms)}")
    
