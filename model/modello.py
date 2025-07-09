import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.bestScore = 0
        self.longestPath = []

        self.pesoAttuale = 1000000

        self.bestScore2 = 0
        self.bestPath = []

    def build_graph(self, storeId, k):
        self.grafo.clear()

        nodesMap = DAO.getter_mapNodes(storeId)
        nodes = nodesMap.values()
        self.grafo.add_nodes_from(nodes)
        print(self.grafo)


        edgesId = DAO.getter_edges(storeId, k)
        for edge in edgesId:
            if edge[0] in nodesMap.keys() and edge[1] in nodesMap.keys():
                self.grafo.add_edge(nodesMap[edge[0]], nodesMap[edge[1]], weight= int(edge[2]))

        print(self.grafo)

    def longest_path(self, node):
        self.ricorsione([node])
        return self.bestScore, self.longestPath

    def ricorsione(self, parziale):
        rimanenti = self.rimanenti(parziale)
        if not rimanenti:
            print(parziale)
            self.score(parziale)
        else:
            rimanenti = rimanenti.copy()
            for n in rimanenti:
                parziale.append(n)
                parziale = parziale.copy()
                self.ricorsione(parziale)
                parziale.pop()


    def rimanenti(self, parziale):
        rimanenti = []
        ns = parziale[-1]
        vicini = self.grafo.neighbors(ns)
        for vicino in vicini:
            if vicino not in parziale:
                rimanenti.append(vicino)
        return rimanenti


    def score(self, parziale):
        score = len(parziale)
        if score > self.bestScore:
            print(score)
            self.bestScore = score
            self.longestPath = parziale.copy()


    def best_path(self, node):
        self.pesoAttuale = 1000000
        self.bestScore2 = 0
        self.bestPath = []

        self.ricorsione2([node])
        return self.bestScore2, self.bestPath


    def ricorsione2(self, parziale):
        rimanenti = self.rimanenti2(parziale)
        if not rimanenti:
            print(parziale)
            self.score2(parziale)
        else:
            rimanenti = rimanenti.copy()
            for n in rimanenti:
                parziale.append(n)
                parziale = parziale.copy()
                self.ricorsione2(parziale)
                parziale.pop()

    def rimanenti2(self, parziale):
        rimanenti = []
        ns = parziale[-1]
        vicini = self.grafo.neighbors(ns)
        if len(parziale) > 1:
            self.pesoAttuale = self.grafo.edges[parziale[-2], ns]['weight']

        for vicino in vicini:
            pesoArco = self.grafo[ns][vicino]['weight']
            if pesoArco < self.pesoAttuale:
                rimanenti.append(vicino)
        return rimanenti


    def score2(self, parziale):
        score = 0
        for i in range(len(parziale)-1):
            n1 = parziale[i]
            n2 = parziale[i+1]
            score += self.grafo[n1][n2]['weight']
        if score > self.bestScore2:
            self.bestScore2 = score
            self.bestPath = parziale.copy()


if __name__ == "__main__":
    m = Model()
    m.build_graph(2, 5)

