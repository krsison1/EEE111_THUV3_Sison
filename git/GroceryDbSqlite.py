'''
This is the interface to an SQLite Database
'''
import json
import sqlite3
import csv
from tkinter import filedialog

class GroceryListDbSqlite:
    def __init__(self, dbName='GroceryList.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.jsonFile = self.dbName.replace('.db','.json')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS GroceryItems (
                item TEXT PRIMARY KEY,
                qty TEXT,
                category TEXT,
                urgency TEXT,
                status TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees (
                    item TEXT PRIMARY KEY,
                    qty TEXT,
                    category TEXT,
                    urgency TEXT,
                    status TEXT)''')
        self.commit_close()

    def fetch_items(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM GroceryItems')
        items = self.cursor.fetchall()
        self.conn.close()
        return items

    def insert_item(self, item, qty, category, urgency, status):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO GroceryItems (item, qty, urgency, category, status) VALUES (?, ?, ?, ?, ?)',
                           (item, qty, urgency, category, status))
        self.commit_close()

    def delete_item(self, item):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM GroceryItems WHERE item = ?', (item,))
        self.commit_close()

    def update_item(self, new_qty, new_category, new_urgency, new_status, item):
        self.connect_cursor()
        self.cursor.execute('UPDATE GroceryItems SET qty = ?, category = ?, urgency = ?, status = ? WHERE item = ?',
                    (new_qty, new_category, new_urgency, new_status, item))
        self.commit_close()

    def item_exists(self, item):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM GroceryItems WHERE item = ?', (item,))
        result = self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            items = self.fetch_items()
            for entry in items:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")
    
    def export_json(self):
        with open(self.jsonFile, "w") as filehandle:
            items = self.fetch_items()
            data = [dict(zip(('item', 'qty', 'category', 'urgency', 'status'), item)) for item in items]
            json.dump(data, filehandle, indent=8)

    def import_csv(self):
        path = filedialog.askopenfilename(title="Select CSV File", filetypes=(("CSV Files", "*.csv"),))
        if path:
            with open(path, 'r') as csvfile:
                decoder = csv.reader(csvfile)
                header = next(decoder)
                for row in decoder:
                    item, qty, category, urgency, status = row
                    if not self.item_exists(item):
                        self.insert_item(item, qty, category, urgency, status)