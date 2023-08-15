from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

class GrafoPonderado:
    def __init__(self):
        self.lista_adj = {}
        self.num_nos = 0
        self.num_arestas = 0
        self.grafo = nx.Graph()

    def adicionar_no(self, node):
        if node in self.lista_adj:
            print(f"AVISO: No {node} já existe")
            return
        self.lista_adj[node] = {}
        self.num_nos += 1

    def adicionar_aresta(self, no1, no2, peso):
        if no1 not in self.lista_adj:
            self.adicionar_no(no1)
        if no2 not in self.lista_adj:
            self.adicionar_no(no2)

        self.lista_adj[no1][no2] = peso
        self.lista_adj[no2][no1] = peso
        self.num_arestas += 1

    def adicionar_nos(self, nos):
        for no in nos:
            self.adicionar_no(no)

    def adicionar_aresta_bidimensional(self, no1, no2, peso):
        self.adicionar_aresta(no1, no2, peso)
        self.adicionar_aresta(no2, no1, peso)

    def remove_aresta(self, no1, no2):
        try:
            peso = self.lista_adj[no1].pop(no2)
            self.lista_adj[no2].pop(no1)
            self.num_arestas -= 1
            print(f"Removida a aresta {no1} -> {no2} com peso {peso}")
        except KeyError:
            print(f"WARN: Aresta {no1} -> {no2} não existe")

    def remove_no(self, no):
        if no in self.lista_adj:
            for no2 in self.lista_adj[no]:
                self.lista_adj[no2].pop(no)
                self.num_arestas -= 1
            self.num_arestas -= len(self.lista_adj[no])
            self.num_nos -= 1
            self.lista_adj.pop(no)
            print(f"Removido o nó {no}")
        else:
            print(f"WARN: Nó {no} não existe")

    def __str__(self):
        saida = ""
        for no in self.lista_adj:
            saida += str(no) + " -> " + str(self.lista_adj[no]) + "\n"
        return saida

    def ler_arquivo(self, nome_arquivo):
        file = open(nome_arquivo, 'r', encoding='utf-8')
        i = 0
        for linha in file:
            i += 1
            if i == 1:
                continue
            #print(f"Linha lida: {linha}") 
            conteudo = linha.strip().split("\t")
            u = conteudo[0]
            v = conteudo[1]
            w = conteudo[2]
        self.adicionar_aresta(u, v, w)
        file.close()
    
    def grafo_resultado_votos_iguais(self, data):
        votos_iguais = defaultdict(int)
        num_nos = set()
        num_arestas = 0
        grafo = GrafoPonderado()

        for i, linha1 in enumerate(data):
            id_votacao1 = linha1[0]
            voto1 = linha1[3]
            deputado1 = linha1[6]
            num_nos.add(deputado1)
            
            for j in range(i + 1, len(data)):
                linha2 = data[j]
                id_votacao2 = linha2[0]
                voto2 = linha2[3]
                deputado2 = linha2[6]
                num_nos.add(deputado2)
                
                if id_votacao1 == id_votacao2 and voto1 == voto2:
                    if (deputado1, deputado2) not in votos_iguais:
                        num_arestas += 1
                    votos_iguais[(deputado1, deputado2)] += 1
        #salvando
        nome_arquivo = 'resultados_votos_iguais.txt'

        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write(f" {len(num_nos)}")
            arquivo.write(f"  {num_arestas}\n")
            for (deputado1, deputado2), contagem in votos_iguais.items():
                arquivo.write(f"{deputado1}  {deputado2} {contagem}\n")



    def calculate_normalized_weight(agreements, votes):
        return agreements / int(votes) 

    def criar_grafo_votacoes_iguais(ano, partido, grafo_saida_txt, threshold):
        nome_arquivo1 = f"graph{ano}.txt"
        nome_arquivo2 = f"politicians{ano}.txt"
        threshold = float(threshold)

        # Lê os dados dos arquivos e os transforma em listas
        with open(nome_arquivo1, "r", encoding="utf-8") as f1:
            data1 = f1.readlines()

        with open(nome_arquivo2, "r", encoding="utf-8") as f2:
            data2 = f2.readlines()

        grafo = nx.Graph()
        max_votes = 0

        with open(nome_arquivo2, "r", encoding="utf-8") as arquivo_politicos:
            for linha in arquivo_politicos:
                nome_politico, partido_politico, _ = linha.strip("[]\n").split(";")
                if not partido or partido_politico in partido:
                    grafo.add_node(nome_politico, partido=partido_politico, votacoes=0)

        with open(nome_arquivo1, "r", encoding="utf-8") as arquivo_grafo:
            for linha in arquivo_grafo:
                deputado1, deputado2, votacao = linha.strip("[]\n").split(";")
                votacao = int(votacao)
                if grafo.has_node(deputado1) and grafo.has_node(deputado2) and votacao > 0:
                    grafo.nodes[deputado1]['votacoes'] += 1
                    grafo.nodes[deputado2]['votacoes'] += 1
                    grafo.add_edge(deputado1, deputado2, votacao=votacao)
                    
        # Calcular e armazenar os pesos normalizados das arestas
        normalized_weights = {}
       
        for node1, node2, data in grafo.edges(data=True):
            for index, linha in enumerate(data2):
                nome, _, votacao = linha.strip().split(";")
                if nome == node1 or nome == node2:
                    votacao = int(votacao)
                    while index + 1 < len(data2):
                        proxima_linha = data2[index + 1]
                        proximo_nome, _, proxima_votacao = proxima_linha.strip().split(";")
                        proxima_votacao = int(proxima_votacao)
                        if proximo_nome == node1 or proximo_nome == node2:
                            voto = proxima_votacao
                            if votacao <= proxima_votacao:
                                votacao = votacao
                            else:
                                votacao = proxima_votacao
                        index += 1           
                    max_votos = votacao
                    votacao = data['votacao']
                    normalized_weight = GrafoPonderado.calculate_normalized_weight(votacao, max_votos)
                    if normalized_weight >= threshold:
                        #inversao = 1 - normalized_weight
                        normalized_weights[(node1, node2)] = normalized_weight #inversao
                break
        # Escrever os resultados formatados no arquivo de saída
        with open(grafo_saida_txt, "w", encoding="utf-8") as arquivo_saida:         
            for (dep1, dep2), weight in normalized_weights.items():
                arquivo_saida.write(f"{dep1};{dep2} {weight:.3f}\n")