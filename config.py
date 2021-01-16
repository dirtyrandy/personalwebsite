import os
from pathlib import Path

web_templates_dir = Path(os.path.abspath(os.path.dirname(__file__))).joinpath('web/templates')
auth_templates_dir = Path(os.path.abspath(os.path.dirname(__file__))).joinpath('auth/templates')
