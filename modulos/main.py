import formatarQuestoes as fQ
import extrairTexto as eT
import classificarDireito as cD
import gerarCsv as gCsv
import contextlib
import os

caminhoPDF = r"provas\ENADE\2012_direito.pdf"

# PARA GERAR A LISTA DE QUESTÕES:
saida_debug = os.path.join("outputs", "debug_listaQuestoes.txt")

try:
    listaDeQuestoes = fQ.gerarListaQuestoes(caminhoPDF)
    print("Geração da lista de questões concluída com sucesso!\n")

    # Salvar prints em arquivo de debug
    os.makedirs(os.path.dirname(saida_debug), exist_ok=True)
    with open(saida_debug, "w", encoding="utf-8") as f, contextlib.redirect_stdout(f):
        for i, questao in enumerate(listaDeQuestoes):
            print(f"###NUMERO: {i}###\n")
            print(f"Questão: {questao}\n")

except Exception as e:
    print(f"Erro ao gerar lista de questões: {e}")


## PARA FORMATAR AS QUESTOES:
try:
    fQ.formatarQuestoes(listaDeQuestoes)
except Exception as e:
    print(f"Erro ao formatar questões: {e}")



## PARA GERAR CSVs:
try:
    gCsv.gerar_csvs(caminhoPDF)
    print("CSV gerado com sucesso!\n")
except Exception as e:
    print(f"Erro ao gerar CSV: {e}")



## PARA GERAR A CLASSIFICAÇÃO DAS QUESTÕES:
try:
    cD.classificarQuestoesCsv()
except Exception as e:
    print(f"Erro ao gerar classificação das questões: {e}")

