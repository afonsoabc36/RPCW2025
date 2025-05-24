import json
from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS, OWL, XSD

g = Graph()
g.parse("sapientia_base.ttl")

n = Namespace("http://www.semanticweb.org/afonsoabc36/ontologies/2025/rpcw2025normal#")

triplos_para_adicionar = []

# Set das entidades identificadas pelos seus nomes
conceitos_mencionados = set()
disciplinas_mencionados = set()
mestres_mencionados = set()
obras_mencionados = set()
aprendizes_mencionados = set()
tipos_conhecimento_mencionados = set()
periodos_historicos_mencionados = set()
aplicacoes_mencionados = set()

def safe_uri(s):
    """Transform a string into a URI replacing invalid characters."""
    return URIRef(n[s.strip().replace(" ", "_").replace(".", "_").replace("-", "_")])

def add_triplo(subject, predicate, obj):
    """Adiciona um triplo à lista para processamento posterior."""
    triplos_para_adicionar.append((subject, predicate, obj))

def parse_conceitos():
    """Parse conceitos.json e coleta os dados e triplos."""
    try:
        with open('datasets/conceitos.json', encoding='utf-8') as f:
            data = json.load(f)
        for conceito_data in data['conceitos']:
            nome = conceito_data['nome']
            conceitos_mencionados.add(nome)
            # Período histórico
            if 'períodoHistórico' in conceito_data:
                periodo = conceito_data['períodoHistórico']
                periodos_historicos_mencionados.add(periodo)
                add_triplo(safe_uri(nome), n.surgeEm, safe_uri(periodo))
            # Aplicações
            if 'aplicações' in conceito_data:
                for aplicacao in conceito_data['aplicações']:
                    aplicacoes_mencionados.add(aplicacao)
                    add_triplo(safe_uri(nome), n.temAplicaçãoEm, safe_uri(aplicacao))
            # Conceitos relacionados
            if 'conceitosRelacionados' in conceito_data:
                for conceito_rel in conceito_data['conceitosRelacionados']:
                    conceitos_mencionados.add(conceito_rel)
                    add_triplo(safe_uri(nome), n.estáRelacionadoCom, safe_uri(conceito_rel))
    except FileNotFoundError:
        print("Arquivo conceitos.json não encontrado")

def parse_disciplinas():
    """Parse disciplinas.json e coleta os dados e triplos."""
    try:
        with open('datasets/disciplinas.json', encoding='utf-8') as f:
            data = json.load(f)
        for disciplina_data in data['disciplinas']:
            nome = disciplina_data['nome']
            disciplinas_mencionados.add(nome)
            # Tipos de conhecimento
            if 'tiposDeConhecimento' in disciplina_data:
                for tipo in disciplina_data['tiposDeConhecimento']:
                    tipos_conhecimento_mencionados.add(tipo)
                    add_triplo(safe_uri(nome), n.pertenceA, safe_uri(tipo))
            # Conceitos
            if 'conceitos' in disciplina_data:
                for conceito in disciplina_data['conceitos']:
                    conceitos_mencionados.add(conceito)
                    add_triplo(safe_uri(conceito), n.éEstudadoEm, safe_uri(nome))
    except FileNotFoundError:
        print("Arquivo disciplinas.json não encontrado")

def parse_mestres():
    """Parse mestres.json e coleta os dados e triplos."""
    try:
        with open('datasets/mestres.json', encoding='utf-8') as f:
            data = json.load(f)
        for mestre_data in data['mestres']:
            nome = mestre_data['nome']
            mestres_mencionados.add(nome)
            # Período histórico
            if 'períodoHistórico' in mestre_data:
                periodo = mestre_data['períodoHistórico']
                periodos_historicos_mencionados.add(periodo)
                add_triplo(safe_uri(nome), n.viveuEm, safe_uri(periodo))
            # Disciplinas
            if 'disciplinas' in mestre_data:
                for disciplina in mestre_data['disciplinas']:
                    disciplinas_mencionados.add(disciplina)
                    add_triplo(safe_uri(nome), n.ensina, safe_uri(disciplina))
    except FileNotFoundError:
        print("Arquivo mestres.json não encontrado")

def parse_obras():
    """Parse obras.json e coleta os dados e triplos."""
    try:
        with open('datasets/obras.json', encoding='utf-8') as f:
            data = json.load(f)
        for obra_data in data['obras']:
            titulo = obra_data['titulo']
            obras_mencionados.add(titulo)
            # Autor
            if 'autor' in obra_data:
                autor = obra_data['autor']
                mestres_mencionados.add(autor)
                add_triplo(safe_uri(titulo), n.foiEscritoPor, safe_uri(autor))
            # Conceitos
            if 'conceitos' in obra_data:
                for conceito in obra_data['conceitos']:
                    conceitos_mencionados.add(conceito)
                    add_triplo(safe_uri(titulo), n.explica, safe_uri(conceito))
    except FileNotFoundError:
        print("Arquivo obras.json não encontrado")

