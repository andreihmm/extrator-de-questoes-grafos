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

            if re.match(r"(?i)^quest(ã|a)o ", line):
                current_question = {
                    "uuid": str(uuid.uuid4()),
                    "enunciado": "",
                    "alternativas": []
                }
                questoes.append(current_question)
                reading_enunciado = True
                print(f"  -> Nova questão detectada (UUID {current_question['uuid']})")
                continue

            if current_question:
                # Detecta alternativas (ex: "A) texto da alternativa")
                if re.match(r"^[A-Z]\)", line):
                    reading_enunciado = False
                    current_question["alternativas"].append(line)
                    print(f"  -> Alternativa adicionada: {line}")
                elif reading_enunciado:
                    # Concatena linhas do enunciado
                    current_question["enunciado"] += (" " + line if current_question["enunciado"] else line)
                    print(f"  -> Enunciado atualizado: {current_question['enunciado']}")
                else:
                    # Continuação de alternativa quebrada
                    if current_question["alternativas"]:
                        current_question["alternativas"][-1] += " " + line
                        print(f"  -> Alternativa atualizada: {current_question['alternativas'][-1]}")

    return questoes

def extrair_metadados(caminho_pdf):
    # Nome do arquivo (ex: "2012_direito.pdf")
    nome_arquivo = os.path.basename(caminho_pdf)

    # Tenta achar um ano no nome do arquivo (aceita 2012_direito.pdf ou ENADE2012.pdf)
    match = re.search(r"(19|20)\d{2}", nome_arquivo)
    ano = match.group(0) if match else "DESCONHECIDO"

    # Nome da pasta pai (ex: "ENADE")
    exame = os.path.basename(os.path.dirname(caminho_pdf)).upper()

    return exame, ano


def salvar_csv(questoes, questoes_csv, exame, ano):
    os.makedirs(os.path.dirname(questoes_csv), exist_ok=True)

    # CSV: uuid; enunciado; exame; ano
    with open(questoes_csv, "w", newline="", encoding="utf-8") as qfile:
        writer = csv.writer(qfile, delimiter=";")
        writer.writerow(["questao_uuid", "enunciado", "exame", "ano"])
        for q in questoes:
            if q["enunciado"]:
                writer.writerow([q["uuid"], q["enunciado"], exame, ano])


def gerar_csvs(caminho_pdf, input_file=INPUT_FILE):
    exame, ano = extrair_metadados(caminho_pdf)
    print(f"\n📘 Exame detectado: {exame}\n📅 Ano: {ano}")

    questoes = parse_questoes(input_file)
    print(f"\nTotal de questões detectadas: {len(questoes)}\n")

    salvar_csv(questoes, QUESTOES_CSV, exame, ano)
    print(f"✅ Arquivo CSV gerado em: {QUESTOES_CSV}")