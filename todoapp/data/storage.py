import json
import os

class Storage:
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, data):
        folder = os.path.dirname(self.file_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def load(self):
        if not os.path.exists(self.file_path):
            return {"tasks": [], "completed_tasks": []}

        with open(self.file_path, "r") as file:
            return json.load(file)
