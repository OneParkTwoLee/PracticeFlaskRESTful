class FileModel:
    def __init__(self, file, creation_date, label):
        # We will automatically generate the new id
        self.id = 0
        self.file = file
        self.creation_date = creation_date
        self.label = label