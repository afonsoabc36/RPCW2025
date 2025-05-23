from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS, OWL, XSD

g = Graph()
g.parse("med_doentes.ttl")
n = Namespace("http://www.example.org/disease-ontology#")

def patient_disease_diagnostic():
    """Function to parse the data and insert the triples."""
    query="""
    PREFIX: <http://www.example.org/disease-ontology#>
    CONSTRUCT {
      ?patient :hasDisease ?disease .
    }
    WHERE {
      ?disease a :Disease ;
               :hasSymptom ?symptom .

      ?patient a :Patient ;
               :exhibitsSymptom ?symptom .

      FILTER NOT EXISTS {
        ?disease :hasSymptom ?requiredSymptom .
        FILTER NOT EXISTS {
          ?patient :exhibitsSymptom ?requiredSymptom .
        }
      }

      FILTER NOT EXISTS {
        ?patient :exhibitsSymptom ?symptomExtra .
        FILTER NOT EXISTS {
          ?disease :hasSymptom ?symptomExtra .
        }
      }
    }
    """
    for r in g.query(query):
        g.add(r)

def print_graph():
    """Print new ontology to the stdout."""
    print(g.serialize(format='turtle'))

def main():
    """Function responsible to delegate functions."""
    patient_disease_diagnostic()
    print_graph()


if __name__ == "__main__":
    main()
