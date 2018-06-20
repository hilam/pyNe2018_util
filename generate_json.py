# ler programaçção de um csv e montar trecho de código html
# para injetar na página
import csv

header = """{
    "0.0.1": [{
"""

comma = ","
datas = ["2018-05-24", "2018-05-25", "2018-05-26"]
qtde_date = {key:0 for key in datas}
group_date = 0

locais = ["[LAB] GAROTAS DO ENIAC", "[LAB] ADA LOVELACE", "[LAB] GRACE HOPPER", "[SALA] HIPÁCIA DE ALEXANDRIA",
          "[SALA] KAREN SPARK JONES", "[LAB] JEAN SAMMET", "[LAB] RADIA PERLMAN", "[LAB] CAROL SHAW",
          "[SALA] ROBERTA WILLIAMS", "[SALA] FRANCES ALLEN", "TEATRO PYTHÔNICO", "FREETIME"]

lista = f''
for local in locais:
    lista += f'"{local}"{comma if local != locais[-1] else ""} '

schedule_header = f"""        "tracks": [{lista}], 
"""

schedules = open("schedule.json","w+")
tracks = open("tracks.json","w+")

tracks.write(f"{header}")
schedules.write(f"{header}")
schedules.write(f"{schedule_header}")
schedules.write(f"""        "{datas[group_date]}": [""")

with open("programacao.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    qtde_total = 0
    for row in reader:
        data_evento = row["Data"][:10]
        qtde_date[data_evento] += 1
        qtde_total += 1

with open("programacao.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    atual = 1
    total = 1

    for row in reader:
        id = row["ID"]
        titulo = row["Título"]
        nome = row["Palestrante"]
        email = row["E-mail"]
        imagem = row["Foto"]
        bio = row["Bio"]
        data_evento = row["Data"][:10]
        hora_inicio = row["Início"][:5]
        hora_fim = row["Final"][:5]
        local = row["Local"]

        track = f"""
        "{id}": {{
            "title": "{titulo}",
            "description": "{email}",
            "type": "default",
            "speaker": {{
                "name": "{nome}",
                "info": "{bio}",
                "photo": "{imagem}"
            }}
        }}{comma if total < qtde_total else ""}
        """

        tracks.write(f"{track}")

        schedule = f"""
        {{
          "talk_id": "{id}",
          "title": "{titulo}",
          "start_time": "{hora_inicio}",
          "end_time": "{hora_fim}",
          "track": "{locais.index(local)+1}"
        }}{comma if atual < qtde_date[data_evento] else ""}
        """

        # controle externo do grupamento de data
        if data_evento != datas[group_date]:
            schedules.write(""" ], \n """)
            schedules.write(f"""       "{data_evento}": [""")
            group_date += 1
            atual = 1

        schedules.write(f"{schedule}")

        atual += 1
        total += 1

tracks.write("} ] }\n")
tracks.close()

schedules.write("] } ] }\n")
schedules.close()
