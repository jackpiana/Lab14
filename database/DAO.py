from database.DB_connect import DBConnect
from model.order import Order


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getter_storesId():
        """
        :return: lista di tuple contenenti gli attributi selezionati dalla query
        """
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """select distinct store_id 
                        from stores s 
                    """
            cursor.execute(query)
            for row in cursor:
                result.append(row[0]) #row è una tupla contenente tutti gli attributi selezionati dalla query
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def getter_mapNodes(storeId):
        """
        usa unpacking di dizionari per creare oggetti di classe avente tutte le righe di data tabella
        return: mappa key= id, value= oggetto
        """
        conn = DBConnect.get_connection()
        result = {}
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor(dictionary=True)
            query = """select *
                from orders o
                where o.store_id = %s

                            """
            cursor.execute(query, (storeId,))
            for row in cursor:
                result[row["order_id"]] = (Order(**row))  # **row è un operatore di unpacking (espansione) di un dizionario. nb: serve che tutti i nomi degli attributi combacino
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def getter_edges(storeId, k):
        """
        :return: lista di tuple contenenti nid1, nid2, weight
        """
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """
                    select o1.order_id, o2.order_id, sum(oi1.quantity) + sum(oi2.quantity) as 'weight'
                    from orders o1, orders o2, order_items oi1, order_items oi2
                    where o1.order_id = oi1.order_id
                    and o2.order_id = oi2.order_id
                    and o1.store_id = o2.store_id
                    and o1.store_id = %s
                    and o1.order_date > o2.order_date 
                    and datediff(o1.order_date, o2.order_date) < %s
                    group by o1.order_id, o2.order_id
                    order by weight desc
                    """
            cursor.execute(query, (storeId, k))
            for row in cursor:
                result.append(row) #row è una tupla contenente nid1, nid2, weight
            cursor.close()
            conn.close()
        return result
