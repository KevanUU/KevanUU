import os.path

from source.data_processor import DataProcessor
from utils.config import Config

cfg = Config(
    input_data='input',
    output_data=os.path.join('output', 'data'),
    output_figure=os.path.join('output', 'figure'),
)

if __name__ == "__main__":
    dp = DataProcessor(cfg)
    dp.main()
