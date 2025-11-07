import os
import extrairTexto as eT
from typing import List
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_GRAFOS = os.getenv('GROQ_GRAFOS')
client = Groq(api_key=GROQ_GRAFOS)

def gerarListaQuestoes(caminhoPDF):
    textoCru = eT.extrair_texto_pdf(caminhoPDF)
    return textoCru.split("QUESTÃ")

def formatarQuestoes(questoes):
    caminho_saida = os.path.join("outputs", "saidaGrafos.txt")

    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        for i, questao in enumerate(questoes):
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0.0,
                messages=[
                        {
                            "role": "system",
                            "content": (
                                "Você é um assistente especializado em revisar e padronizar questões de prova. "
                                "Responda apenas com o texto final da questão formatada, sem explicações ou comentários adicionais."
                            )
                        },
                        {
                            "role": "user",
                            "content": f"""
                                Corrija e padronize a seguinte questão de prova conforme as regras abaixo:

                                1. Mantenha apenas texto puro.
                                2. Corrija erros de português, pontuação e clareza.
                                3. Separe o enunciado e as alternativas de forma explícita:
                                - Coloque ENUNCIADO: antes do texto da pergunta.
                                - Coloque ALTERNATIVA: antes de cada alternativa.
                                4. Liste cada alternativa em uma linha separada.
                                5. Não use letras A), B), C)... apenas o texto da alternativa.
                                6. Preserve todas as informações importantes da questão.
                                7. Caso o texto seja sobre instruções da prova (sem pergunta), retorne apenas: INSTRUÇÃO.
                                8. Caso a questão seja objetiva, adicione ;OBJETIVA ao final, e caso seja discursiva adicione ;DISCURSIVA
                                
                                Exemplo:
                                Entrada:
                                QUESTÃO: Qual a tradução de 'dog'?
                                A) Gato
                                B) Cachorro
                                C) Pássaro

                                Saída:
                                ENUNCIADO: Qual a tradução de 'dog'?
                                ALTERNATIVA: Gato
                                ALTERNATIVA: Cachorro
                                ALTERNATIVA: Pássaro
                                ;DISCURSIVA

                                Questão a corrigir:
                                {questao}
                                """
                        }
                ]
            )
            arquivo.write(f"Questão {i + 1} corrigida:\n")
            arquivo.write(chat_completion.choices[0].message.content + "\n\n")