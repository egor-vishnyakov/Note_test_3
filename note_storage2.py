import os
import datetime
from dateutil import parser
import uuid
from file_storage import FileStorage as FST
from note_titles import NoteTitles as NTT


STORAGE_FOLDER = 'storage'
QUIT_PHRASE = 'QUIT!'


class Storage:
    def __init__(self, folder=STORAGE_FOLDER):
        self.folder = folder
        self.storage = FST(self.folder)
        self.note_titles = NTT(self.folder)

    def get_note_data(self, note_id):
        note_data = self.note_titles.search_note(note_id)
        note_text = self.storage.get_note_text(note_data.get_guid())
        note_data.text = note_text

        return note_data

    def get_note_text(self, note_id):
        note_data = self.note_titles.search_note(note_id)

        return self.storage.get_note_text(note_data.get_guid())

    # def search_note(self, note_id):
    #     titles = self.note_titles.read_titles()
    #
    #     for title in titles:
    #         if title.get_guid() == note_id:
    #             return title
    #
    #     return {}

    def write_note(self, note_id, text, name):
        note_data = self.note_titles.search_note(note_id)
        note_data.set_name(name)

        if note_data:
            self.storage.set_note_text(note_data.get_guid(), text)
        else:
            print('Error! No filename')

        self.note_titles.write_name(note_data)

    def add_new_note(self, name, text='', parent_id=None, is_folder=False):
        print('name: ', name, 'text: ', text, 'parent_id: ', parent_id, 'is_folder: ', is_folder)

        note_data = self.note_titles.search_note(parent_id)
        print('is parent folder: ', note_data.get_is_folder())

        new_guid = uuid.uuid4().hex
        self.note_titles.append_name(name if name else new_guid, new_guid, parent_id if note_data.get_is_folder() else None, is_folder)
        self.write_note(new_guid, text, name)

        return new_guid

    def delete_note(self, note_id):
        self.note_titles.delete_name(note_id)
        self.storage.delete_note(note_id)

    # self.storage.add_new_folder('new_fodler', self.tree.get_cur_parent_id())
    def add_new_folder(self, name, parent_id=None):
        new_guid = uuid.uuid4().hex
        self.note_titles.append_name(name if name else new_guid, new_guid, True, parent_id)
        self.storage.add_folder(new_guid)

        return new_guid

    def _search_guid_in_data(self, data, guid):
        for title in data:
            if title.get_guid() == guid:
                return title

        return {}

    def get_storage_structure(self):
        titles = self.note_titles.read_titles()

        def map_dict(title):
            res = dict()
            res['folder'] = title.get_is_folder()
            res['name'] = title.get_name()
            res['parent'] = title.get_parent_id()
            res['id'] = title.get_guid()
            return res

        structure = list(map(map_dict, titles))

        return structure

    def get_storage_structure2(self, storage_dir=STORAGE_FOLDER, parent_id=None):
        titles = self.read_titles()

        structure = list()

        for filename in os.listdir(storage_dir):
            full_path = os.path.join(STORAGE_FOLDER, filename)
            item_id = os.path.splitext(filename)[0]   # it's must be ID

            note_data = self._search_guid_in_data(titles, item_id)
            if note_data != {}:
                item_name = note_data.get_name()
            else:
                item_name = item_id

            if os.path.isdir(full_path):
                structure.append({'folder': True, 'name': item_name, 'parent': parent_id, 'id': item_id})
                structure = structure + self.get_storage_structure(full_path, item_id)
            else:
                structure.append({'folder': False, 'name': item_name, 'parent': parent_id, 'id': item_id})

        return structure
