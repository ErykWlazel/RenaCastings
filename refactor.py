from tkinter import *
from tkinter.ttk import *
import orm

root = Tk()
root.title("GG")
#root.state("zoomed")
root.resizable(False, False)


def build_label(
    container: str,
    grid_row: int,
    grid_coulmn: int,
    label_text: str,
    grid_sticky: str = "NW",
    label_font: str = "TkDefaultFont ",
) -> Label:
    new_label = Label(container, text=label_text, font=label_font)
    new_label.grid(row=grid_row, column=grid_coulmn, sticky=grid_sticky)
    return new_label


def build_entry(
    container: str, grid_row: int, grid_column: int, stickiness: str = "NW"
) -> Entry:
    new_entry = Entry(container)
    new_entry.grid(row=grid_row, column=grid_column, sticky=stickiness)
    

    return new_entry


"""def entry_keyrelease_detach(custom_entry: Entry, event):
    article_code_listbox.delete(0, END)
    for record in db.return_values_from_table_column_where_ilike('products', 'products.article_code', f'{(article_code_entry.get().upper().replace(" ",""))}%'):
        article_code_listbox.insert(0, record)"""


def build_treeview(container: str, grid_row: int, grid_column: int) -> Treeview:
    new_treeview = Treeview(container)
    new_treeview.grid(row=grid_row, column=grid_column)
    return new_treeview


def build_style(theme_use: str = "clam") -> Style:
    new_style = Style()
    new_style.theme_use(theme_use)
    return new_style


def customize_treeview(
    custom_treeview: Treeview, custom_style: Style, treeview_columns: list[(str, int)]
) -> Treeview:
    custom_treeview["columns"] = [column for column, text_width in treeview_columns]
    custom_treeview.column("#0", width=0, stretch=NO)

    for (column, text_width) in treeview_columns:
        custom_treeview.heading(
            column, text=column, anchor=W
        )  # command = lambda: column_heading_click_sort('stock.id', 0))
        custom_treeview.column(column, width=text_width, anchor=W, stretch=NO)

    custom_style.configure("Treeview", font=(None, 16))
    custom_style.configure("Treeview.Heading", background="#D4D4D4", font=(None, 30))

    def block_heading_resize(event):
        if custom_treeview.identify_region(event.x, event.y) == "separator":
            return "break"

    custom_treeview.bind("<Button-1>", block_heading_resize)

    return custom_treeview


def fill_treeview_default(custom_treeview: Treeview) -> Treeview:
    custom_treeview.delete(*custom_treeview.get_children())
    for id, record in enumerate(orm.fetchall_default_ordered_stock()):
        custom_treeview.insert(parent="", index="end", iid=id, text="", values=(record))
    return custom_treeview




def build_gui():
    


    build_label(root, 0, 0, "Stock list:")

    stock_list_treeview = fill_treeview_default(
        (
        customize_treeview(
            build_treeview(root, 1, 0),
            build_style(),
            [
                ("ID", 60),
                ("article_code", 230),
                ("productie_order", 300),
                ("machining_line", 310),
                ("location", 200),
                ("amount", 180),
                ("container", 210),
                ("description", 240),
            ],
            )
        )
    )

    treeview_children = stock_list_treeview.get_children()
    build_label(root, 2, 0, "Search by article code:")


    def hide_records_not_like(event):
        like = stock_search_entry.get().upper()

        for children in treeview_children:
            stock_list_treeview.reattach(children, '', children)
            

        for records in stock_list_treeview.get_children():
            if not stock_list_treeview.item(records, 'values')[1].startswith(like):
                stock_list_treeview.detach(records)
                
    stock_search_entry = build_entry(root, 3, 0)
    stock_search_entry.focus()
    stock_children = stock_list_treeview.get_children()
    
    stock_search_entry.bind("<KeyRelease>", hide_records_not_like)
    
    

build_gui()



"""    
"""




root.mainloop()
