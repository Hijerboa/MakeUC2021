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
        objects = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[12] not in regions:
                    regions.append(row[12])
                    data = {'name': row[12]}
                    objects.append(City(**data))
                line_count += 1
                if line_count % 500 == 0:
                    print(line_count)
                    session.bulk_save_objects(objects)
                    session.commit()
                    objects = []
        session.bulk_save_objects(objects)
        session.commit()
        session.close()