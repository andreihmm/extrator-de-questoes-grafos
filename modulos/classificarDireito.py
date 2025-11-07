import os
import csv
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_CLASSIFICAR = os.getenv("GROQ_CLASSIFICAR")
client = Groq(api_key=GROQ_CLASSIFICAR)

def classificarQuestoesCsv():
    input_csv = os.path.join("outputs", "csvs", "questoes.csv")
    output_csv = os.path.join("outputs", "csvs", "classificacoes.csv")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Prompt do sistema (apenas disciplinas de computação)
    prompt_sistema = (
        "Você é um assistente que classifica questões de Direito com base nas seguintes disciplinas:\n"
        "- Direito Constitucional\n"
        "- Direito Administrativo\n"
        "- Direito Civil\n"
        "- Direito Penal\n"
        "- Direito Processual Civil\n"
        "- Direito Processual Penal\n"
        "- Direito do Trabalho\n"
        "- Direito Processual do Trabalho\n"
        "- Direito Tributário\n"
        "- Direito Empresarial\n"
        "- Direito Internacional\n"
        "- Direito Ambiental\n"
        "- Filosofia do Direito\n"
        "- Teoria do Direito\n"
        "- Hermenêutica Jurídica\n"
        "- Direitos Humanos\n"
        "- Ética e Cidadania\n"
        "- Formação Geral\n"
        "- Outros\n"
        "Responda apenas com a tag mais apropriada para a questão, sem explicações."
    )


    with open(input_csv, "r", encoding="utf-8") as infile, \
         open(output_csv, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile, delimiter=";")
        writer = csv.writer(outfile, delimiter=";")
        writer.writerow(["questao_uuid", "classificacao"])

        for row in reader:
            questao_uuid = row["questao_uuid"]
            enunciado = row["enunciado"]

            print(f"\nClassificando questão {questao_uuid}: {enunciado[:70]}...")

            try:
                chat_completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": enunciado}
                    ],
                    temperature=0.0
                )
                classificacao = chat_completion.choices[0].message.content.strip()
                print(f"  -> {classificacao}")
                writer.writerow([questao_uuid, classificacao])
            except Exception as e:
                print(f"Erro ao classificar questão {questao_uuid}: {e}")
                writer.writerow([questao_uuid, "ERRO"])

    print(f"\nClassificações salvas em: {output_csv}")
