# TPC3 - Quiz App

## Metadata

| Title |    Date    | AuthorId |  AuthorName  | UcSigla |                        UcNome                        |
| :---: | :--------: | :------: | :----------: | :-----: | :--------------------------------------------------: |
| TPC3  | 11-03-2025 | PG55920  | Afonso Silva |  RPCW   | Representação e Processamento de Conhecimento na Web |

## Resumo

- Desenvolvimento de uma aplicação de Quizzes utilizando Flask.
- Geração automática de perguntas através de dados da ontologia de História de Portugal.
- Obter os dados através de pedidos ao GraphQL, utilizando queries SPARQL.

## Resultados

- Existência de 2 tipos de perguntas (Verdadeiro/Falso, Escolha Múltipla).
- Perguntas sobre Presidentes, Reis, Dinastias e Descobrimentos.

### Verdadeiro/Falso

- O Rei {nome} tem o cognome {cognome}.
- O descobrimento descrito por '{descrição}' ocorreu durante a Dinastia {nome}.
- O Militante {nomeMilitante} representa o partido {nomePartido}.

### Escolha Múltipla

- Em que ano nasceu o Rei {nome}?
- Quantos mandatos cumpriu o Presidente {nome}?
- O Presidente {nome} nasceu em que ano?

## Run

Primeiro, iniciar a API:

```
python3 app_api.py
```

Depois, correr a aplicação:

```
python3 app_jinja.py
```

Por último, navegar para o [website](http://localhost:5000/).
