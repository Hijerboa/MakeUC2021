from db.models import Country
import csv
from db.database_connection import initialize, create_session
from db.db_utils import get_or_create

def gen_countries():
    initialize()
    session = create_session()
    countries = []
    with open('scripts/data.csv', encoding = "ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if int(row[7]) not in countries:
                    countries.append(int(row[7]))
                    object, created = get_or_create(session, Country, id=int(row[7]), defaults={'name': row[8]})
                    session.commit()
                line_count += 1
                if line_count % 500 == 0:
                    print(line_count)

