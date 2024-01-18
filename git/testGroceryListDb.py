import os
import unittest
import json
import csv

from GroceryDbSqlite import GroceryListDbSqlite

class TestGroceryListDb(unittest.TestCase):

    def setUp(self):
        self.db_name = 'test_GroceryListDbSql.db'
        self.db = GroceryListDbSqlite(dbName=self.db_name)

    def tearDown(self):
        os.remove(self.db_name)

    def test_create_table(self):
        self.db.create_table()
        self.assertTrue(os.path.exists(self.db_name))

    def test_insert_fetch_items(self):
        items = [
            ('Apples', '5', 'Fruits', 'High', 'Pending'),
            ('Milk', '2 gallons', 'Dairy', 'Medium', 'Bought')
        ]
        for item in items:
            self.db.insert_item(*item)

        fetched_items = self.db.fetch_items()
        self.assertEqual(fetched_items, items)

    def test_update_item(self):
        self.db.insert_item('Bread', '1 loaf', 'Bakery', 'Low', 'Pending')
        self.db.update_item('2 loaves', 'Grains', 'Medium', 'Bought', 'Bread')

        updated_item = self.db.fetch_items()[0]
        self.assertEqual(updated_item, ('Bread', '2 loaves', 'Grains', 'Medium', 'Bought'))

    def test_delete_item(self):
        self.db.insert_item('Banana', '3', 'Fruits', 'High', 'Pending')
        self.db.delete_item('Banana')

        self.assertFalse(self.db.item_exists('Banana'))
        self.assertEqual(self.db.fetch_items(), [])

    def test_export_csv(self):
        self.db.insert_item('Eggs', '1 dozen', 'Dairy', 'High', 'Pending')
        self.db.export_csv()

        with open(self.db.csvFile, 'r') as filehandle:
            content = filehandle.read()
            self.assertEqual(content, 'Eggs,1 dozen,Dairy,High,Pending\n')

    def test_export_json(self):
        self.db.insert_item('Cheese', '1 block', 'Dairy', 'Medium', 'Bought')
        self.db.export_json()

        with open(self.db.jsonFile, 'r') as filehandle:
            data = json.load(filehandle)
            self.assertEqual(data, [{'item': 'Cheese', 'qty': '1 block', 'category': 'Dairy', 'urgency': 'Medium', 'status': 'Bought'}])

    def test_import_csv(self):
        test_csv_file = 'test_data.csv'
        with open(test_csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['item', 'qty', 'category', 'urgency', 'status'])
            writer.writerow(['Bread', '2 loaves', 'Grains', 'Medium', 'Bought'])
            writer.writerow(['Tomatoes', '3', 'Produce', 'High', 'Pending'])

        self.db.import_csv(test_csv_file)

        fetched_items = self.db.fetch_items()
        expected_items = [
            ('Bread', '2 loaves', 'Grains', 'Medium', 'Bought'),
            ('Tomatoes', '3', 'Produce', 'High', 'Pending')
        ]
        self.assertEqual(fetched_items, expected_items)

        os.remove(test_csv_file)

if __name__ == '__main__':
    unittest.main()
