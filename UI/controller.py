import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.storeId = None
        self.k = None
        self.node = None

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        self._view._ddNode.options.clear()

        self._view.update_page()

        self.read_casellaTesto_intero()

        if self.storeId is not None and self.k is not None:
            self._model.build_graph(self.storeId, self.k)

        self._view.txt_result.controls.append(ft.Text(self._model.grafo))
        self.fill_dropdownNodi()

        self._view.update_page()

    def handleCerca(self, e):
        bestScore, longestPath = self._model.longest_path(self.node)
        self._view.txt_result.controls.append(ft.Text(f"longest path partendo da {self.node}"
                                                      f"\nlunghezza: {bestScore}"
                                                      f"\n cammino:"))
        for n in longestPath:
            self._view.txt_result.controls.append(ft.Text(n))

        self._view.update_page()


    def handleRicorsione(self, e):
        bestScore, bestPath = self._model.best_path(self.node)
        self._view.txt_result.controls.append(ft.Text(f"heaviest path partendo da {self.node}"
                                                      f"\npeso totale: {bestScore}"
                                                      f"\n cammino:"))
        for n in bestPath:
            self._view.txt_result.controls.append(ft.Text(n))

        self._view.update_page()


    #DROPDOWN
    def fill_dropdown(self):
        lista_opzioni = DAO.getter_storesId()
        for o in lista_opzioni:
            self._view._ddStore.options.append(ft.dropdown.Option(key= o,
                                                                  text=o,
                                                                  data= o,
                                                                  on_click=self.read_dropdownStore))

    def fill_dropdownNodi(self):
        lista_opzioni = list(self._model.grafo.nodes())
        for o in lista_opzioni:
            self._view._ddNode.options.append(ft.dropdown.Option(key= o,
                                                                  text=o,
                                                                  data= o,
                                                                  on_click=self.read_dropdownNodi))


    def read_dropdownNodi(self, e):
        self.node = e.control.data
        self._view._btnCerca.disabled = False
        print(f"nodo dd: {self.node} - {type(self.node)}")
        self._view.update_page()


    def read_dropdownStore(self, e):
        self.storeId = e.control.data
        print(f"store dd: {self.storeId} - {type(self.storeId)}")



    def read_casellaTesto_intero(self):
        valore = self._view._txtIntK.value
        try:
            k = int(valore)
            self.k = k
            print(f"k: {self.k} {type(self.k)}")
            return True
        except ValueError:
            self._view.create_alert("inserire valore valido")
            return False
