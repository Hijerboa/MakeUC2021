from db.models import TargetType
import csv
from db.database_connection import initialize, create_session

def gen_targets():
    initialize()
    session = create_session()
    locations = []
    with open('scripts/data.csv', encoding = "ISO-8859-1") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        objects = []
        found = []
        found_dicts = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                id = row['targtype1']
                if int(id) not in found:
                    print('found')
                    found.append(int(id))
                    found_dicts.append({
                        'id': int(id),
                        'name': row['targtype1_txt']
                    })
        for value in found_dicts:
            objects.append(TargetType(**value))
        session.bulk_save_objects(objects)
        session.commit()
        session.close()
