import os

for i in range(1,9):
    os.mkdir(f"TP{i}")
    os.chdir(f"./TP{i}")
    with open("README.md", "w") as readme:
        readme.write(f"""# TPC{i}

## Metadata

| Title | Date | AuthorId | AuthorName | UcSigla | UcNome |
|:-----:|:----:|:--------:|:----------:|:-------:|:------:|
| TPC{i} | | PG55920 | Afonso Silva | RPCW | Representação e Processamento de Conhecimento na Web |

## Resumo

-
-
-

## Resultados

""")
    os.chdir("..")
