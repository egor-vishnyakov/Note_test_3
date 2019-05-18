import csv
import datetime

TITLES_FILE = 'titles.csv'

MY_NAME = 'name'
MY_GUID = 'GUID'
MY_CREATE_DATE = 'create_date'
MY_MODIF_DATE = 'modif_date'
MY_IS_FOLDER = 'is_folder'
MY_PARENT_ID = 'parent_id'


def get_fieldnames():
    return [MY_GUID, MY_NAME, MY_CREATE_DATE, MY_MODIF_DATE, MY_PARENT_ID, MY_IS_FOLDER]


class Title:
    """Pretty note data"""

    def __init__(self, line=None):
        """Waiting for dict"""
        self.line = line if line else {}
        if line == None:
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


class NoteTitles:
    def __init__(self, folder):
        self.folder = folder

    def read_titles(self):
        with open(self.get_titles_name(), 'r') as f:
            reader = csv.DictReader(f)

            titles = Titles()
            for line in reader:
                titles.add(line)

            return titles

    def append_name(self, name, guid, parent_id=None, is_folder=False):
        with open(self.get_titles_name(), 'a', newline='\n') as f:
            writer = csv.DictWriter(f, delimiter=',', fieldnames=get_fieldnames())

            new_note = Title()
            new_note.set_guid(guid)
            new_note.set_name(name)
            new_note.set_is_folder(is_folder)
            new_note.set_parent_id(parent_id)

            writer.writerow(new_note.get_dict())
            return new_note

    def write_name(self, note_data):
        titles = self.read_titles()

        with open(self.get_titles_name(), 'w') as f:
            writer = csv.DictWriter(f, delimiter=',', fieldnames=get_fieldnames())
            writer.writeheader()

            for title in titles:
                if title.get_guid() == note_data.get_guid():
                    title.set_modif_date(datetime.datetime.now())
                    title.set_name(note_data.get_name())
                writer.writerow(title.get_dict())

    def delete_name(self, note_id):
        titles = self.read_titles()

        with open(self.get_titles_name(), 'w') as f:
            writer = csv.DictWriter(f, delimiter=',', fieldnames=get_fieldnames())
            writer.writeheader()

            for title in titles:
                if title.get_guid() == note_id:
                    print('GUID deleted')
                else:
                    writer.writerow(title.get_dict())

    def search_name(self, name):
        titles = self.read_titles()
        for title in titles:
            if name == title.get_name():
                return title

        return {}

    def search_note(self, note_id):
        titles = self.read_titles()

        for title in titles:
            if title.get_guid() == note_id:
                return title

        return {}

    def get_titles_name(self):
        return self.folder + '/' + TITLES_FILE
