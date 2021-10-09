from db.models import City
import csv
from db.database_connection import initialize, create_session
from db.db_utils import get_or_create

def gen_cities():
    initialize()
    session = create_session()
    regions = []
    with open('scripts/data.csv', encoding = "ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[11] not in regions:
                    regions.append(row[12])
                    try:
                        object, created = get_or_create(session, City, name=row[12])
                        session.commit()
                    except UnicodeEncodeError:
                        print(row[12])
                line_count += 1
                if line_count % 500 == 0:
                    print(line_count)

