import json
import os

class Storage:
    def __init__(self, file_path):
        """
        Initialize the Storage.

        :param file_path: Path to the JSON file for saving/loading data.
        """
        self.file_path = file_path

    def save(self, data):
        """
        Save data to a JSON file.

        :param data: A dictionary containing tasks and completed tasks.
        """
        folder = os.path.dirname(self.file_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def load(self):
        """
        Load data from a JSON file.

        :return: A dictionary containing tasks and completed tasks.
        """
        if not os.path.exists(self.file_path):
            return {"tasks": [], "completed_tasks": []}

        with open(self.file_path, "r") as file:
            return json.load(file)
