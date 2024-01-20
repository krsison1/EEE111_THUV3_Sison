from GroceryListDb import GroceryListDb
from GroceryListGuiTk import GroceryListGuiTk

def main():
    db = GroceryListDb(init=False, dbName='GroceryList.csv')
    app = GroceryListGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()