def parse_aprendizes():
    """Parse o arquivo de aprendizes (pgxxxxx.json ou exxxxx.json)."""
    try:
        with open('datasets/pg55920.json', encoding='utf-8') as f:
            data = json.load(f)
        for aprendiz_data in data:
            nome = aprendiz_data['nome']
            aprendizes_mencionados.add(nome)
            # Disciplinas
            if 'disciplinas' in aprendiz_data:
                for disciplina in aprendiz_data['disciplinas']:
                    disciplinas_mencionados.add(disciplina)
                    add_triplo(safe_uri(nome), n.aprende, safe_uri(disciplina))
            if 'idade' in aprendiz_data:
                add_triplo(
                    safe_uri(nome),
                    n.idade,
                    Literal(int(aprendiz_data['idade']), datatype=XSD.decimal)
                )
    except FileNotFoundError:
        print("Arquivo pg55920.json não encontrado")

def create_all_entities():
    """Cria todas as entidades mencionadas com pelo menos o nome."""
    # Criar conceitos
    for nome_conceito in conceitos_mencionados:
        uri_conceito = safe_uri(nome_conceito)
        g.add((uri_conceito, RDF.type, n.Conceito))
        g.add((uri_conceito, RDF.type, OWL.NamedIndividual))
        g.add((uri_conceito, n.nome, Literal(nome_conceito, datatype=XSD.string)))
    # Criar disciplinas
    for nome_disciplina in disciplinas_mencionados:
        uri_disciplina = safe_uri(nome_disciplina)
        g.add((uri_disciplina, RDF.type, n.Disciplina))
        g.add((uri_disciplina, RDF.type, OWL.NamedIndividual))
        g.add((uri_disciplina, n.nome, Literal(nome_disciplina, datatype=XSD.string)))
    # Criar mestres
    for nome_mestre in mestres_mencionados:
        uri_mestre = safe_uri(nome_mestre)
        g.add((uri_mestre, RDF.type, n.Mestre))
        g.add((uri_mestre, RDF.type, OWL.NamedIndividual))
        g.add((uri_mestre, n.nome, Literal(nome_mestre, datatype=XSD.string)))
    # Criar obras
    for titulo_obra in obras_mencionados:
        uri_obra = safe_uri(titulo_obra)
        g.add((uri_obra, RDF.type, n.Obra))
        g.add((uri_obra, RDF.type, OWL.NamedIndividual))
        g.add((uri_obra, n.titulo, Literal(titulo_obra, datatype=XSD.string)))
    # Criar aprendizes
    for nome_aprendiz in aprendizes_mencionados:
        uri_aprendiz = safe_uri(nome_aprendiz)
        g.add((uri_aprendiz, RDF.type, n.Aprendiz))
        g.add((uri_aprendiz, RDF.type, OWL.NamedIndividual))
        g.add((uri_aprendiz, n.nome, Literal(nome_aprendiz, datatype=XSD.string)))
    # Criar tipos de conhecimento
    for nome_tipo in tipos_conhecimento_mencionados:
        uri_tipo = safe_uri(nome_tipo)
        g.add((uri_tipo, RDF.type, n.TipoDeConhecimento))
        g.add((uri_tipo, RDF.type, OWL.NamedIndividual))
        g.add((uri_tipo, n.nome, Literal(nome_tipo, datatype=XSD.string)))
    # Criar períodos históricos
    for nome_periodo in periodos_historicos_mencionados:
        uri_periodo = safe_uri(nome_periodo)
        g.add((uri_periodo, RDF.type, n.PeríodoHistorico))
        g.add((uri_periodo, RDF.type, OWL.NamedIndividual))
        g.add((uri_periodo, n.nome, Literal(nome_periodo, datatype=XSD.string)))
    # Criar aplicações
    for nome_aplicacao in aplicacoes_mencionados:
        uri_aplicacao = safe_uri(nome_aplicacao)
        g.add((uri_aplicacao, RDF.type, n.Aplicação))
        g.add((uri_aplicacao, RDF.type, OWL.NamedIndividual))
        g.add((uri_aplicacao, n.nome, Literal(nome_aplicacao, datatype=XSD.string)))

def add_all_triplos():
    """Adiciona todos os triplos coletados ao grafo."""
    for triplo in triplos_para_adicionar:
        g.add(triplo)

def print_graph():
    """Print new ontology to the stdout."""
    print(g.serialize(format='turtle'))

def save_graph():
    """Save the populated ontology to a file."""
    g.serialize(destination="sapientia_ind.ttl", format="turtle")

def main():
    """Function responsible to delegate functions."""
    # Parse todos os arquivos e coleta triplos e entidades
    parse_conceitos()
    parse_disciplinas()
    parse_mestres()
    parse_obras()
    parse_aprendizes()
    # Criar todas as entidades mencionados
    create_all_entities()
    # Adicionar todos os triplos de relações
    add_all_triplos()
    # Salvar e imprimir
    save_graph() # TODO: uncomment
    # print_graph()

if __name__ == "__main__":
    main()
