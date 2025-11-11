import os
import csv
import uuid
import re

# Caminhos padrão
INPUT_FILE = os.path.join("outputs", "saidaGrafos.txt")
OUTPUT_DIR = os.path.join("outputs", "csvs")
QUESTOES_CSV = os.path.join(OUTPUT_DIR, "questoes.csv")

def extrair_metadados(caminho_pdf):
    """Extrai nome do exame e ano a partir do caminho do PDF."""
    nome_arquivo = os.path.basename(caminho_pdf)
    match = re.search(r"(19|20)\d{2}", nome_arquivo)
    ano = match.group(0) if match else "DESCONHECIDO"
    exame = os.path.basename(os.path.dirname(caminho_pdf)).upper()
    return exame, ano

def parse_questoes(input_file):
    """Lê o arquivo de texto e cria uma lista de questões formatadas."""
    questoes = []
    current_question = None

    with open(input_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            print(f"[Linha {line_num}] {line}")

            # Detecta início de uma nova questão (ENUNCIADO)
            if line.startswith("ENUNCIADO:"):
                if current_question:  # salva a anterior
                    questoes.append(current_question)

                current_question = {
                    "uuid": str(uuid.uuid4()),
                    "enunciado": line.replace("ENUNCIADO:", "").strip(),
                    "alternativas": [],
                    "tipo": "DESCONHECIDO"
                }
                print(f"  -> Nova questão criada (UUID {current_question['uuid']})")
                continue

            # Alternativas
            if line.startswith("ALTERNATIVA:") and current_question:
                alternativa = line.replace("ALTERNATIVA:", "").strip()
                current_question["alternativas"].append(alternativa)
                print(f"  -> Alternativa adicionada: {alternativa}")
                continue

            # Tipo de questão (finalizador)
            if line.startswith(";OBJETIVA") or line.startswith(";DISCURSIVA"):
                if current_question:
                    current_question["tipo"] = line.replace(";", "").strip().upper()
                    print(f"  -> Tipo detectado: {current_question['tipo']}")
                    questoes.append(current_question)
                    current_question = None
                continue

    # Garante que a última questão seja salva
    if current_question:
        questoes.append(current_question)

    print(f"\nTotal de questões detectadas: {len(questoes)}")
    return questoes

def salvar_csv(questoes, questoes_csv, exame, ano):
    """Salva as questões no formato CSV com delimitador ';'."""
    os.makedirs(os.path.dirname(questoes_csv), exist_ok=True)

    with open(questoes_csv, "w", newline="", encoding="utf-8") as qfile:
        writer = csv.writer(qfile, delimiter=";", quoting=csv.QUOTE_NONE, escapechar="\\")
        writer.writerow(["questao_uuid", "enunciado", "exame", "ano", "tipo"])
        for q in questoes:
            if q["enunciado"]:
                writer.writerow([q["uuid"], q["enunciado"], exame, ano, q["tipo"]])

    print(f"✅ CSV gerado em: {questoes_csv}")

def gerar_csvs(caminho_pdf, input_file=INPUT_FILE):
    """Função principal que coordena a extração e geração do CSV."""
    exame, ano = extrair_metadados(caminho_pdf)
    print(f"📘 Exame: {exame}, Ano: {ano}")
    questoes = parse_questoes(input_file)
    salvar_csv(questoes, QUESTOES_CSV, exame, ano)

# Exemplo de uso:
# gerar_csvs(r"provas\ENADE\2012_direito.pdf")
