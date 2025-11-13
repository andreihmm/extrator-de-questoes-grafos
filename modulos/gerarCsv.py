import os
import csv
import uuid
import re

INPUT_FILE = os.path.join("outputs", "saidaGrafos.txt")
OUTPUT_DIR = os.path.join("outputs", "csvs")
QUESTOES_CSV = os.path.join(OUTPUT_DIR, "questoes.csv")


def parse_questoes(input_file):
    questoes = []
    current_question = None
    reading_enunciado = False

    with open(input_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            print(f"[Linha {line_num}] {line}")

            # Detecta o início de uma nova questão pelo "TITULO:"
            if re.match(r"(?i)^TITULO\s*:", line):
                current_question = {
                    "uuid": str(uuid.uuid4()),
                    "titulo": "",
                    "enunciado": "",
                    "tipo": ""
                }
                questoes.append(current_question)
                reading_enunciado = False

                # Captura o título após "TITULO:"
                match = re.search(r"(?i)TITULO\s*:\s*(.*?)(;|$)", line)
                if match:
                    current_question["titulo"] = match.group(1).strip()
                    print(f"  -> Título detectado: {current_question['titulo']}")
                continue

            if not current_question:
                continue

            # Detecta enunciado
            if re.match(r"(?i)^ENUNCIADO\s*:", line):
                reading_enunciado = True
                current_question["enunciado"] = line.strip()
                print(f"  -> Início de enunciado: {current_question['enunciado']}")
                continue

            # Detecta tipo
            if re.search(r"(?i)\bTIPO\s*:", line):
                match = re.search(r"(?i)TIPO\s*:\s*(.*)", line)
                if match:
                    current_question["tipo"] = match.group(1).strip(" ;")
                    print(f"  -> Tipo detectado: {current_question['tipo']}")
                reading_enunciado = False
                continue

            # Continua o enunciado (incluindo alternativas e demais linhas)
            if reading_enunciado:
                current_question["enunciado"] += " " + line
                print(f"  -> Enunciado atualizado: {current_question['enunciado']}")

    return questoes


def extrair_metadados(caminho_pdf):
    nome_arquivo = os.path.basename(caminho_pdf)
    match = re.search(r"(19|20)\d{2}", nome_arquivo)
    ano = match.group(0) if match else "DESCONHECIDO"
    exame = os.path.basename(os.path.dirname(caminho_pdf)).upper()
    return exame, ano


def filtrar_questoes(questoes):
    filtradas = []
    questao9_questoes = []  # ← armazenará as próprias questões 9, não só os índices

    for q in questoes:
        titulo = q.get("titulo", "").strip()
        if not titulo:
            filtradas.append(q)
            continue

        titulo_normalizado = titulo.lower()

        if re.search(r"(quest[aã]o\s*)?(discursiva\s*)?0?[1-2]\b", titulo_normalizado) and (q.get("tipo", "").strip().lower() == "discursiva" or q.get("tipo", "").strip().lower() == "discursivas"):
            print(f"Removendo {titulo}")
            continue

        # Remove questões 1 a 8 (somente se tipo for OBJETIVA)
        if re.search(r"quest[aã]o\s*0?[1-8]\b", titulo_normalizado) and q.get("tipo", "").strip().lower() == "objetiva":
            print(f"Removendo {titulo}")
            continue

        # Remove instruções
        if re.search(r"^instru[cç][aã]o(?:es)?\b", titulo_normalizado):
            print(f"Removendo {titulo}")
            continue

        # Marca possíveis 'Questão 9'
        if re.search(r"quest[aã]o\s*0?9\b", titulo_normalizado):
            questao9_questoes.append(q)

        filtradas.append(q)

    # Remove apenas a última "Questão 9"
    if len(questao9_questoes) > 1:
        ultima_questao9 = questao9_questoes[-1]
        filtradas = [q for q in filtradas if q is not ultima_questao9]
        print(f"Removendo apenas a última ocorrência de '{ultima_questao9['titulo']}'")

    return filtradas


def salvar_csv(questoes, questoes_csv, exame, ano):
    os.makedirs(os.path.dirname(questoes_csv), exist_ok=True)

    with open(questoes_csv, "w", newline="", encoding="utf-8") as qfile:
        writer = csv.writer(qfile, delimiter=";")
        writer.writerow(["questao_uuid", "titulo", "enunciado", "tipo", "exame", "ano"])
        for q in questoes:
            if q["enunciado"]:
                writer.writerow([
                    q["uuid"],
                    q.get("titulo", ""),
                    q["enunciado"],
                    q.get("tipo", ""),
                    exame,
                    ano
                ])


def gerar_csvs(caminho_pdf, input_file=INPUT_FILE):
    exame, ano = extrair_metadados(caminho_pdf)
    print(f"\n📘 Exame detectado: {exame}\n📅 Ano: {ano}")

    questoes = parse_questoes(input_file)
    print(f"\nTotal de questões detectadas: {len(questoes)}")

    questoes_filtradas = filtrar_questoes(questoes)
    print(f"Após filtro: {len(questoes_filtradas)} questões restantes\n")

    salvar_csv(questoes_filtradas, QUESTOES_CSV, exame, ano)
    print(f"Arquivo CSV gerado em: {QUESTOES_CSV}")
