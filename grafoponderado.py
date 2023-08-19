from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
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


    def calculate_normalized_weight(valor, votes):
        return valor / int(votes) 

    def criar_grafo_votacoes_iguais(ano, partido, grafo_saida_txt, threshold, png_output_filename, heatmap_output_filename, grafo_output_filename):
        nome_arquivo1 = f"graph{ano}.txt"
        nome_arquivo2 = f"politicians{ano}.txt"
        threshold = float(threshold)

        
        with open(nome_arquivo1, "r", encoding="utf-8") as f1:
            data1 = f1.readlines()

        with open(nome_arquivo2, "r", encoding="utf-8") as f2:
            data2 = f2.readlines()

        grafo = nx.Graph()
        min_votes = 0

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
                    
       
        normalized_weights = {}
        grafo_novo = nx.Graph()
       
        for node1, node2, data in grafo.edges(data=True):
            partido_node1 = grafo.nodes[node1]['partido']
            partido_node2 = grafo.nodes[node2]['partido']
            
            for index, linha in enumerate(data2):
                nome, partido, votacao = linha.strip().split(";")
                if (nome == node1 and partido == partido_node1) or (nome == node2 and partido == partido_node2):
                    votacao = int(votacao)
                    while index + 1 < len(data2):
                        proxima_linha = data2[index + 1]
                        proximo_nome, proximo_partido, proxima_votacao = proxima_linha.strip().split(";")
                        proxima_votacao = int(proxima_votacao)
                        if (proximo_nome == node1 and proximo_partido == partido_node1) or (proximo_nome == node2 and proximo_partido == partido_node2):
                            if votacao <= proxima_votacao:
                                votacao = votacao
                            else:
                                votacao = proxima_votacao
                        index += 1
                    
                    min_votes = votacao
                    votacao = data['votacao']
                    normalized_weight = GrafoPonderado.calculate_normalized_weight(votacao, min_votes)
                    if normalized_weight >= threshold:
                        #inversao = 1 - normalized_weight
                        normalized_weights[(node1, node2)] = normalized_weight
                        grafo_novo.add_edge(node1, node2, weight=normalized_weight)
                       
                        
       
        with open(grafo_saida_txt, "w", encoding="utf-8") as arquivo_saida:         
            for (dep1, dep2), weight in normalized_weights.items():
                arquivo_saida.write(f"{dep1};{dep2} {weight:.3f}\n")

        #GRAFO BETWEENNESS 
        betweenness_scores = nx.betweenness_centrality(grafo_novo)
        sorted_nodes = sorted(betweenness_scores, key=lambda x: betweenness_scores[x])
        deputados = sorted_nodes
        scores = [betweenness_scores[node] for node in sorted_nodes]
        plt.figure(figsize=(20, 10))
        plt.bar(deputados, scores)
        plt.xlabel('Deputados')
        plt.ylabel('Betweenness')
        plt.title('Medida de Centralidade - Betweenness')
        plt.xticks(rotation=45, ha='right', fontsize=5)
        plt.tight_layout()
        plt.gcf().subplots_adjust(bottom=0.20)
        plt.savefig(png_output_filename)
        plt.show()
        
        #HEATMAP
        adjacency_matrix = nx.to_numpy_array(grafo_novo, weight='weight')  
        correlation_matrix = np.corrcoef(adjacency_matrix)  
        plt.figure(figsize=(20, 10)) 
        plt.imshow(correlation_matrix, cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title('Heatmap - Correlação entre Deputados')
        plt.xticks(range(len(deputados)), deputados, rotation=45, ha='right', fontsize=5)
        plt.yticks(range(len(deputados)), deputados[::-1], fontsize=5)  
        plt.subplots_adjust(left=0.25, right=0.95, top=0.95, bottom=0.2)  
        plt.tight_layout()   
        plt.savefig(heatmap_output_filename)
        plt.show()

        #GRAFO  
        central_node = max(betweenness_scores, key=betweenness_scores.get)        
        plt.figure(figsize=(10, 6))  
        pos = nx.spring_layout(grafo_novo)
        nx.draw_networkx(grafo_novo, pos, with_labels=True, font_size=5, node_size=100)     
        nx.draw_networkx_nodes(grafo_novo, pos, nodelist=[central_node], node_color='red', node_size=150)
        plt.title(f'Grafo de Relações de Votos entre Deputados com Ponto Central Marcado')
        plt.tight_layout() 
        plt.savefig(grafo_output_filename)
        plt.show()

    #Depois vou fazer a inversao de pesos separado      
    # def grafo_inversao_de_pesos(ano, partido, grafo_saida_txt, threshold):
    #     nome_arquivo1 = f"graph{ano}.txt"
    #     nome_arquivo2 = f"politicians{ano}.txt"
    #     threshold = float(threshold)

    #     # Lê os dados dos arquivos e os transforma em listas
    #     with open(nome_arquivo1, "r", encoding="utf-8") as f1:
    #         data1 = f1.readlines()

    #     with open(nome_arquivo2, "r", encoding="utf-8") as f2:
    #         data2 = f2.readlines()

    #     grafo = nx.Graph()
    #     min_votos = 0

    #     with open(nome_arquivo2, "r", encoding="utf-8") as arquivo_politicos:
    #         for linha in arquivo_politicos:
    #             nome_politico, partido_politico, _ = linha.strip("[]\n").split(";")
    #             if not partido or partido_politico in partido:
    #                 grafo.add_node(nome_politico, partido=partido_politico, votacoes=0)

    #     with open(nome_arquivo1, "r", encoding="utf-8") as arquivo_grafo:
    #         for linha in arquivo_grafo:
    #             deputado1, deputado2, votacao = linha.strip("[]\n").split(";")
    #             votacao = int(votacao)
    #             if grafo.has_node(deputado1) and grafo.has_node(deputado2) and votacao > 0:
    #                 grafo.nodes[deputado1]['votacoes'] += 1
    #                 grafo.nodes[deputado2]['votacoes'] += 1
    #                 grafo.add_edge(deputado1, deputado2, votacao=votacao)
                    
        
    #     normalizacao = {}
        
       
    #     for node1, node2, data in grafo.edges(data=True):
    #         partido_node1 = grafo.nodes[node1]['partido']
    #         partido_node2 = grafo.nodes[node2]['partido']
            
    #         for index, linha in enumerate(data2):
    #             nome, partido, votacao = linha.strip().split(";")
    #             if (nome == node1 and partido == partido_node1) or (nome == node2 and partido == partido_node2):
    #                 votacao = int(votacao)
    #                 while index + 1 < len(data2):
    #                     proxima_linha = data2[index + 1]
    #                     proximo_nome, proximo_partido, proxima_votacao = proxima_linha.strip().split(";")
    #                     proxima_votacao = int(proxima_votacao)
    #                     if (proximo_nome == node1 and proximo_partido == partido_node1) or (proximo_nome == node2 and proximo_partido == partido_node2):
    #                         if votacao <= proxima_votacao:
    #                             votacao = votacao
    #                         else:
    #                             votacao = proxima_votacao
    #                     index += 1
                    
    #                 min_votos = votacao
    #                 votacao = data['votacao']
    #                 normalizacao = GrafoPonderado.calculate_normalized_weight(votacao, min_votos)
    #                 if normalizacao >= threshold:
    #                     inversao = 1 - normalizacao
    #                     normalizacao[(node1, node2)] = inversao
                    
       
    #     with open(grafo_saida_txt, "w", encoding="utf-8") as arquivo_saida:         
    #         for (dep1, dep2), weight in normalized_weights.items():
    #             arquivo_saida.write(f"{dep1};{dep2} {weight:.3f}\n")