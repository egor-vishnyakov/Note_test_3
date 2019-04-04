import os
import csv
import datetime
from dateutil import parser
import uuid


TITLES_FILE = 'titles.csv'
STORAGE_FOLDER = 'storage'
EXTENT = '.txt'
QUIT_PHRASE = 'QUIT!'

MY_NAME = 'name'
MY_GUID = 'GUID'
MY_CREATE_DATE = 'create_date'
MY_MODIF_DATE = 'modif_date'
MY_IS_FOLDER = 'is_folder'
MY_PARENT_ID = 'parent_id'


class Title:
    """Pretty note data"""

    def __init__(self, line=None):
        """Waiting for dict"""
        self.line = line if line else {}
        if (line == None):
            self.line[MY_CREATE_DATE] = datetime.datetime.now()
            self.line[MY_MODIF_DATE] = datetime.datetime.now()

    def get_dict(self):
        return self.line

    def get_name(self):
        return self.line[MY_NAME]

    def set_name(self, new_name):
        self.line[MY_NAME] = new_name

    def get_guid(self):
        return self.line[MY_GUID]

    def set_guid(self, new_guid):
        self.line[MY_GUID] = new_guid

    def get_create_date(self):
        return self.line[MY_CREATE_DATE]

    def get_modif_date(self):
        return self.line[MY_MODIF_DATE]

    def set_modif_date(self, new_date):
        self.line[MY_MODIF_DATE] = new_date

    def get_is_folder(self):
        # return self.line[MY_IS_FOLDER]
        return self.line.get(MY_IS_FOLDER, None)

    def set_is_folder(self, new_is_folder):
        self.line[MY_IS_FOLDER] = new_is_folder

    def get_parent_id(self):
        # return self.line[MY_PARENT_ID]
        return self.line.get(MY_PARENT_ID, None)

    def set_parent_id(self, new_parent_id):
        self.line[MY_PARENT_ID] = new_parent_id


class Titles:
    """"Simple container for notes titles"""

    def __init__(self):
        self.titles = []
        self.cur = 0

    def add(self, line):
        """Expect dict"""
        self.titles.append(Title(line))

    def get(self, num):
        """Expect serial number of title"""
        return self.titles[num]

    def __iter__(self):
        # return self.titles
        self.cur = 0
        return self

    def __next__(self):
        if self.cur >= len(self.titles):
            raise StopIteration();

        cur_title = self.titles[self.cur];
        self.cur += 1
        return cur_title


class Storage:
    def __init__(self, folder=STORAGE_FOLDER):
        self.folder = folder

    def get_note_data(self, note_id):
        note_data = self.search_note(note_id)
        note_text = self._inner_get_note_text(note_data)
        note_data.text = note_text

        return note_data

    def _inner_get_note_text(self, note_data):
        try:
            with open(self.get_filename(note_data), 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f'Заметка "{note_data.get_name()}" не существует')

    def get_note_text(self, note_id):
        note_data = self.search_note(note_id)

        return self._inner_get_note_text(note_data)

    def search_note(self, note_id):
        titles = self.read_titles()

        for title in titles:
            if title.get_guid() == note_id:
                return title

        return {}

    def _inner_write_note(self, note_data, text):
        with open(self.get_filename(note_data), 'w') as f:
            f.write(text + '\n')

    def write_note(self, note_id, text, name):
        note_data = self.search_note(note_id)
        note_data.set_name(name)

        if note_data:
            self._inner_write_note(note_data, text)
        else:
            print('Error! No filename')

        self.write_name(note_data)

    def read_titles(self):
        with open(self.get_titles_name(), 'r') as f:
            reader = csv.DictReader(f)

            titles = Titles()
            for line in reader:
                titles.add(line)

            return titles

    def add_new_note(self, name, text='', parent_id=None, is_folder=False):
        new_guid = uuid.uuid4().hex
        self.append_name(name if name else new_guid, new_guid, is_folder, parent_id)
        self.write_note(new_guid, text, name)

        return new_guid

    def append_name(self, name, guid=None, parent_id=None, is_folder=False):
        with open(self.get_titles_name(), 'a', newline='\n') as f:
            writer = csv.DictWriter(f, delimiter=',', fieldnames=self.get_fieldnames())

            new_note = Title()
            new_note.set_guid(guid if guid else uuid.uuid4().hex)
            new_note.set_name(name)
            new_note.set_is_folder(is_folder)
            new_note.set_parent_id(parent_id)

            writer.writerow(new_note.get_dict())
            return new_note

    def write_name(self, note_data):
        titles = self.read_titles();

        with open(self.get_titles_name(), 'w') as f:
            writer = csv.DictWriter(f, delimiter=',', fieldnames=self.get_fieldnames())
            writer.writeheader()

            for title in titles:
                if title.get_guid() == note_data.get_guid():
                    title.set_modif_date(datetime.datetime.now())
                    title.set_name(note_data.get_name())
                writer.writerow(title.get_dict())

    def delete_name(self, note_data):
        titles = []

        with open(self.get_titles_name(), 'r') as f:
            reader = csv.DictReader(f)
            for line in reader:
                titles.append(line)

        with open(self.get_titles_name(), 'w') as f:
            writer = csv.DictWriter(f, delimiter=',', fieldnames=self.get_fieldnames())
            writer.writeheader()

            for line in titles:
                if line[MY_GUID] == note_data[MY_GUID]:
                    print('GUID deleted')
                else:
                    writer.writerow(line)

    def get_filename(self, note_data):
        # return STORAGE_FOLDER + '/' + note_data[MY_GUID] + EXTENT
        # return STORAGE_FOLDER + '/' + note_data.get(MY_GUID, 'NONE') + EXTENT
        return self.folder + '/' + note_data.get_guid() + EXTENT

    def get_titles_name(self):
        return self.folder + '/' + TITLES_FILE

    def get_fieldnames(self):
        return [MY_GUID, MY_NAME, MY_CREATE_DATE, MY_MODIF_DATE]

    def search_name(self, name):
        titles = self.read_titles()
        for title in titles:
            # print(title)
            # if name == title[MY_NAME]:
            if name == title.get_name():
                return title

        return {}

    def _search_guid_in_data(self, data, guid):
        for title in data:
            if title.get_guid() == guid:
                return title

        return {}

    def get_storage_structure(self):
        titles = self.read_titles()

        # test_list.append({'folder': True, 'name': 'folder1', 'parent': None, 'id': 1})

        def map_dict(title):
            res = dict()
            res['folder'] = title.get_is_folder()
            res['name'] = title.get_name()
            res['parent'] = title.get_parent_id()
            res['id'] = title.get_guid()
            return res

        structure = list(map(map_dict, titles)) # [title.get_dict() for title in titles]

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
