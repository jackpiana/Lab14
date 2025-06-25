import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.selectedStore = None
        self.selectedK = None
        self.selectedNode = None


    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        self.read_k()
        self._view.show_loading_bar()
        self._model.buildGrafo(self.selectedStore, self.selectedK)
        self._view.remove_loading_bar()
        self._view.txt_result.controls.append(ft.Text(f"{self._model.grafo}"))
        self.fill_dropdown_nodes()
        self._view.update()


    def handleCerca(self, e):
        print(self.selectedNode, type(self.selectedNode))
        lp = self._model.longest_path(self.selectedNode)
        if lp is None:
            return
        for n in lp:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update()

    def handleRicorsione(self, e):
        pass

    def fill_dropdown(self):
        lista_opzioni = DAO.getter_stores().values()
        for o in lista_opzioni:
            self._view._ddStore.options.append(ft.dropdown.Option(key=o,
                                                                  text=o,
                                                                  data=o,
                                                                  on_click=self.read_dropdown))

    def read_dropdown(self, e):
        self.selectedStore = e.control.data
        print(f"valore letto: {self.selectedStore} - {type(self.selectedStore)}")

    def fill_dropdown_nodes(self):
        self._view._ddNode.options.clear()
        lista_opzioni = list(self._model.grafo.nodes)
        for o in lista_opzioni:
            self._view._ddNode.options.append(ft.dropdown.Option(key=o,
                                                                  text=o,
                                                                  data=o,
                                                                  on_click=self.read_dropdown_nodes))

    def read_dropdown_nodes(self, e):
        self.selectedNode = e.control.data
        print(f"valore letto: {self.selectedNode} - {type(self.selectedNode)}")


    def read_k(self):
        intero = self._view._txtIntK.value
        try:
            intero = int(intero)
            self.selectedK = intero
            print(f"valore selezionato: {self.selectedK} {type(intero)}")
            return True
        except ValueError:
            self._view.create_alert("inserire valore valido")
            return False
