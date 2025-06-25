import copy
from random import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.bestLunghezza = 0
        self.longestPath = None

    def buildGrafo(self, store, k):
        self.grafo = None
        self.grafo = nx.DiGraph()
        idMapOrders = DAO.getter_orders_store(store.store_id)
        nodes = idMapOrders.values()
        self.grafo.add_nodes_from(nodes)
        edges = DAO.get_edges_store(store.store_id, k)
        for e in edges:
            self.grafo.add_edge(idMapOrders[e[0]], idMapOrders[e[1]], weight=e[2])

    def longest_path(self, node):
        self.bestLunghezza = 0
        succ = list(self.grafo.successors(node))
        print(f"successori: {succ}")
        self.ricorsione_longest_path([], copy.deepcopy(succ))
        return self.longestPath


    def ricorsione_longest_path(self, parziale, successori):
        if successori == []:
            lunghezza = len(parziale)
            if lunghezza > self.bestLunghezza:
                self.bestLunghezza = lunghezza
                print(self.bestLunghezza)
                self.longestPath = copy.deepcopy(parziale)
        else:
            for n in successori:
                parziale = copy.deepcopy(parziale)
                succ = list(self.grafo.successors(n))
                parziale.append(n)
                self.ricorsione_longest_path(parziale, copy.deepcopy(succ))
                parziale.pop()

if __name__ == "__main__":
    m = Model()
    stores = DAO.getter_stores()
    print(stores)
    m.buildGrafo(stores[2], 1)
    print(m.grafo)
    m.longest_path(stores[2])
    print(m.longestPath)
