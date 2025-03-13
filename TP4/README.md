# TPC4 - DBPedia Harvester

## Metadata

| Title |    Date    | AuthorId |  AuthorName  | UcSigla |                        UcNome                        |
| :---: | :--------: | :------: | :----------: | :-----: | :--------------------------------------------------: |
| TPC4  | 13-03-2025 | PG55920  | Afonso Silva |  RPCW   | Representação e Processamento de Conhecimento na Web |

## Resumo

- Recolher informação de filmes presentes na DBPedia.
- Informações a recolher sobre cada filme:

```
{
  "id": linkDBPediaFilme,
  "titulo": tituloFilme,
  "pais": paisProducao,
  "dataLancamento": dataLancamento,
  "realizador": nomeRealizador,
  "abstract": abstractEnglish,
  "genero": [generoFilme],
  "elenco": [
              {
                "id": linkDBPediaAtor,
                "nome": nomeAtor,
                "dataNasc": dataNascimentoAtor,
                "origem": paisCidadeOrigem
              }
            ],
}
```

## Resultados

- Queries utilizadas para recolher informação presentes no ficheiro [harvester](./harvester.py).
- Resultado final presente no ficheiro [dataset](./dataset.json).
- Foi imposto um limite ao recolher filmes devido a limitação da API da DBPedia (timeout dos pedidos).
