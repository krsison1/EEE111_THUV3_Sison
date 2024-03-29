import csv
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox, filedialog, Tk, Label
from GroceryDbSqlite import GroceryListDbSqlite
from PIL import Image, ImageTk

class GroceryListGuiTk(Tk):

    def __init__(self, dataBase=GroceryListDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        imgsrc = 'logo.jpg'
        img = Image.open(imgsrc)
        imgres = img.resize((150, 150), Image.Resampling(3))
        imgtk = ImageTk.PhotoImage(imgres)

        self.logo = Label(self, image=imgtk, bd=0)
        self.logo.photo = imgtk
        self.logo.place(x=1275, y=425)

        self.title('Grocery List Manager')
        self.geometry('1500x600')
        self.config(bg='#eaeaea')
        self.resizable(False, False)

        self.font1 = ('Arial', 20, 'bold')
        self.font2 = ('Arial', 12, 'bold')

        # Data Entry Form
        # 'Item' Label and Entry Widgets
        self.item_label = self.newCtkLabel('Item') 
        self.item_label.place(x=100, y=450)
        self.item_entryVar = StringVar() 
        self.item_entry = self.newCtkEntry(entryVariable=self.item_entryVar)
        self.item_entry.place(x=150, y=450)

        # 'Qty' Label and Entry Widgets
        self.qty_label = self.newCtkLabel('Qty')
        self.qty_label.place(x=100, y=500)
        self.qty_entryVar = StringVar()  
        self.qty_entry = self.newCtkEntry(entryVariable=self.qty_entryVar) 
        self.qty_entry.place(x=150, y=500)

        # 'Category' Label and Combo Box Widgets
        self.category_label = self.newCtkLabel('Category') 
        self.category_label.place(x=480, y=450)
        self.category_cboxVar = StringVar()  
        self.category_cboxOptions = ['Grains', 'Dairy', 'Produce', 'Cans/Jars', 'Meat', 'Condiments', 'Drinks', 'Household'] 
        self.category_cbox = self.newCtkComboBox(options=self.category_cboxOptions, 
                                    entryVariable=self.category_cboxVar) 
        self.category_cbox.place(x=550, y=450)

        # 'Urgency' Label and Combo Box Widgets
        self.urgency_label = self.newCtkLabel('Urgency')
        self.urgency_label.place(x=480, y=500)
        self.urgency_cboxVar = StringVar()
        self.urgency_cboxOptions = ['Urgent', 'Not Urgent']
        self.urgency_cbox = self.newCtkComboBox(options=self.urgency_cboxOptions, 
                                    entryVariable=self.urgency_cboxVar)
        self.urgency_cbox.place(x=550, y=500)

        # 'Status' Label and Combo Box Widgets
        self.status_label = self.newCtkLabel('Status') 
        self.status_label.place(x=850, y=475)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['Available', 'Unavailable']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=900, y=475)

        self.add_button = self.newCtkButton(text='Add Item',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=1230,y=20)

        self.new_button = self.newCtkButton(text='New Item',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=1230,y=80)

        self.update_button = self.newCtkButton(text='Update Item',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=1230,y=140)

        self.delete_button = self.newCtkButton(text='Delete Item',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404')
        self.delete_button.place(x=1230,y=200)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=1230,y=260)

        self.export_button = self.newCtkButton(text='Export to JSON',
                                               onClickHandler=self.export_to_json)
        self.export_button.place(x=1230,y=320)

        self.import_button = self.newCtkButton(text='Import CSV File',
                                               onClickHandler=self.import_to_csv)
        self.import_button.place(x=1230,y=380)        

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#000',
                        background='#e7e7e7',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('Item', 'Qty', 'Category', 'Urgency', 'Status')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Item', anchor=tk.CENTER, width=150)
        self.tree.column('Qty', anchor=tk.CENTER, width=10)
        self.tree.column('Category', anchor=tk.CENTER, width=150)
        self.tree.column('Urgency', anchor=tk.CENTER, width=10)
        self.tree.column('Status', anchor=tk.CENTER, width=150)

        self.tree.heading('Item', text='Item')
        self.tree.heading('Qty', text='Qty')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Urgency', text='Urgency')
        self.tree.heading('Status', text='Status')

        self.tree.place(x=100, y=20, width=1100, height=400)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#161C25'

        widget = ttk.Label(self, 
                        text=text)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label', entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25

        widget = ttk.Entry(self, textvariable=entryVariable, width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25
        widget_Options=options

        widget = ttk.Combobox(self, 
                              textvariable=entryVariable,
                              width=widget_Width)
        
        # set default value to 1st option
        widget['values'] = tuple(options)
        widget.current(1)
        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=25
        widget_Function=onClickHandler

        widget = ttk.Button(self,
                            text=text,
                            command=widget_Function,
                            width=widget_Width)
       
        return widget
    
    # Handles
    def add_to_treeview(self):
        items = self.db.fetch_items() 
        self.tree.delete(*self.tree.get_children())
        for item in items:
            print(item)
            self.tree.insert('', END, values=item)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.item_entryVar.set('Item')
        self.qty_entryVar.set('Quantity')
        self.category_cboxVar.set('Dairy')
        self.urgency_cboxVar.set('Urgent')
        self.status_cboxVar.set('Available') 

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.item_entryVar.set(row[0])
            self.qty_entryVar.set(row[1])
            self.category_cboxVar.set(row[2]) 
            self.urgency_cboxVar.set(row[3])
            self.status_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        item=self.item_entryVar.get()
        qty=self.qty_entryVar.get()
        category=self.category_cboxVar.get()
        urgency=self.urgency_cboxVar.get()
        status=self.status_cboxVar.get()

        if not (item and qty and category and urgency and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.item_exists(item):
            messagebox.showerror('Error', 'Item already exists')
        else:
            self.db.insert_item(item, qty, category, urgency, status)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an item to delete')
        else:
            item = self.item_entryVar.get()
            self.db.delete_item(item)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an Item to update')
        else:
            item=self.item_entryVar.get()
            qty=self.qty_entryVar.get()
            category=self.category_cboxVar.get()
            urgency=self.urgency_cboxVar.get()
            status=self.status_cboxVar.get()
            self.db.update_item(qty, category, urgency, status, item)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')

    def export_to_json(self):
        self.db.export_json()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.json')

    def import_to_csv(self):
        self.db.import_csv()
        self.add_to_treeview()
        messagebox.showinfo('Success','Data imported from CSV')



