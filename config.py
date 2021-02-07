import os
from pathlib import Path

template_directory = Path(os.path.abspath(os.path.dirname(__file__))).joinpath('web')
email_template_directory = Path(os.path.abspath(os.path.dirname(__file__))).joinpath('helpers', 'templates')

random_long_string = 'ydfnxxxtzlhsarzbaknwrcgyboklqt'
email_sender = 'noreply@seecook.info'
personal_address = 'calebcook353@gmail.com'
requester_response_template = 'website_email_response.html'
