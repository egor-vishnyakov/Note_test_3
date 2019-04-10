import tkinter as tk
from tkinter import ttk


TREE_FOLDER = 'folder'
TREE_PARENT = 'parent'
TREE_ID = 'id'
TREE_NAME = 'name'


class NoteTreeView(ttk.Frame):
    def __init__(self, parent=None, structure=None):
        ttk.Frame.__init__(self, parent)
        self.folders_id = {}

        self.pack(expand=tk.YES, fill=tk.Y)
        self.make_widgets()
        self.set_tree(structure)
        self.set_selection_first()

    def make_widgets(self):
        sbar = tk.Scrollbar(self)
        treeview = ttk.Treeview(self)

        sbar.config(command=treeview.yview())
        treeview.config(yscrollcommand=sbar.set)

        sbar.pack(side=tk.RIGHT, fill=tk.Y)
        treeview.pack(side=tk.LEFT, fill=tk.BOTH)

        self.treeview = treeview
        self.config_tree()

    def config_tree(self):
        self.treeview['columns'] = TREE_ID
        self.treeview.column('#0', width=250, minwidth=250, stretch=tk.NO)
        self.treeview.column(TREE_ID, width=0, minwidth=0, stretch=tk.NO)

        self.treeview.heading('#0', text='Блокноты', anchor=tk.CENTER)
        self.treeview.heading(TREE_ID, text=TREE_ID, anchor=tk.CENTER)

    def set_tree(self, structure):
        if not structure:
            return

        # children = self.treeview.get_children()
        # if len(children) > 0:
        for child in self.treeview.get_children():
            self.treeview.delete(child)

        for line in structure:
            parent = line.get(TREE_PARENT)
            item_id = line.get(TREE_ID, '')
            row = self.treeview.insert(self.folders_id.get(parent if parent else '', ''), 'end', '',
                                       text=line.get(TREE_NAME), values=item_id)
            is_folder = line.get(TREE_FOLDER)
            if is_folder:
                self.folders_id[item_id] = row

            print('parent: ', parent, 'id: ', item_id, 'name: ', line.get(TREE_NAME))

        print(self.folders_id)

    def set_selection(self, item):
        self.treeview.selection_set(item)
        self.treeview.focus(item)

    def set_selection_first(self):
        self.set_selection(self.treeview.get_children()[0])


    def get_id(self, line):
        return self.treeview.set(line, column=TREE_ID)

    def get_cur_id(self):
        return self.get_id(self.treeview.focus())

    def get_cur_data(self):
        return self.treeview.set(self.treeview.focus())

    def get_cur_raw(self):
        return self.treeview.item(self.treeview.focus())

    def get_cur_parent_id(self):
        return self.get_parent_id(self.treeview.focus())

    def get_parent_id(self, line_id):
        return self.get_id(self.treeview.parent(line_id))


if __name__ == '__main__':
    test_list = list()
    test_list.append({TREE_FOLDER: True, TREE_NAME: 'folder1', TREE_PARENT: None, TREE_ID: 1})
    test_list.append({TREE_FOLDER: False, TREE_NAME: 'note1', TREE_PARENT: 1, TREE_ID: 2})
    test_list.append({TREE_FOLDER: False, TREE_NAME: 'note2', TREE_PARENT: 1, TREE_ID: 3})
    test_list.append({TREE_FOLDER: False, TREE_NAME: 'note3', TREE_PARENT: 1, TREE_ID: 4})

    test_list.append({TREE_FOLDER: True, TREE_NAME: 'folder2', TREE_PARENT: 1, TREE_ID: 5})
    test_list.append({TREE_FOLDER: False, TREE_NAME: 'note4', TREE_PARENT: 5, TREE_ID: 6})
    test_list.append({TREE_FOLDER: False, TREE_NAME: 'note5', TREE_PARENT: 5, TREE_ID: 7})
    test_list.append({TREE_FOLDER: False, TREE_NAME: 'note6', TREE_PARENT: 5, TREE_ID: 8})

    test_list.append({TREE_FOLDER: True, TREE_NAME: 'folder3', TREE_PARENT: None, TREE_ID: 9})
    test_list.append({TREE_FOLDER: False, TREE_NAME: 'note7', TREE_PARENT: 9, TREE_ID: 10})
    test_list.append({TREE_FOLDER: False, TREE_NAME: 'note8', TREE_PARENT: 9, TREE_ID: 11})
    test_list.append({TREE_FOLDER: False, TREE_NAME: 'note9', TREE_PARENT: 9, TREE_ID: 12})

    test_list.append({TREE_FOLDER: True, TREE_NAME: 'folder4', TREE_PARENT: None, TREE_ID: 13})
    test_list.append({TREE_FOLDER: False, TREE_NAME: 'note10', TREE_PARENT: 13, TREE_ID: 14})
    test_list.append({TREE_FOLDER: False, TREE_NAME: 'note11', TREE_PARENT: 13, TREE_ID: 15})
    test_list.append({TREE_FOLDER: False, TREE_NAME: 'note12', TREE_PARENT: 13, TREE_ID: 16})

    test_list.append({TREE_NAME: 'note13', TREE_PARENT: None})

    root = tk.Tk()
    ntv = NoteTreeView(structure=test_list)

    def test(event):
        print(ntv.get_cur_id())
        print(ntv.get_cur_data())
        print(ntv.get_cur_raw())

    root.bind('<Control-s>', test)

    root.mainloop()
