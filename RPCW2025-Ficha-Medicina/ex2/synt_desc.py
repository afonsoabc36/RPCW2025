"""Populate the ontology based on data from the datasets."""
import csv
from rdflib import Graph, Namespace, Literal, URIRef, RDF, OWL, RDFS

g = Graph()
g.parse("medical.ttl")
n = Namespace("http://www.example.org/disease-ontology#")

disease_symptom_map = {}
symptom_set = set()

def parse_syntoms():
    """Extract and populate the info on diseases and their symptoms."""
    with open('Disease_Syntoms.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # Ignore header

        for row in reader:
            disease = row[0].strip().replace(" ", "_").replace("(","").replace(")","")
            symptoms = [s.strip().replace(" ", "_") for s in row[1:] if s.strip()]

            if disease not in disease_symptom_map:
                disease_symptom_map[disease] = set()
            disease_symptom_map[disease].update(symptoms)
            symptom_set.update(symptoms)

    for s in symptom_set:
        uri_s = URIRef(n[s])
        g.add((uri_s,RDF.type,n.Symptom))
        g.add((uri_s,RDF.type,OWL.NamedIndividual))

    for d,symptoms in disease_symptom_map.items():
        uri_d = URIRef(n[d])
        g.add((uri_d,RDF.type,n.Disease))
        for s in symptoms:
            uri_s = URIRef(n[s])
            g.add((uri_d,n.hasSymptom,uri_s))

def parse_descriptions():
    """Extract and populate the info on disease description."""
    g.add((URIRef(n["hasDescription"]),RDF.type,OWL.DatatypeProperty))
    g.add((URIRef(n["hasDescription"]),RDFS.domain,n.Disease))
    with open('Disease_Description.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # Ignore header

        for row in reader:
            disease = row[0].strip().replace(" ", "_")
            disease_uri = URIRef(n[disease])
            description = row[1].strip().replace('"', '\\"')
            g.add((disease_uri,n.hasDescription,Literal(description)))

def print_graph():
    """Print new ontology to the stdout."""
    print(g.serialize(format='turtle'))


def main():
    """Function responsible to delegate functions."""
    parse_syntoms()
    parse_descriptions()
    print_graph()

if __name__ == "__main__":
    main()
