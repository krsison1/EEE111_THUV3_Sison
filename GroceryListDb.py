from GroceryListEntry import GroceryListEntry
import csv
import json

class GroceryListDb:
    def __init__(self, init=False, dbName='GroceryList.csv'):
        self.dbName = dbName
        self.entries = []

    def fetch_items(self):
        return [(entry.item, entry.qty, entry.category, entry.urgency, entry.status) for entry in self.entries]

    def insert_item(self, item, qty, category, urgency, status):
        newEntry = GroceryListEntry(item=item, qty=qty, category=category, urgency=urgency, status=status)
        self.entries.append(newEntry)

    def delete_item(self, item):
        self.entries = [entry for entry in self.entries if entry.item != item]

    def update_item(self, new_qty, new_category, new_urgency, new_status, item):
        for entry in self.entries:
            if entry.item == item:
                entry.qty = new_qty
                entry.category = new_category
                entry.urgency = new_urgency
                entry.status = new_status
                break

    def export_csv(self):
        with open(self.dbName, 'w', newline='') as csvfile:
            filemaker = csv.writer(csvfile)
            filemaker.writerow(['item', 'qty', 'category', 'urgency', 'status'])
            for entry in self.entries:
                filemaker.writerow([entry.item, entry.qty, entry.category, entry.urgency, entry.status])

    def item_exists(self, item):
        return any(entry.item == item for entry in self.entries)

    def export_json(self):
        with open(f"{self.dbName.replace('.csv', '.json')}", 'w') as jsonfile:
            data = [entry.__dict__ for entry in self.entries]
            json.dump(data, jsonfile, indent=8)   