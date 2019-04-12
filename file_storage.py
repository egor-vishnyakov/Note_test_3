import os

EXTENT = '.txt'


class FileStorage:
    def __init__(self, folder):
        self.folder = folder

    def get_note_text(self, note_id):
        try:
            with open(self.get_filename(note_id), 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f'Note wit id "{note_id}" not exist')

    def set_note_text(self, note_id, text):
        with open(self.get_filename(note_id), 'w') as f:
            f.write(text + '\n')

    def get_filename(self, note_id):
        return self.folder + '/' + note_id + EXTENT

    def get_foldername(self, folder_id):
        return os.path.join(self.folder, folder_id)
        # return self.folder + '/' + folder_id

    def delete_note(self, note_id):
        os.remove(self.get_filename(note_id))

    def add_folder(self, folder_id):
        os.mkdir(self.get_foldername(folder_id))
