import os


class Config:
    def __init__(self, input_data: str, output_data: str, output_figure: str):
        self.input_data = self.setup_folder_path(input_data)
        self.output_data = self.setup_folder_path(output_data)
        self.output_figure = self.setup_folder_path(output_figure)

    @staticmethod
    def setup_folder_path(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path
