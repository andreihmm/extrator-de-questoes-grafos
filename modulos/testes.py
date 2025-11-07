import gerarCsv as gCsv
import classificarDireito as cD
import formatarQuestoes as fQ
import extrairTexto as eT
import os
import contextlib

caminhoPDF = r"provas\ENADE\2012_direito.pdf"
saida_debug = os.path.join("outputs", "debug_listaQuestoes.txt")


# # PARA TESTAR SAÍDAS CRUAS:
# try:
#     with open(r"saidaTextoCru.txt", "w", encoding="utf-8") as arquivo:
#         arquivo.write(eT.extrair_texto_pdf(caminhoPDF))
# except Exception as e:
#     print(f"Erro ao extrair texto: {e}")

# try:
#     listaDeQuestoes = fQ.gerarListaQuestoes(caminhoPDF)
#     print("Geração da lista de questões concluída com sucesso!\n")

#     # Salvar prints em arquivo de debug
#     os.makedirs(os.path.dirname(saida_debug), exist_ok=True)
#     with open(saida_debug, "w", encoding="utf-8") as f, contextlib.redirect_stdout(f):
#         for i, questao in enumerate(listaDeQuestoes):
#             print(f"###NUMERO: {i}###\n")
#             print(f"Questão: {questao}\n")

# except Exception as e:
#     print(f"Erro ao gerar lista de questões: {e}")


# ## PARA FORMATAR AS QUESTOES:
# try:
#     fQ.formatarQuestoes(listaDeQuestoes)
# except Exception as e:
#     print(f"Erro ao formatar questões: {e}")



try:
    gCsv.gerar_csvs(caminhoPDF)
except Exception as e:
    print(f"Erro ao gerar csv: {e}")