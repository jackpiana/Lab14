from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():
    def __init__(self):
        pass



    @staticmethod
    def getter_stores():
        """
        usa unpacking di dizionari per creare oggetti di classe avente tutte le righe di data tabella
        return: lista di oggetti
        """
        conn = DBConnect.get_connection()
        result = {}
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor(dictionary=True)
            query = """select *
                        from stores
                        """
            cursor.execute(query)
            for row in cursor:
                result[row["store_id"]] = (Store(**row))  #**row è un operatore di unpacking (espansione) di un dizionario. nb: serve che tutti i nomi degli attributi combacino
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def getter_orders_store(store_id):   #NODES
        """
        usa unpacking di dizionari per creare oggetti di classe avente tutte le righe di data tabella
        return: lista di oggetti
        """
        conn = DBConnect.get_connection()
        result = {}
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor(dictionary=True)
            query = """select *
                        from orders
                        where store_id = %s
                        """
            cursor.execute(query, (store_id,))
            for row in cursor:
                result[row["order_id"]] = (Order(**row))  #**row è un operatore di unpacking (espansione) di un dizionario. nb: serve che tutti i nomi degli attributi combacino
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def get_edges_store(store_id, k):
        """
        :return: lista di tuple contenenti gli attributi selezionati dalla query
        """
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """
                    select t1.order_id, t2.order_id, sum(t1.quantity+t2.quantity) as "weight"
                    from (select o.order_id, o.order_date, i.quantity, o.store_id 
                    from orders o, order_items i 
                    where o.store_id = %s
                    and o.order_id = i.order_id) t1,
                    (select o.order_id, o.order_date, i.quantity, o.store_id
                    from orders o, order_items i 
                    where o.store_id = %s
                    and o.order_id = i.order_id) t2
                    where (DATEDIFF(t1.order_date, t2.order_date)) < %s
                    and (DATEDIFF(t1.order_date, t2.order_date)) > 0
                    and t1.order_id != t2.order_id 
                    and t1.store_id = t2.store_id
                    group by t1.order_id, t2.order_id
                    """
            cursor.execute(query, (store_id, store_id, k))
            for row in cursor:
                result.append(row)  # row è una tupla contenente id nodo1, id nodo2
            cursor.close()
            conn.close()
        return result

if __name__ == '__main__':
    DAO = DAO()
    print(DAO.getter_stores())
