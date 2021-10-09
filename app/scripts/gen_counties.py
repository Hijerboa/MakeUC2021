from db.models import Country
import csv
from db.database_connection import initialize, create_session

def gen_countries():
    initialize()
    session = create_session()
    with open('')
