import os
import csv
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_CLASSIFICAR = os.getenv("GROQ_CLASSIFICAR")
client = Groq(api_key=GROQ_CLASSIFICAR)

def classificarQuestoesCsv():
    input_csv = os.path.join("outputs", "csvs", "questoes.csv")
    output_csv = os.path.join("outputs", "csvs", "classificacoes.csv")
    output_txt = os.path.join("outputs", "csvs", "classificacoes_detalhes.txt")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    prompt_sistema = (
        "Você é um assistente que classifica questões de Direito com base nas seguintes disciplinas:\n"
        "- Antropologia e Sociologia Jurídicas\n"
        "- Psicologia Jurídica\n"
        "- Filosofia do Direito e Ética\n"
        "- História do Direito\n"
        "- Teoria Geral do Direito\n"
        "- Teoria do Estado e Ciência Política\n"
        "- Direito Constitucional\n"
        "- Direito Ambiental\n"
        "- Direito Administrativo\n"
        "- Direito Tributário\n"
        "- Direito Penal\n"
        "- Direito Civil\n"
        "- Direito Econômico e Economia Política\n"
        "- Direito Empresarial\n"
        "- Direito do Consumidor\n"
        "- Direito do Trabalho\n"
        "- Direito Internacional\n"
        "- Direitos Humanos\n"
        "- Direito Processual e Formas Consensuais de Solução de Conflitos\n"
        "- Direito Previdenciário\n"
        "- Formação Geral\n"
        "- Outros\n\n"
        "Instruções importantes:\n"
        "1. Toda questão tem que ter pelo 1 ou 2 classificações"
        "2. Não classifique uma questão com mais de 2 classificações."
        "3. Para cada categoria aplicável, responda em uma linha separada, no formato:\n"
        "<ID>;<CLASSIFICAÇÃO>\n"
        "4. Não escreva explicações, comentários ou texto adicional.\n"
        "5. Use exatamente os nomes das disciplinas listadas acima.\n"
        "Exemplo de resposta válida:\n"
        "123;Direito Constitucional\n"
        "123;Direito Administrativo"
    )

    with open(input_csv, "r", encoding="utf-8") as infile, \
         open(output_csv, "w", newline="", encoding="utf-8") as outfile, \
         open(output_txt, "w", encoding="utf-8") as txtfile:

        reader = csv.DictReader(infile, delimiter=";")
        writer = csv.writer(outfile, delimiter=";")
        writer.writerow(["questao_uuid", "classificacao"])

        for row in reader:
            questao_uuid = row["questao_uuid"]
            enunciado = row["enunciado"]

            print(f"\nClassificando questão {questao_uuid}: {enunciado[:70]}...")

            try:
                # envia o ID e o enunciado ao modelo
                user_content = f"Questão ID: {questao_uuid}\nEnunciado: {enunciado}"

                chat_completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": user_content}
                    ],
                    temperature=0.0
                )

                resposta_bruta = chat_completion.choices[0].message.content.strip()

                # grava o texto completo no TXT
                txtfile.write(f"Questão {questao_uuid}\n")
                txtfile.write(f"Enunciado: {enunciado}\n")
                txtfile.write("Resposta completa do modelo:\n")
                txtfile.write(f"{resposta_bruta}\n")
                txtfile.write("=" * 100 + "\n\n")

                # divide a resposta em linhas válidas no formato ID;Categoria
                linhas_validas = []
                for linha in resposta_bruta.split("\n"):
                    linha = linha.strip()
                    if not linha:
                        continue
                    # tenta capturar formato tipo "123;Direito Civil"
                    match = re.match(r"^(\S+)\s*;\s*(.+)$", linha)
                    if match:
                        qid, categoria = match.groups()
                        linhas_validas.append((qid.strip(), categoria.strip()))
                    else:
                        # fallback: se a linha não seguir o formato, usa o ID atual
                        linhas_validas.append((questao_uuid, linha))

                # grava todas as classificações da questão
                for qid, categoria in linhas_validas:
                    writer.writerow([qid, categoria])
                    print(f"  -> {qid}; {categoria}")

            except Exception as e:
                print(f"Erro ao classificar questão {questao_uuid}: {e}")
                writer.writerow([questao_uuid, "ERRO"])
                txtfile.write(f"Questão {questao_uuid} - ERRO: {e}\n")
                txtfile.write("=" * 100 + "\n\n")

    print(f"\n✅ Classificações salvas em: {output_csv}")
    print(f"🗒️  Detalhes completos salvos em: {output_txt}")

if __name__ == "__main__":
    classificarQuestoesCsv()
