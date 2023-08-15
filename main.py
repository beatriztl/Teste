import pandas as pd
from collections import defaultdict
from grafoponderado import GrafoPonderado
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# #Lendo o arquivo de votações
# tabela = pd.read_excel('votacoesVotos-2023.xlsx')
# arquivo_votacoes = tabela[['idVotacao', 'voto', 'deputado_id', 'deputado_nome']]

# #Criando o grafo das participações dos deputados
# participacao = tabela['deputado_nome'].value_counts().sort_index()
# arquivo_saida = 'participacao_deputados.txt'
# participacao.to_csv(arquivo_saida, sep='\t', header=['Participações'], index_label='Deputado(a)')
# print("\nArquivo de participação dos deputados criado: participacao_deputados.txt")

# #Criando o grafo de votos iguais
# data = tabela.values.tolist()
# grafo = GrafoPonderado()
# grafo.grafo_resultado_votos_iguais(data)
# print("Grafo de resultados iguais processado.\n")

# anos = list(range(2002, 2024))
# ano = int(input("Digite o ano que você deseja verificar: "))
# partido = input("Digite o(s) partido(s) separados por vírgula (ou deixe em branco para não filtrar por partido): ").split(", ")

# if not partido[0].strip():
#     partido = []

# if ano not in anos:
#     print(f"Ano inválido. Escolha um ano entre 2002 e 2023.")
# else:
#     threshold = 0.9
#     grafo_resultado_filtros = f"grafo_votacoes_iguais_por_filtros_{ano}.txt"
#     GrafoPonderado.criar_grafo_votacoes_iguais(ano, partido, grafo_resultado_filtros, threshold)
#     print(f"Grafo de votações iguais normalizado salvo em {grafo_resultado_filtros}.")

anos = list(range(2002, 2024))
ano = int(input("Digite o ano que você deseja verificar: "))
partido = input("Digite o(s) partido(s) separados por vírgula (ou deixe em branco para não filtrar por partido): ").split(", ")

if not partido[0].strip():
    partido = []

if ano not in anos:
    print(f"Ano inválido. Escolha um ano entre 2002 e 2023.")
else:
    threshold = input("Informe o percentual minimo de concordancia ( threshold ) ( ex . 0.9) :") 
    grafo_resultado_filtros = f"grafo_votacoes_iguais_por_filtros_{ano}.txt"
    grafico_centralidade = f"grafico_centralidade_{ano}.pdf"
    GrafoPonderado.criar_grafo_votacoes_iguais(ano, partido, grafo_resultado_filtros, threshold, f"grafico_centralidade_{ano}.pdf")
    print(f"Grafo de votações iguais normalizado salvo em {grafo_resultado_filtros}.")