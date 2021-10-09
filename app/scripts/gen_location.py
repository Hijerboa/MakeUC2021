from db.models import Location
import csv
from db.database_connection import initialize, create_session
from db.db_utils import get_or_create

def gen_locs():
    initialize()
    session = create_session()
    locations = []
    with open('scripts/data.csv', encoding = "ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        objects = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[17] == '':
                    continue
                elif row[17] not in locations:
                    locations.append(row[17])
                    data = {'name': row[12]}
                    objects.append(Location(**data))
                line_count += 1
                if line_count % 100 == 0:
                    session.bulk_save_objects(objects)
                    session.commit()
                    objects = []
                    print(line_count)
        session.bulk_save_objects(objects)
        session.commit()
        session.close()