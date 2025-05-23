"""Populate the ontology based on data from the datasets."""
import json
from rdflib import Graph, Namespace, Literal, URIRef, RDF, OWL, RDFS

g = Graph()
g.parse("med_tratamentos.ttl")
n = Namespace("http://www.example.org/disease-ontology#")

def parse_pacients():
    """Extract and populate the info on diseases and their symptoms."""
    with open('doentes.json', encoding='utf-8') as f:
        pacients = json.load(f)
    for i,p in enumerate(pacients):
        name = p["nome"]
        id_ = f"p_{i}"
        uri_p = URIRef(n[id_])
        syntoms = p["sintomas"]
        g.add((uri_p,RDF.type,n.Patient))
        g.add((uri_p,RDF.type,OWL.NamedIndividual))
        g.add((uri_p,n.name,Literal(name)))
        for s in syntoms:
            s = s.strip().replace(" ","_")
            uri_s = URIRef(n[s])
            g.add((uri_p,n.exhibitsSymptom,uri_s))


def print_graph():
    """Print new ontology to the stdout."""
    print(g.serialize(format='turtle'))


def main():
    """Function responsible to delegate functions."""
    parse_pacients()
    print_graph()

if __name__ == "__main__":
    main()
