from tkinter import *
from tkinter.ttk import *
import orm as db

root = Tk()
root.title('GG')            
root.state('zoomed')
root.resizable(False, False)

def build_label(container: str, grid_row: int, grid_coulmn: int, label_text: str,  grid_sticky: str= 'NW', label_font: str = 'TkDefaultFont ') -> Label:
    new_label = Label(container, text= label_text, font= label_font)
    new_label.grid(row = grid_row, column= grid_coulmn, sticky= grid_sticky)
    return new_label

def build_treeview(container: str, grid_row: int, grid_column: int) -> Treeview:
    new_treeview = Treeview(container)
    new_treeview.grid(row = grid_row, column = grid_column)
    return new_treeview

def build_style(theme_use: str = 'clam') -> Style:
    new_style = Style()
    new_style.theme_use(theme_use)
    return new_style

def customize_treeview(custom_treeview: Treeview, custom_style: Style, treeview_columns: list[(str, int)]) -> Treeview:
    custom_treeview['columns'] = treeview_columns[]
    custom_treeview.column("#0", width=0, stretch=NO)


    for (column, text_width) in treeview_columns:
        print(column, text_width)
        #custom_treeview.heading(column, text= column, anchor= W)# command = lambda: column_heading_click_sort('stock.id', 0))
        #custom_treeview.column(column, width= text_width, anchor= W, stretch=NO)


    custom_style.configure("Treeview", font=(None, 16))
    custom_style.configure("Treeview.Heading", background= '#D4D4D4', font=(None, 38))

    return custom_treeview



build_label(root, 0, 0, 'Stock list:')
customize_treeview(build_treeview(root, 1, 0), build_style(), [('ID', 60), ('article_code', 280), ('serial_number', 330), ('location', 280), ('amount', 200), ('container', 200), ('description', 280), ('date', 300)])


root.mainloop()