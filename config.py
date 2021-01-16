import os
from pathlib import Path

template_directory = Path(os.path.abspath(os.path.dirname(__file__))).joinpath('web')
image_directory = Path(os.path.abspath(os.path.dirname(__file__))).joinpath('web/images')
asset_directory = Path(os.path.abspath(os.path.dirname(__file__))).joinpath('web/assets')
