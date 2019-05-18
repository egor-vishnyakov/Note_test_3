import note_storage2 as st

from Scrolled_text_1 import ScrolledText as SText
from Treeview_test2 import NoteTreeView as NTV
from tkinter import *
import pprint

class MyNote(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.storage = st.Storage(folder='storage')
        self.pack(expand=YES, fill=BOTH)
        self.make_widgets()
        self.make_binds()

    def test(self, event):
        print('Test!')

    def make_widgets(self):
        frame1 = Frame(self)
        frame1.pack(expand=YES, fill=Y, side=LEFT)

        # notes_listbox = Listbox(frame1)
        # notes_listbox.pack(expand=YES, fill=BOTH, side=TOP)
        # self.list_notes = notes_listbox

        frame_btn_folder = Frame(frame1)
        frame_btn_folder.pack(fill=X, side=TOP)

        btn_f1 = Button(frame_btn_folder, text='AddF', command=self.add_folder)
        btn_f1.pack(side=LEFT)

        ntv = NTV(frame1, structure=self.make_structure())
        ntv.pack(expand=YES, fill=Y, side=TOP)
        self.tree = ntv

        frame_btn_note = Frame(frame1)
        frame_btn_note.pack(fill=X, side=BOTTOM)

        btn1 = Button(frame_btn_note, text='Open', command=self.open_note)
        btn1.pack(side=LEFT)

        btn2 = Button(frame_btn_note, text='Save', command=self.save_note)
        btn2.pack(side=RIGHT)

        btn3 = Button(frame_btn_note, text='AddN', command=self.add_note)
        btn3.pack(side=LEFT)

        btn4 = Button(frame_btn_note, text='Delete', command=self.delete_note)
        btn4.pack(side=RIGHT)

        frame_text = Frame(self)
        frame_text.pack(fill=BOTH, side=RIGHT)

        entry = Entry(frame_text)
        entry.pack(fill=X, side=TOP)
        self.name_entry = entry

        text = SText(frame_text)
        text.pack(fill=BOTH, side=BOTTOM)
        self.text = text

    def make_binds(self):
        self.tree.bind('<Double-Button-1>', self.open_note())
        # pass
        # self.tree.bind('<Control-o>', self.open_note)
        # self.text.bind('<Control-s>', self.save_note) #not here, text capture keys

    def open_note(self, note_id=None):
        self.cur_id = note_id if note_id else self.tree.get_cur_id()
        note_data = self.storage.get_note_data(self.cur_id)
        self.text.settext(note_data.text)
        self.set_name(note_data.get_name())

    def save_note(self, event=None):
        self.storage.write_note(self.cur_id, self.text.gettext(), self.get_name())
        self.refresh_notes()

    def add_note(self, event=None):
        # self.cur_id = self.storage.add_new_note('new_note', self.tree.get_cur_parent_id())
        self.cur_id = self.storage.add_new_note('new_note', parent_id=self.tree.get_cur_id())
        self.refresh_notes()
        self.open_note(self.cur_id)

    def delete_note(self, event=None):
        self.storage.delete_note(self.tree.get_cur_id())
        self.refresh_notes()

    def add_folder(self):
        self.cur_id = self.storage.add_new_folder('new_fodler', self.tree.get_cur_parent_id())
        self.refresh_notes()
        # self.open_note(self.cur_id)

    def make_structure(self):
        return self.storage.get_storage_structure()

    def refresh_notes(self):
        self.tree.set_tree(self.make_structure())

    def get_name(self):
        return self.name_entry.get()

    def set_name(self, new_name):
        self.name_entry.delete(0, END)
        self.name_entry.insert(0, new_name)


if __name__ == '__main__':
    root = Tk()

    mn = MyNote()

    def open_note(event):
        mn.open_note()

    def save_note(event):
        mn.save_note()

    def get_struct(event):
        mn.make_structure()

    root.bind('<Control-o>', open_note)
    root.bind('<Control-s>', save_note)
    # root.bind('<Control-ы>', save_note)
    root.bind('<Control-m>', get_struct)
    root.bind('<Double-Button-1>', open_note)
    root.mainloop()
