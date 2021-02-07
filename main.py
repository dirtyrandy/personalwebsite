import os

from flask import Flask
from jinja2 import Template

from config import template_directory

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def root():
    template_file = next(
        file for file in template_directory.iterdir() if 'index.html' == file.name.lower()
    )
    return Template(template_file.read_text()).render(cloudfront_url=os.getenv('cloudfront_url'))


if __name__ == '__main__':
    app.run()
