from GroceryListDb import GroceryListDb
from EmpGuiTk import EmpGuiTk

def main():
    db = GroceryListDb(init=False, dbName='GroceryList.csv')
    app = EmpGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()