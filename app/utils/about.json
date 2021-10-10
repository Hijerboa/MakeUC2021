import json, os

def get_about():
    about_file = os.path.dirname(os.path.dirname(__file__))
    about_file = os.path.join(about_file, 'utils', 'about.json')
    with open(about_file) as f:
        about = json.load(f)
        return about