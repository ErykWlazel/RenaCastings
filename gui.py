from tkinter import *
from tkinter.ttk import Combobox, Treeview, Style
from tkinter.font import BOLD, Font
from typing import Callable
import orm as db
import os
from datetime import datetime
import re


def build_root():
    global root
    root = Tk()
    root.title('GG')            
    root.state('zoomed')
    root.resizable(False, False)
    return root

def build_fonts():
    global big_font
    big_font = Font( family='Helvetica', size=28)

def build_label(container: str, label_text: str, label_font: str):
    stock_label = Label(container, text= label_text, font= label_font)
    stock_label.grid(row = 0, column= 0, sticky= NW)

def build_stock_treeview(root):
    global stock_treeview
    stock_treeview = Treeview(root)
    stock_treeview.grid(row = 1, column = 0)

def build_styles():
    global stock_treeview_style
    stock_treeview_style = Style()
    stock_treeview_style.theme_use('clam')

def build_stock_treeview_columns_with_headings_in_style():
    stock_treeview_style.configure("Treeview", font=(None, 16))
    stock_treeview_style.configure("Treeview.Heading", background= '#D4D4D4', font=(None, 38))

    stock_treeview['columns'] = ('ID', 'article_code', 'serial_number', 'location', 'amount', 'container', 'description', 'date')

    stock_treeview.column("#0", width=0, stretch=NO)
    stock_treeview.heading("ID",text="ID",anchor=W, command= lambda: column_heading_click_sort('stock.id', 0))
    stock_treeview.column('ID', anchor=W, width=60, stretch=NO)
    stock_treeview.heading("article_code",text="Article code",anchor=W, command= lambda: column_heading_click_sort('products.article_code', 1))
    stock_treeview.column('article_code', anchor=W, width=280)
    stock_treeview.heading("serial_number",text="Serial number",anchor=W, command= lambda: column_heading_click_sort('products.serial_code', 2))
    stock_treeview.column('serial_number', anchor=W, width=330)
    stock_treeview.heading("description",text="Description",anchor=W, command= lambda: column_heading_click_sort('products.description', 6))
    stock_treeview.column('description', anchor=W, width=280)
    stock_treeview.heading("amount",text="Amount",anchor=W, command= lambda: column_heading_click_sort('stock.amount', 4))
    stock_treeview.column('amount', anchor=W, width=200)
    stock_treeview.heading("location",text="Location",anchor=W, command= lambda: column_heading_click_sort('locations.location_name', 3))
    stock_treeview.column('location', anchor=W, width=200)
    stock_treeview.heading("container",text="Container",anchor=W, command= lambda: column_heading_click_sort('containers.container_name', 5))
    stock_treeview.column('container', anchor=W, width=280)
    stock_treeview.heading("date",text="Date",anchor=W, command= lambda: column_heading_click_sort('stock.date', 7))
    stock_treeview.column('date', anchor=W, width=300)

    stock_treeview.bind("<Button-1>", block_heading_resize)
    stock_treeview.bind("<Button-3>", popup_right_click_menu)
 
def build_right_click_menu_with_commands():
    global right_click_menu
    right_click_menu = Menu(root, tearoff= 0)
    right_click_menu.add_command(label ="Move", command= lambda: popup_right_click_menu_choice('Move'))
    right_click_menu.add_command(label ="Recount", command= lambda: popup_right_click_menu_choice('Recount'))
    right_click_menu.add_command(label ="Repack", command= lambda: popup_right_click_menu_choice('Repack'))
    right_click_menu.add_command(label ="Merge", command= lambda: popup_right_click_menu_choice('Merge'))
    right_click_menu.add_command(label ="Delete", command= lambda: popup_right_click_menu_choice('Delete'))
    right_click_menu.add_separator()
    right_click_menu.add_command(label ="Add new record", command= lambda: popup_right_click_menu_choice('Add'))

def popup_right_click_menu(event):
    iid = stock_treeview.identify_row(event.y)
    
    try:
        if iid:
            stock_treeview.selection_set(iid)
            right_click_menu.tk_popup(event.x_root, event.y_root)
        else:
            right_click_menu_just_add = Menu(root, tearoff= 0)
            right_click_menu_just_add.add_command(label ="Add new record", command= lambda: popup_right_click_menu_choice('Add'))
            right_click_menu_just_add.tk_popup(event.x_root, event.y_root)


    finally:
        right_click_menu.grab_release()

