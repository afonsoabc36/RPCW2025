# TPC5

## Metadata

| Title |    Date    | AuthorId |  AuthorName  | UcSigla |                        UcNome                        |
| :---: | :--------: | :------: | :----------: | :-----: | :--------------------------------------------------: |
| TPC5  | 18-03-2025 | PG55920  | Afonso Silva |  RPCW   | Representação e Processamento de Conhecimento na Web |

## Resumo

- Povoar a ontologia `cinema-base.ttl` desenvolvida na aula TP6 com 500 filmes.

## Run

### Fazer download dos datasets

> [!NOTE]
> Este processo pode demorar algum tempo e os ficheiros ocupam bastante espaço.

```sh
./get_imdb_movie_files
```

> [!WARNING]
> Este script foi escrito em Bash (a shell superior).
> O interpretador tem de estar disponível em `/bin/bash`,
> pois o script pode não funcionar corretamente com outros shells.

### Concatenar a informação

- Isto irá criar um ficheiro `movies.json` na diretoria `data` com a informação sobre os mesmos concatenada.

```sh
python3 concatenate_data.py
```

> [!NOTE]
> Isto pode também demorar algum tempo a executar.
> Pode demorar menos ao passar o argumento `low_memory=False` à função `read_csv`.
> Isto irá consumir bastante memória e não foi possível executar no meu caso.

### Criar um novo ficheiro Turtle

Para verificar como ficaria a ontologia populada corra o comando:

```sh
python3 populate.py
```

> [!NOTE]
> Isto irá apenas imprimir o resultado para o stdout.
> Para a guardar redirecione o output para um ficheiro.

```sh
python3 populate.py > cinema.ttl
```

## Resultados

### Script de concatenação

Ficheiro `data/movies.json`:

```json
{
    "movies": [
        {
            "id": "tt0000147",
            "originalTitle": "The Corbett-Fitzsimmons Fight",
            "duration": 100,
            "releaseYear": 1897,
            "genres": [
                "Documentary",
                "News",
                "Sport"
            ],
            "originalLanguage": null,
            "originalCountry": "US",
            "peopleInvolved": [
                {
                    "nconst": "nm0103755",
                    "category": "producer",
                    "job": "producer",
                    "name": "William A. Brady"
                }
            ]
        }, ...
    ]
}
```

### Ontologia populada

Ficheiro `cinema.ttl` com os novos indivíduos e as suas relações.
