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

                db_object.success = int(row['success'])
                db_object.suicide = int(row['suicide'])

                if int(row['property']) == 1:
                    db_object.prop_dam = int(row['property'])
                    if not row['prop_extent'] == '':
                        db_object.prop_dam_ext = int(row['prop_extent'])
                    if not row['propvalue'] == '':
                        db_object.prop_dam_value = int(row['propvalue'])
                    if not row['propcomment'] == '':
                        db_object.prop_comment = row['propcomment']
                elif int(row['property']) == 0:
                    db_object.prop_dam = int(row['property'])

                if int(row['ishostkid']) == 1:
                    db_object.hostages = int(row['ishostkid'])
                    if not row['nhostkid'] == '':
                        db_object.num_hostages = int(row['nhostkid'])
                    if not row['nhostkidus'] == '':
                        db_object.num_hostages_us = int(row['nhostkidus'])
                    if not row['ransom'] == '-9' and not row['ransom'] == '':
                        db_object.ransom = int(row['ransom'])
                        if not row['ransomamt'] == '':
                            db_object.ransom_amt = int(row['ransomamt'])
                elif int(row['ishostkid']) == 0:
                    db_object.hostages = int(row['ishostkid'])

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