def block_heading_resize(event):
    if stock_treeview.identify_region(event.x, event.y) == 'separator':
        return 'break'

def build_gui():
    root = build_root()
    build_fonts()
    build_label(root, 'STOCK LIST', big_font)
    build_styles()
    build_stock_treeview(root)
    build_stock_treeview_columns_with_headings_in_style()
    build_right_click_menu_with_commands()


def fill_treeview_with_table_records(treeview: Treeview, column: str, order: str):
    treeview.delete(*treeview.get_children())
    for id, record in enumerate(db.return_formated_stock_by_column(column, order)):
        treeview.insert(parent='',index='end', iid= id, text='', values= (record))


def is_treeview_sorted(index: int):
    list_of_values = []
    for record in stock_treeview.get_children():
        list_of_values.append(stock_treeview.item(record, 'values')[index])
    if list_of_values == sorted(list_of_values):
        return('DESC')
    else:
        return('ASC')
     

def column_heading_click_sort(column: str, index: int):
    fill_treeview_with_table_records(stock_treeview, column, is_treeview_sorted(index))


def popup_right_click_menu_choice(event: str):
        top = Toplevel(root)
        top.resizable(False, False)
        selected_choice = stock_treeview.selection()
        top.geometry('500x100+550+300')
        top.title(event)
        top.grab_set()

        try:
            selected_choice_amount = stock_treeview.item(selected_choice, 'values')[4]
        except:
            selected_choice_amount = 0

        def check_if_entry_is_selected_choice_amount():
           return amount_entry.get() == selected_choice_amount


        def create_proceed_button(function_name: Callable, row, column):
            button = Button(top, text= 'Proceed', command= function_name)
            button.grid(row= row, column= column, padx= 20)
            

        def create_label(text: str, row,column: int):
            label = Label(top, text= text)
            label.grid(row= row, column= column)
            return label
        
        def create_combobox(table, table_column: str, row,column: int):
            combobox = Combobox(top)
            combobox.grid(row= row, column= column)
            combobox['values'] = db.return_values_from_table_column(table, table_column)
            combobox.current(0)
            return combobox

        def create_amount_entry(row, column: int):
            amount_entry = Entry(top, width= 20)
            amount_entry.grid(row = row, column= column, padx= 20)
            try:
                stock_treeview.item(selected_choice, 'values')[4]
                amount_entry.insert(0, stock_treeview.item(selected_choice, 'values')[4])
            except:
                pass
            finally:
                top_register = top.register(amount_entry_validation)
                amount_entry.config(validate='key', validatecommand=(top_register, '%v', '%P'))
                return amount_entry

        def amount_entry_validation(v, input): 
                    if input.isdigit():
                        return True
                    elif input == '':
                        return True
                    else:
                        return False      

        def button_command_move():
            if check_if_entry_is_selected_choice_amount() == True:
                top.destroy()
            else:
                pass

        def button_command_recount():
            if check_if_entry_is_selected_choice_amount() == True:
                top.destroy()
            else:
                pass

        def button_command_repack():
            top.destroy()

        def button_command_merge():
            top.destroy()

        def button_command_add():
            record = []
            record.append(article_code_entry.get())
            if db.check_if_table_contains('products', 'products.article_code', record[0]) == 1:
                print('Record in db')
            else:
                print('No such record in db')
            record.append(amount_entry.get())
            
            record.append(location_combobox.get())
            record.append(container_combobox.get())
            record.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            record.append(os.getlogin())

            


        def key_release_search(event):
            article_code_listbox.delete(0, END)
            for record in db.return_values_from_table_column_where_ilike('products', 'products.article_code', f'{(article_code_entry.get().upper().replace(" ",""))}%'):
                article_code_listbox.insert(0, record)

        def fill_entry_with_selected(event):
            article_code_entry.delete(0, END)
            article_code_entry.insert(0, article_code_listbox.get((article_code_listbox.curselection())[0])[0])
            article_code_entry.focus()
            article_code_listbox.delete(0, END)



            
        
        match event:
            case 'Move':
                move_label = create_label('Move to:', 0, 0)
                amount_label = create_label('Amount:', 0, 1)
                location_combobox = create_combobox('locations', 'locations.location_name', 1, 0)
                amount_entry = create_amount_entry(1, 1)
                create_proceed_button(button_command_move, 1, 2)
                
            case 'Recount':
                amount_label = create_label('Amount:', 0, 1)
                amount_entry = create_amount_entry(1, 1)
                create_proceed_button(button_command_recount, 1, 2)
            case 'Repack':
                repack_label = create_label('Repack:', 0, 1)
                container_combobox = create_combobox('containers', 'containers.container_name', 1, 1)
                create_proceed_button(button_command_repack, 1, 2)
            case 'Merge':
                top.geometry('1000x300+550+300')
                top_style = Style()
                top_style.configure("Custom.Treview.Heading", font = (None, 6))
                top_style.configure("Custom.Treview", font = (None, 20))
                merge_treeview = Treeview(top, style= "Custom.Treeview", show= "tree")

                merge_treeview.grid(row= 0, column= 0)
                merge_treeview['columns'] = ('ID', 'article_code', 'serial_number', 'location', 'amount', 'container', 'description', 'date')                
                merge_treeview.column("#0", width=0, stretch=NO)
                merge_treeview.column('ID', anchor=W, width=20)
                merge_treeview.column('article_code', anchor=W, width=160)
                merge_treeview.column('serial_number', anchor=W, width=120)
                merge_treeview.column('description', anchor=W, width=0, stretch=NO)
                merge_treeview.column('amount', anchor=W, width=60)
                merge_treeview.column('location', anchor=W, width=180)
                merge_treeview.column('container', anchor=W, width=150)
                merge_treeview.column('date', anchor=W, width=280)
                fill_treeview_with_table_records(merge_treeview, 'stock.date', 'DESC')
                create_proceed_button(button_command_merge, 1, 0)
            case 'Add':
                top.geometry('1100x200+550+300')
                article_code_label = create_label('Article code:', 0, 0)
                article_code_entry = Entry(top, width= 20)
                article_code_entry.grid(row= 1, column= 0)
                article_code_listbox = Listbox(top)
                article_code_listbox.grid(row= 2, column= 0)
                for record in db.return_values_from_table_column('products', 'products.article_code'):
                    article_code_listbox.insert(0, record)

                full_gitterbox_weight_label = create_label('Full container weight:', 0, 1)
                full_gitterbox_weight_entry = Entry(top, width= 7)
                full_gitterbox_weight_entry.grid(row = 1, column= 1, padx= 20)
                
                one_product_weight_label = create_label('One product weight', 0, 2)
                one_product_weight_entry = Entry(top, width= 7)
                one_product_weight_entry.grid(row = 1, column= 2)



                empty_gitterbox_weight_label = create_label('Empty container weight:', 0, 3)
                empty_gitterbox_weight_entry = Entry(top, width= 7)
                empty_gitterbox_weight_entry.grid(row= 1, column= 3)
                empty_gitterbox_weight_entry.insert(0, 83)
                

                amount_label = create_label('Amount:', 0, 4)
                amount_entry = create_amount_entry(1, 4)
                amount_entry.delete(0, END)  
                location_combobox = create_combobox('locations', 'locations.location_name', 1, 5)
                container_combobox = create_combobox('containers', 'containers.container_name', 1, 6)

                article_code_entry.focus()
                create_proceed_button(button_command_add, 1, 7)

                '''def key_release_calculate(event):
                    amount_entry.delete(0, END)
                    amount = (int(full_gitterbox_weight_entry.get()) - int(empty_gitterbox_weight_entry.get())) / int(one_product_weight_entry.get())
                    if amount > 0:
                        amount_entry.insert(0, amount)
                    else:
                        pass'''



                '''full_gitterbox_weight_entry.insert(0, 580)
                one_product_weight_entry.insert(0, 0.33)  
                article_code_entry.insert(0, 'BEKC100230A')'''
                
                article_code_entry.bind('<KeyRelease>', key_release_search)
                article_code_listbox.bind('<ButtonRelease-1>', fill_entry_with_selected)
                #full_gitterbox_weight_entry.bind('<KeyRelease>', key_release_calculate)
                #empty_gitterbox_weight_entry.bind('<KeyRelease>', key_release_calculate)
                #one_product_weight_entry.bind('<KeyRelease>', key_release_calculate)
                
                
    
                
        

build_gui()

fill_treeview_with_table_records(stock_treeview, 'stock.date', 'DESC')

#popup_right_click_menu_choice('Add')




root.mainloop()