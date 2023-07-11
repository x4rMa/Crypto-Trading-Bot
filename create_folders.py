import os


class Folder:
    def __init__(self):
        pass

    def create_folder_link(self, folder_path, file_name):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, file_name)
        return file_path
