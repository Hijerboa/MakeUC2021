from db.models import TerroristAct, ProvState, City, Location
import csv
from db.database_connection import initialize, create_session
from datetime import date
from db.db_utils import get_single_object, create_single_object

def search_list(list, search_id):
    print('entered search')
    for item in list:
        if item.id == search_id:
            print('returning')
            return item
    return None

def gen_terrorists():
    initialize()
    session = create_session()
    """all_objects_query = session.query(TerroristAct).limit(1000).offset(1000)
    all_objects = []
    for object in all_objects_query:
        all_objects.append(object)"""
    print('Objects added')
    with open('scripts/data.csv', encoding = "ISO-8859-1") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        objects = []
        for row in csv_reader:
            if line_count == 0 or line_count <= 109000:
                line_count += 1
                continue
            else:
                db_object: TerroristAct = get_single_object(session, TerroristAct, id=int(row['eventid']))
                if db_object is None:
                    print("None found :(")
                    continue
                print(db_object.id)
                if row['doubtterr'] == 1:
                    db_object.doubout_terrorism = True
                elif row['doubtterr'] == 0:
                    db_object.doubout_terrorism = False
                if not row['alternative'] == '':
                    db_object.alt_designation = int(row['alternative'])
                if not row['multiple'] == '':
                    db_object.part_of_multiple = int(row['multiple'])

                # casualties
                if not row['nkill'] == '':
                    db_object.num_killed = int(row['nkill'])
                if not row['nkillus'] == '':
                    db_object.num_killed_us = int(row['nkillus'])
                if not row['nkillter'] == '':
                    db_object.num_perp_killed = int(row['nkillter'])
                if not row['nwound'] == '':
                    string = row['nwound']
                    string_split = string.split('.')
                    db_object.num_injured = int(string_split[0])
                if not row['nwoundus'] == '':
                    db_object.num_injured_us = int(row['nwoundus'])
                if not row['nwoundte'] == '':
                    db_object.num_perp_wounded = int(row['nwoundte'])

                objects.append(db_object)
                line_count += 1

            if len(objects) >= 500:
                session.bulk_save_objects(objects)
                session.commit()
                objects = []
                print(line_count)

        session.bulk_save_objects(objects)
        session.commit()
        objects = []
