"""Populate the ontology based on data from the datasets."""
import csv
from rdflib import Graph, Namespace, Literal, URIRef, RDF, OWL, RDFS

g = Graph()
g.parse("med_doencas.ttl")
n = Namespace("http://www.example.org/disease-ontology#")

disease_treatment_map = {}
treatments_set = set()

def parse_treatments():
    """Extract and populate the info on diseases and their symptoms."""
    with open('Disease_Treatment.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # Ignore header

        for row in reader:
            disease = row[0].strip().replace(" ", "_").replace("(","").replace(")","")
            treatments = [s.strip().replace(" ", "_") for s in row[1:] if s.strip()]

            if disease not in disease_treatment_map:
                disease_treatment_map[disease] = set()
            disease_treatment_map[disease].update(treatments)
            treatments_set.update(treatments)

    for t in treatments_set:
        uri_t = URIRef(n[t])
        g.add((uri_t,RDF.type,n.Treatment))

    for d,treatments in disease_treatment_map.items():
        uri_d = URIRef(n[d])
        for t in treatments:
            uri_t = URIRef(n[t])
            g.add((uri_d,n.hasTreatment,uri_t))

def print_graph():
    """Print new ontology to the stdout."""
    print(g.serialize(format='turtle'))


def main():
    """Function responsible to delegate functions."""
    parse_treatments()
    print_graph()

if __name__ == "__main__":
    main()
