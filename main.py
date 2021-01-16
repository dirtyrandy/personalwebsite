from config import auth_templates_dir, web_templates_dir

from flask import Flask
from jinja2 import Template


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def root():
    return Template(web_templates_dir.joinpath('base.html')).render()


if __name__ == '__main__':
    app.run()
