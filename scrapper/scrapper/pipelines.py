# Define your item pipelines here
from itemadapter import ItemAdapter
import mysql.connector


class ScrapperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name == 'utilities':
                values = adapter.get(field_name)
                if isinstance(values, list):  # Vérifie que c'est bien une liste
                    adapter[field_name] = [value.strip().lower() for value in values if isinstance(value, str)]  

        # Nettoyage du prix
        price_string = adapter.get('price')
        if isinstance(price_string, str):  
            try:
                adapter['price'] = int(price_string.split('/')[0].replace('$', '').replace(',', '').strip())  
            except ValueError:
                adapter['price'] = None  # En cas d'erreur de conversion
        
        # Nettoyage de la surface
        area_string = adapter.get('area')
        if isinstance(area_string, str):  
            try:
                adapter['area'] = int(area_string.split(' ')[0])  
            except ValueError:
                adapter['area'] = None  # Si conversion échoue
        
        
        adresse = adapter.get('adresse')
        adapter['adresse'] = adresse
        
        return item

class ResetMysqlPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='user1',
            password='Arcep@1990',
            database='cocohome'
        )
        self.cur = self.conn.cursor()

        # Suppression et création des tables
        self.cur.execute("DROP TABLE IF EXISTS houses_utilities, houses, utilities")

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS houses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                price INT,
                area INT,
                adresse TEXT
            )
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS utilities (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(45) UNIQUE NOT NULL
            )
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS houses_utilities (
                house_id INT,
                utility_id INT,
                PRIMARY KEY (house_id, utility_id),
                FOREIGN KEY (house_id) REFERENCES houses(id) ON DELETE CASCADE,
                FOREIGN KEY (utility_id) REFERENCES utilities(id) ON DELETE CASCADE
            )
        """)

        self.conn.commit()
    
class SaveToMysqlPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='user1',
            password='Arcep@1990',
            database='cocohome'
        )
        self.cur = self.conn.cursor()

        # Désactiver les clés étrangères et vider les tables
        self.cur.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.cur.execute("TRUNCATE TABLE houses_utilities")
        self.cur.execute("TRUNCATE TABLE utilities")
        self.cur.execute("TRUNCATE TABLE houses")
        self.cur.execute("SET FOREIGN_KEY_CHECKS = 1")
        self.conn.commit()  # ✅ Toujours commit après un DELETE

    def process_item(self, item, spider):
        title = item.get('title', 'Unknown')
        price = item.get('price', None)
        area = item.get('area', None)
        adresse = item.get('adresse', '')
        utilities = item.get('utilities', [])

        adresse_str = ', '.join(adresse) if isinstance(adresse, list) else str(adresse)

        # 🔹 Insérer la maison
        self.cur.execute("""
            INSERT INTO houses (title, price, area, adresse) 
            VALUES (%s, %s, %s, %s)
        """, (title, price, area, adresse_str))
        house_id = self.cur.lastrowid

        utilities_ids = []
        for utility in utilities:
            self.cur.execute("SELECT id FROM utilities WHERE name = %s", (utility,))
            result = self.cur.fetchone()

            if result:
                utility_id = result[0]
            else:
                self.cur.execute("INSERT INTO utilities (name) VALUES (%s)", (utility,))
                self.conn.commit()  # ✅ Commit immédiatement pour être sûr
                utility_id = self.cur.lastrowid

                if utility_id is None:
                    raise Exception(f"Erreur lors de l'insertion de {utility}")

            utilities_ids.append((house_id, utility_id))

        # 🔹 Insérer les relations maison ↔ utilities
        if utilities_ids:
            self.cur.executemany("""
                INSERT INTO houses_utilities (house_id, utility_id) 
                VALUES (%s, %s)
            """, utilities_ids)
            self.conn.commit()  # ✅ Commit après un executemany()

        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
