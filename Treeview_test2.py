import tkinter as tk
from tkinter import ttk


class NoteTreeView(ttk.Frame):
    def __init__(self, parent=None, structure=None):
        ttk.Frame.__init__(self, parent)
        self.folders_id = {}

        self.pack(expand=tk.YES, fill=tk.Y)
        self.make_widgets()
        self.set_tree(structure)

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
        self.treeview['columns'] = 'id'
        self.treeview.column('#0', width=250, minwidth=250, stretch=tk.NO)
        self.treeview.column('id', width=0, minwidth=0, stretch=tk.NO)

        self.treeview.heading('#0', text='Блокноты', anchor=tk.CENTER)
        self.treeview.heading('id', text='ID', anchor=tk.CENTER)

    def set_tree(self, structure):
        if not structure:
            return

        for line in structure:
            parent = line.get('parent')
            item_id = line.get('id', '')
            row = self.treeview.insert(self.folders_id.get(parent if parent else '', ''), 'end', '',
                                       text=line.get('name'), values=item_id)
            is_folder = line.get('folder')
            if is_folder:
                self.folders_id[item_id] = row

            print('parent: ', parent, 'id: ', item_id, 'name: ', line.get('name'))

        print(self.folders_id)

    def get_id(self, line):
        return self.treeview.set(line, column='id')

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
    test_list.append({'folder': True, 'name': 'folder1', 'parent': None, 'id': 1})
    test_list.append({'folder': False, 'name': 'note1', 'parent': 1, 'id': 2})
    test_list.append({'folder': False, 'name': 'note2', 'parent': 1, 'id': 3})
    test_list.append({'folder': False, 'name': 'note3', 'parent': 1, 'id': 4})

    test_list.append({'folder': True, 'name': 'folder2', 'parent': 1, 'id': 5})
    test_list.append({'folder': False, 'name': 'note4', 'parent': 5, 'id': 6})
    test_list.append({'folder': False, 'name': 'note5', 'parent': 5, 'id': 7})
    test_list.append({'folder': False, 'name': 'note6', 'parent': 5, 'id': 8})

    test_list.append({'folder': True, 'name': 'folder3', 'parent': None, 'id': 9})
    test_list.append({'folder': False, 'name': 'note7', 'parent': 9, 'id': 10})
    test_list.append({'folder': False, 'name': 'note8', 'parent': 9, 'id': 11})
    test_list.append({'folder': False, 'name': 'note9', 'parent': 9, 'id': 12})

    test_list.append({'folder': True, 'name': 'folder4', 'parent': None, 'id': 13})
    test_list.append({'folder': False, 'name': 'note10', 'parent': 13, 'id': 14})
    test_list.append({'folder': False, 'name': 'note11', 'parent': 13, 'id': 15})
    test_list.append({'folder': False, 'name': 'note12', 'parent': 13, 'id': 16})

    test_list.append({'name': 'note13', 'parent': None})

    root = tk.Tk()
    ntv = NoteTreeView(structure=test_list)

    def test(event):
        print(ntv.get_cur_id())
        print(ntv.get_cur_data())
        print(ntv.get_cur_raw())

    root.bind('<Control-s>', test)

    root.mainloop()
