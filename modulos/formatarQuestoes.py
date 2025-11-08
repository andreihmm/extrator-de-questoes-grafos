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
    return textoCru.split("QUESTÃO")

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
                                3. Coloque TITULO: para mostrar o nome/numeração da questão antes do enunciado. A Questão: 03 deve ter o título Questão 03.
                                4. Separe o enunciado e as alternativas de forma explícita:
                                - Coloque ENUNCIADO: antes do texto da pergunta.
                                - Coloque ALTERNATIVA: antes de cada alternativa.
                                5. Liste cada alternativa em uma linha separada.
                                6. Não use letras A), B), C)... apenas o texto da alternativa.
                                7. Preserve todas as informações importantes da questão.
                                8. Caso o texto seja sobre instruções da prova (sem pergunta), retorne apenas: INSTRUÇÃO.
                                9. Caso a questão seja objetiva, adicione ; TIPO: OBJETIVA ao final, e caso seja discursiva adicione ;TIPO: DISCURSIVA
                                10. As últimas 9 questões da prova são sobre percepção da prova, e por isso devem ser excluídas.
                                
                                Exemplo:
                                Entrada:
                                QUESTÃO 23: Qual a tradução de 'dog'?
                                A) Gato
                                B) Cachorro
                                C) Pássaro

                                Saída:
                                TITULO: QUESTÃO 23;
                                ENUNCIADO: Qual a tradução de 'dog'?
                                ALTERNATIVA: Gato
                                ALTERNATIVA: Cachorro
                                ALTERNATIVA: Pássaro
                                ; TIPO: OBJETIVA

                                Questão a corrigir:
                                {questao}
                                """
                        }
                ]
            )
            arquivo.write(f"Questão {i + 1} corrigida:\n")
            arquivo.write(chat_completion.choices[0].message.content + "\n\n")