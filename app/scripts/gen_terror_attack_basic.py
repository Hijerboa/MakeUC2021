from db.models import TerroristAct, ProvState, City, Location
import csv
from db.database_connection import initialize, create_session
from datetime import date
from db.db_utils import get_single_object, create_single_object

def gen_terrorists():
    initialize()
    session = create_session()
    countries = []
    with open('scripts/data.csv', encoding = "ISO-8859-1") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        objects = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                basic_info = {
                    'id': row['eventid'],
                    'approx_date': row['approxdate'],
                    'extended': int(row['extended']),
                    'country': row['country'],
                    'region': row['region'],
                    'latitude': row['latitude'],
                    'longitude': row['longitude'],
                    'specificity': row['specificity'],
                    'vicinity': int(row['vicinity']),
                    'summary': row['summary']
                }
                if row['imonth'] == '0':
                    month = 1
                else:
                    month = int(row['imonth'])
                if row['iday'] == '0':
                    day = 1
                else:
                    day = int(row['imonth'])
                basic_info['date'] = date(int(row['iyear']), month, day)
                if not row['resolution'] == '':
                    row_value = row['resolution'].split('/')
                    basic_info['resolution'] = date(int(row_value[2]), int(row_value[0]), int(row_value[1]))
                if row['latitude'] == '' or row['longitude'] == '':
                    continue
                basic_info['latitude'] = row['latitude']
                basic_info['longitude'] = row['longitude']
                if not row['resolution'] == '':
                    basic_info['resolution'] = row['resolution']
                # get prov_state
                if not row['provstate'] == '':
                    prov_object = get_single_object(session, ProvState, name=row['provstate'])
                    basic_info['prov_state'] = prov_object.id
                # get city
                if not row['city'] == '':
                    city_object = get_single_object(session, City, name=row['city'])
                # get location
                if not row['location'] == '':
                    location = get_single_object(session, Location, name=row['location'])
                objects.append(TerroristAct(**basic_info))
                line_count += 1
                if line_count % 500 == 0:
                    session.bulk_save_objects(objects)
                    session.commit()
                    objects = []
                    print(line_count)
        session.bulk_save_objects(objects)
        session.commit()
        session.close()
