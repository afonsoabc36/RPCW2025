import sys
import json

def parseJson(inputFile:str) -> dict:
    with open(inputFile, "r") as f:
        data = json.load(f)
    exams = {}
    athletes = {}
    athlete_id = 0
    clubs = {}
    clubSet = set()
    club_id = 0
    sports = {}
    sportSet = set()
    sport_id = 0
    for exam in data:
        club_name = exam["clube"] 
        club_id = club_name.replace(" ", "_")
        if club_id not in clubs:
            clubSet.add(exam["clube"])
            clubs[club_id] = {
                "name": club_name,
                "sports": []
            }
        if exam["modalidade"] not in clubs[club_id]["sports"]:
            clubs[club_id]["sports"].append(exam["modalidade"])
        current_sport_id = 0
        if exam["modalidade"] not in sports:
            sportSet.add(exam["modalidade"])
            sports[exam["modalidade"]] = {
                "id": sport_id,
            }
            current_sport_id = sport_id
            sport_id += 1
        else:
            current_sport_id = sports[exam["modalidade"]]["id"]

        athlete = {
            "firstName" : exam["nome"]["primeiro"],
            "lastName" : exam["nome"]["último"],
            "age": exam["idade"],
            "gender": exam["género"],
            "address": exam["morada"],
            "sport": current_sport_id,
            "club": club_id,
            "email": exam["email"],
            "federated": exam["federado"]
        }
        athletes[athlete_id] = athlete
        examData = {
            "date": exam["dataEMD"],
            "result": exam["resultado"],
            "athlete": athlete_id
        }
        exams[exam["_id"]] = examData
        athlete_id += 1

    result = {
        'exams': exams,
        'athletes': athletes,
        'clubs': clubs,
        'sports': sports,
    }

    return result


