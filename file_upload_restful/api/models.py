class FileModel:
    def __init__(self, creation_date, size):
        # We will automatically generate the new id
        self.id = 0
        self.creation_date = creation_date
        self.size = size