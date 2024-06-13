import sqlite3
import time

def show_visits():
    connection = sqlite3.connect("google_bot.db")
    cursor = connection.cursor()

    while True:
        query = """
        SELECT visit.id, visit.collected_on, visit.URL
        FROM visit
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        print("Visits: ")
        for row in rows:
            print(row)

        visit_number = input('Voer visit nummer in om de item te zien: ')

        if visit_number.lower() == "x":
            break

        cursor.execute("SELECT COUNT(*) FROM visit WHERE id = ?", (visit_number,))
        bestaat = cursor.fetchone()[0]   

        if bestaat:

            query = """
            SELECT visit_items.visit_id, visit_items.id, visit_items.name, visit_items.rank
            FROM visit_items
            WHERE visit_items.visit_id = ?  
            """

            cursor.execute(query, (visit_number,))
            items = cursor.fetchall()   

            print("Visit items: ")
            print("VISIT, ID, NAME, RANK")
            for item in items:
                print(item)
            time.sleep(1)

            visit_item = input('Van welk item wil je details weten')

            cursor.execute('SELECT COUNT(*) FROM visit_items WHERE id = ?', (visit_item,))
            bestaat_item = cursor.fetchall()[0]

            if bestaat_item:
                query = """
                SELECT visit_item_info.visit_item_id, visit_item_info.id, visit_item_info.key, visit_item_info.value
                FROM visit_item_info
                WHERE visit_item_info.visit_item_id = ?
                """

                cursor.execute(query, (visit_item,))
                item_details = cursor.fetchall()
                print("Item detail")
                print("VISIT, ID, KEY, VALUE")
                for items in item_details:
                    print(items)
                time.sleep(1)

                stoppen = input("Typ x om te stoppen: ")
                
                if stoppen.lower() == "x":
                    break

        else:
            print("Dit visit nummer bestaat niet")
            time.sleep(1)


if __name__ == "__main__":
    show_visits()




