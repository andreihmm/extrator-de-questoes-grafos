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
                                3. Coloque TITULO: para mostrar o nome/numeração da questão antes do enunciado. A Questão: 03 deve ter o título Questão 03. A questão Questão: DISCURSIVA 01 deve ser Questão Discursiva 01
                                4. Coloque ENUNCIADO: antes do texto e da pergunta
                                5. Se a questão tem um texto antes do enunciado, coloque TEXTO: antes do texto.
                                7. Quando o texto tem fonte/referência bibliográfica, exclua ela. Considere que o texto é o que está antes dela e a pergunta depois.
                                8. Separe o enunciado e as alternativas de forma explícita:
                                - Coloque PERGUNTA: antes da pergunta.
                                - Coloque ALTERNATIVA: antes de cada alternativa, que são identificadas por letras.
                                9. Liste cada alternativa em uma linha separada.
                                10. Não use letras A), B), C)... apenas o texto da alternativa.
                                11. Em questões com afirmações/asserções numeradas por numeros romanos, colocar ASSERÇÃO: antes de cada asserção. 
                                - As asserções nunca são iguais as alternativas.
                                - As asserções são sempre numeradas por numeros romanos de I a V
                                12. Preserve todas as informações importantes da questão.
                                13. Caso o texto seja sobre instruções da prova (sem pergunta), retorne apenas: INSTRUÇÃO.
                                14. Caso a questão seja objetiva, adicione ; TIPO: OBJETIVA ao final, e caso seja discursiva adicione ;TIPO: DISCURSIVAS
                                15. Em questões discursivas não aponte alternativas
                                
                                Exemplo 1:
                                Entrada:
                                QUESTÃO 23: 
                                John has two cats and a dog
                                BRASIL. Supremo Tribunal Federal. ADI n.o 3.386/DF. Rel. Min. Cármen Lúcia.
                                Julgamento em: 14/04/2011, publicada no DJe n.o 162, de 24/08/2011.
                                Disponível em: <http://redir.stf.jus.br>. Acesso em: 13 jul. 2012.

                                Como citado pelo texto, qual a tradução de 'dog'?
                                A) Gato
                                B) Cachorro
                                C) Pássaro

                                Saída:
                                TITULO: QUESTÃO 23;
                                ENUNCIADO:
                                TEXTO: John has two cats and a dog
                                PERGUNTA: Qual a tradução de 'dog'?
                                ALTERNATIVA: Gato
                                ALTERNATIVA: Cachorro
                                ALTERNATIVA: Pássaro
                                ; TIPO: OBJETIVA

                                Questão a corrigir:
                                {questao}

                                Exemplo 2:
                                Entrada:
                                QUESTÃO 24: 
                                John has two cats and a dog

                                Avalie as seguintes afirmações:
                                    I. João tem um gato
                                    II. João tem um elefante
                                    III. João tem um cachorro
                                É correto apenas o que se afirma em
                                A) I e II.
                                B) I e III.
                                C) III e IV.
                                D) Somente III

                                Saída:
                                TITULO: QUESTÃO 24;
                                ENUNCIADO:
                                TEXTO: John has two cats and a dog
                                PERGUNTA: Avalie as seguintes afirmações:
                                ASSERÇÃO: I. João tem um gato
                                ASSERÇÃO: II. João tem um elefante
                                ASSERÇÃO: I. João tem um gato
                                ASSERÇÃO: III. João tem um cachorro
                                ALTERNATIVA: I e II.
                                ALTERNATIVA: I e III.
                                ALTERNATIVA: Somente III
                                ; TIPO: OBJETIVA

                                Questão a corrigir:
                                {questao}
                                
                                """
                        }
                ]
            )
            arquivo.write(f"Questão {i + 1} corrigida:\n")
            arquivo.write(chat_completion.choices[0].message.content + "\n\n")