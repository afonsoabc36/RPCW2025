## Ex1

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://www.semanticweb.org/afonsoabc36/ontologies/2025/untitled-ontology-13/>
```

1. Quantas classes estão definidas na Ontologia?

```sparql
SELECT (COUNT(DISTINCT ?c) as ?nc)
WHERE {
    ?c rdf:type owl:Class.
    FILTER(STRSTARTS(STR(?c), STR(:)))
}
```

> [!NOTE]
> Filter necessário devido a classes \_:nodeX no GraphDB

2. Quantas Object Properties estão definidas na Ontologia?

```sparql
SELECT (COUNT (DISTINCT ?o) as ?on)
WHERE {
    ?o a owl:ObjectProperty.
}
```

3. Quantos indivíduos existem na tua ontologia?

```sparql
SELECT (COUNT (DISTINCT ?i) as ?in)
WHERE {
    ?i a owl:NamedIndividual.
}
```

4. Quem planta tomates?

```sparql
SELECT DISTINCT ?s
WHERE {
    ?s a :Pessoa;
       :cultiva ?f.
    ?f a :Tomate.
}
```

5. Quem contrata trabalhadores temporários?

```sparql
SELECT DISTINCT ?s
WHERE {
    ?t a :TrabalhadorTemp;
       :trabalhaEm ?fazenda.
    ?s :possui ?fazenda.
}
```

## Ex2

11 . Uma vez criada a ontologia (última versão: med_doentes.ttl), especifica queries SPARQL que permitam responder às seguintes questões:

- Quantas doenças estão presentes na ontologia?

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://www.example.org/disease-ontology#>

SELECT (COUNT(DISTINCT ?doenca) AS ?n)
WHERE {
    ?doenca rdf:type :Disease .
}
```

- Que doenças estão associadas ao sintoma "yellowish_skin"?

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://www.example.org/disease-ontology#>

SELECT DISTINCT ?doenca
WHERE {
    ?doenca rdf:type :Disease ;
            :hasSymptom :yellowish_skin .
}
```

- Que doenças estão associadas ao tratamento "exercise"?

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://www.example.org/disease-ontology#>

SELECT DISTINCT ?doenca
WHERE {
    ?doenca rdf:type :Disease ;
            :hasTreatment :exercise .
}
```

- Produz uma lista ordenada alfabeticamente com o nome dos doentes.

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://www.example.org/disease-ontology#>

SELECT ?name
WHERE {
    ?patient rdf:type :Patient ;
            :name ?name .
}
ORDER BY ?name
```

12. Cria uma query CONSTRUCT que diagnostique a doença de cada pessoa, ou seja, produza uma lista
    de triplos com a forma :patientX :hasDisease :diseaseY. No fim, acrescenta estes triplos à
    ontologia;

```sparql
PREFIX : <http://www.example.org/disease-ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT {
  ?patient :hasDisease ?disease .
}
WHERE {
  ?disease a :Disease ;
           :hasSymptom ?symptom .

  ?patient a :Patient ;
           :exhibitsSymptom ?symptom .

  # O paciente tem todos os sintomas da doença
  FILTER NOT EXISTS {
    ?disease :hasSymptom ?requiredSymptom .
    FILTER NOT EXISTS {
      ?patient :exhibitsSymptom ?requiredSymptom .
    }
  }
}
```

-- ou --

```sparql
PREFIX : <http://www.example.org/disease-ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT {
  ?patient :hasDisease ?disease .
}
WHERE {
  ?disease a :Disease ;
           :hasSymptom ?symptom .

  ?patient a :Patient ;
           :exhibitsSymptom ?symptom .

  # O paciente tem todos os sintomas da doença
  FILTER NOT EXISTS {
    ?disease :hasSymptom ?requiredSymptom .
    FILTER NOT EXISTS {
      ?patient :exhibitsSymptom ?requiredSymptom .
    }
  }

  # E o paciente não tem sintomas extra que não estão na doença
  FILTER NOT EXISTS {
    ?patient :exhibitsSymptom ?symptomExtra .
    FILTER NOT EXISTS {
      ?disease :hasSymptom ?symptomExtra .
    }
  }
}
```

> [!NOTE]
> Script para a inserção disponível em `ex2/construct.py`.
> Se for diretamente no GraphDB, trocar a _keyword_ CONSTRUCT por INSERT

13. Cria um query SPARQL que poduza uma distribuição dos doentes pelas doenças, ou seja, dá como resultado uma lista de pares (doença, nº de doentes);

```sparql
SELECT ?d (COUNT(?p) AS ?np)
WHERE {
    ?d a :Disease.
    ?p a :Patient.
    ?p :hasDisease ?d.
}
GROUP BY ?d
```

14. Cria um query SPARQL que poduza uma distribuição das doenças pelos sintomas, ou seja, dá como resultado uma lista de pares (sintoma, nº de doenças com o sintoma);

```sparql
SELECT ?s (COUNT(?d) AS ?nd)
WHERE {
    ?s a :Symptom.
    ?d a :Disease.
    ?d :hasSymptom ?s.
}
GROUP BY ?s
```

15. Cria um query SPARQL que poduza uma distribuição das doenças pelos tratamentos, ou seja, dá como resultado uma lista de pares (tratamento, nº de doenças com o tratamento).

```sparql
SELECT ?t (COUNT(?d) AS ?nd)
WHERE {
    ?t a :Treatment.
    ?d a :Disease.
    ?d :hasTreatment ?t.
}
GROUP BY ?t
```