def writeFile(data:dict, outputFile:str) -> None:
    ttl = """@prefix : <http://rpcw.di.uminho.pt/2025/emd/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2025/emd/> .

<http://rpcw.di.uminho.pt/2025/emd> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2025/emd/praticadaPor
:praticadaPor rdf:type owl:ObjectProperty ;
              rdfs:domain :Modalidade ;
              owl:inverseOf :pratica .


###  http://rpcw.di.uminho.pt/2025/emd/pratica
:pratica rdf:type owl:ObjectProperty ;
         rdfs:domain :Pessoa .


###  http://rpcw.di.uminho.pt/2025/emd/referenteA
:referenteA rdf:type owl:ObjectProperty ;
            rdfs:domain :Exame ;
            owl:inverseOf :realiza .


###  http://rpcw.di.uminho.pt/2025/emd/realiza
:realiza rdf:type owl:ObjectProperty ;
         rdfs:domain :Pessoa .


###  http://rpcw.di.uminho.pt/2025/emd/representa
:representa rdf:type owl:ObjectProperty ;
            rdfs:domain :Pessoa .


###  http://rpcw.di.uminho.pt/2025/emd/representadoPor
:representadoPor rdf:type owl:ObjectProperty ;
                 rdfs:domain :Clube ;
                 owl:inverseOf :representa .

 
###  http://rpcw.di.uminho.pt/2025/emd/dispoeDe
:dispoeDe rdf:type owl:ObjectProperty ;
          rdfs:domain :Clube .


###  http://rpcw.di.uminho.pt/2025/emd/disponibilizadaPor
:disponibilizadaPor    rdf:type owl:ObjectProperty ;
                       rdfs:domain :Modalidade ;
                       owl:inverseOf :dispoeDe .   


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2025/emd/eFederado
:eFederado rdf:type owl:DatatypeProperty ;
           rdfs:domain :Pessoa ;
           rdfs:range xsd:boolean .


###  http://rpcw.di.uminho.pt/2025/emd/temData
:temData rdf:type owl:DatatypeProperty ;
         rdfs:domain :Exame ;
         rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2025/emd/temEmail
:temEmail rdf:type owl:DatatypeProperty ;
          rdfs:domain :Pessoa ;
          rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2025/emd/temGenero
:temGenero rdf:type owl:DatatypeProperty ;
           rdfs:domain :Pessoa ;
           rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2025/emd/temIdade
:temIdade rdf:type owl:DatatypeProperty ;
          rdfs:domain :Pessoa ;
          rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2025/emd/temMorada
:temMorada rdf:type owl:DatatypeProperty ;
           rdfs:domain :Pessoa ;
           rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2025/emd/temNome
:temNome rdf:type owl:DatatypeProperty ;
         rdfs:domain [ rdf:type owl:Class ;
                       owl:unionOf ( :Clube
                                     :Modalidade
                                   )
                     ] ;
         rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2025/emd/temPrimeiroNome
:temPrimeiroNome rdf:type owl:DatatypeProperty ;
                 rdfs:domain :Pessoa ;
                 rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2025/emd/temUltimoNome
:temUltimoNome rdf:type owl:DatatypeProperty ;
               rdfs:domain :Pessoa ;
               rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2025/emd/temResultado
:temResultado rdf:type owl:DatatypeProperty ;
              rdfs:domain :Exame ;
              rdfs:range xsd:boolean .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2025/emd/Clube
:Clube rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2025/emd/Exame
:Exame rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2025/emd/Modalidade
:Modalidade rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2025/emd/Pessoa
:Pessoa rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################

"""

    for idAtleta, athlete in data["athletes"].items():
        idModalidade = athlete["sport"]
        idClube = athlete["club"]
        federated = str(athlete["federated"])
        email = athlete["email"]
        gender = athlete["gender"]
        age = int(athlete["age"])
        address = athlete["address"]
        firstName = athlete["firstName"]
        lastName = athlete["lastName"]

        indent = " " * (8+len(str(idAtleta)))
        athleteIndent = " " * (17+len(str(idAtleta)))
        ttl += f"""### http://rpcw.di.uminho.pt/2025/emd#Atleta{idAtleta}
:Atleta{idAtleta} rdf:type owl:NamedIndividual , 
{athleteIndent}:Pessoa ;
{indent}:pratica :Modalidade{idModalidade} ;
{indent}:representa :Clube{idClube} ;
{indent}:eFederado "{federated}"^^xsd:boolean ;
{indent}:temEmail "{email}" ;
{indent}:temGenero "{gender}" ;
{indent}:temIdade {age} ;
{indent}:temMorada "{address}" ;
{indent}:temPrimeiroNome "{firstName}" ;
{indent}:temUltimoNome "{lastName}" .


"""

    for idClube, club in data["clubs"].items():
        indent = " " * (7+len(idClube))
        clubIndent = " " * (16+len(idClube))
        clubName = club["name"]
        ttl += f"""### http://rpcw.di.uminho.pt/2025/emd#Clube{idClube}
:Clube{idClube} rdf:type owl:NamedIndividual ,
{clubIndent}:Clube ;
"""
        for sport in club["sports"]:
            ttl += f"""{indent}:dispoeDe :Modalidade{sport} ;
"""
        ttl += f"""{indent}:temNome "{clubName}" .


"""
    for idExame, exam in data["exams"].items():
        indent = " " * (7+len(idExame))
        examIndent = " " * (16+len(idExame))
        idAtleta = exam["athlete"]
        date = exam["date"]
        result = exam["result"]
        ttl += f"""### http://rpcw.di.uminho.pt/2025/emd#Exame{idExame}
:Exame{idExame} rdf:type owl:NamedIndividual ,
{examIndent}:Exame ;
{indent}:referenteA :Atleta{idAtleta} ;
{indent}:temData "{date}" ;
{indent}:temResultado "{result}"^^xsd:boolean .


"""

    for idModalidade, sport in data["sports"].items():
        indent = " " * (12+len(idModalidade))
        sportIndent = " " * (21+len(idModalidade))
        sportName = idModalidade
        ttl += f"""### http://rpcw.di.uminho.pt/2025/emd#Modalidade{idModalidade}
:Modalidade{idModalidade} rdf:type owl:NamedIndividual ,
{sportIndent}:Modalidade ;
{indent}:temNome "{sportName}" .


"""
        

    with open(outputFile, "w") as f:
        f.write(ttl)

if __name__ == "__main__":
    outputFile = "../outputs/emd_generated.ttl"
    inputFile = "../datasets/emd.json"
    if len(sys.argv) > 1:
        outputFile = sys.argv[1]
    if len(sys.argv) > 2:
        inputFile = sys.argv[2]

    data = parseJson(inputFile)
    writeFile(data, outputFile)
