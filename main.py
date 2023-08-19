import pandas as pd
from collections import defaultdict
from grafoponderado import GrafoPonderado
import networkx as nx
import matplotlib.pyplot as plt

anos = list(range(2002, 2024))
ano = int(input("Informe o ano a considerar: "))
threshold = float(input("Informe o percentual mínimo de concordância (threshold) (ex: 0.9): "))
partido = input("Informe os partidos a analisar, separados por , (ex: PT, MDB, PL): ").split(", ")

if not partido[0].strip():
    partido = []

if ano not in anos:
    print(f"Ano inválido. Escolha um ano entre 2002 e 2023.")
else:
    print("Processando...\n")
    grafo_resultado_filtros = f"grafo_votacoes_normalizado{ano}.txt"
    grafico_centralidade = f"grafico_centralidade_{ano}.png"
    heatmap = f"heatmap_{ano}.png"
    grafo = f"grafo_{ano}.png"
    #grafo_resultado_filtros_inversao_de_pesos = f"grafo_votacoes_iguais_por_filtros_inversao_de_pesos_{ano}.txt"
    #GrafoPonderado.grafo_inversao_de_pesos(ano, partido, grafo_resultado_filtros_inversao_de_pesos, threshold)
    GrafoPonderado.criar_grafo_votacoes_iguais(ano, partido, grafo_resultado_filtros, threshold, f"grafico_centralidade_{ano}.png", f"heatmap_{ano}.png", f"grafo_{ano}.png")
    print(f"Grafo de votações normalizada salvo em {grafo_resultado_filtros}. Salvos em arquivo txt também.")
    print(f"Os plots foram salvos nos arquivos:\n{grafico_centralidade}\n{heatmap}\n{grafo}\n\n")

