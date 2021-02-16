import os
from pathlib import Path

from jinja2 import Template

template_directory = Path(os.path.abspath(os.getcwd())).joinpath('web')

email_sender = 'noreply@seecook.info'
requester_response_template = Template(
    Path(os.path.abspath(os.getcwd())).joinpath('web', 'templates', 'website_email_response.html').read_text()
).render()
