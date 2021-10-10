from db.models import TerroristAct, TargetInfo, WeaponInfo, AttackType
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

def finalize_terrorists():
    initialize()
    session = create_session()
    print('Objects added')
    with open('scripts/data.csv', encoding = "ISO-8859-1") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        objects = []
        attack_type_objects = []
        for result in session.query(AttackType):
            attack_type_objects.append(result)
        for row in csv_reader:
            if line_count == 0 or line_count <=48171:
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
                    if not row['propextent'] == '':
                        db_object.prop_dam_ext = int(row['propextent'])
                    if not row['propvalue'] == '':
                        value_split = row['propvalue'].split('.')
                        db_object.prop_dam_value = int(value_split[0])
                    if not row['propcomment'] == '':
                        db_object.prop_comment = row['propcomment']
                elif int(row['property']) == 0:
                    db_object.prop_dam = int(row['property'])

                if not row['ishostkid'] == '':
                    if int(row['ishostkid']) == 1:
                        db_object.hostages = int(row['ishostkid'])
                        if not row['nhostkid'] == '':
                            db_object.num_hostages = int(row['nhostkid'])
                        if not row['nhostkidus'] == '':
                            db_object.num_hostages_us = int(row['nhostkidus'])
                        if not row['ransom'] == '-9' and not row['ransom'] == '':
                            db_object.ransom = int(row['ransom'])
                            if not row['ransomamt'] == '':
                                ransom_split = row['ransomamt'].split('.')
                                db_object.ransom_amt = int(ransom_split[0])
                    elif int(row['ishostkid']) == 0:
                        db_object.hostages = int(row['ishostkid'])


                # handle targets
                if not row['targtype1'] == '':
                    dict = {
                        'terror_act': db_object.id,
                        'target_type': int(row['targtype1']),
                    }
                    if not row['targsubtype1'] == '':
                        dict['target_subtype'] = int(row['targsubtype1'])
                    if not row['target1'] == '':
                        dict['target'] = row['target1'][0:128]
                    if not row['natlty1'] == '':
                        dict['nationality'] = row['natlty1']
                    objects.append(TargetInfo(**dict))

                if not row['targtype2'] == '':
                    dict = {
                        'terror_act': db_object.id,
                        'target_type': int(row['targtype2']),
                    }
                    if not row['targsubtype2'] == '':
                        dict['target_subtype'] = int(row['targsubtype2'])
                    if not row['target2'] == '':
                        dict['target'] = row['target2'][0:128]
                    if not row['natlty2'] == '':
                        dict['nationality'] = row['natlty2']
                    objects.append(TargetInfo(**dict))

                if not row['targtype3'] == '':
                    dict = {
                        'terror_act': db_object.id,
                        'target_type': int(row['targtype3']),
                    }
                    if not row['targsubtype3'] == '':
                        dict['target_subtype'] = int(row['targsubtype3'])
                    if not row['target1'] == '':
                        dict['target'] = row['target1'][0:128]
                    if not row['natlty3'] == '':
                        dict['nationality'] = row['natlty3']
                    objects.append(TargetInfo(**dict))


                # Handle Weapons
                if not row['weaptype1'] == '':
                    dict = {
                        'terror_act': db_object.id,
                        'weapon_type': int(row['weaptype1'])
                    }
                    if not row['weapsubtype1'] == '':
                        dict['weapon_subtype'] = int(row['weapsubtype1'])
                    objects.append(WeaponInfo(**dict))

                if not row['weaptype2'] == '':
                    dict = {
                        'terror_act': db_object.id,
                        'weapon_type': int(row['weaptype2'])
                    }
                    if not row['weapsubtype2'] == '':
                        dict['weapon_subtype'] = int(row['weapsubtype2'])
                    objects.append(WeaponInfo(**dict))

                if not row['weaptype3'] == '':
                    dict = {
                        'terror_act': db_object.id,
                        'weapon_type': int(row['weaptype3'])
                    }
                    if not row['weapsubtype3'] == '':
                        dict['weapon_subtype'] = int(row['weapsubtype3'])
                    objects.append(WeaponInfo(**dict))

                if not row['weaptype4'] == '':
                    dict = {
                        'terror_act': db_object.id,
                        'weapon_type': int(row['weaptype4'])
                    }
                    if not row['weapsubtype4'] == '':
                        dict['weapon_subtype'] = int(row['weapsubtype4'])
                    objects.append(WeaponInfo(**dict))

                # Attack Types
                if not row['attacktype1'] == '':
                    attack_object = None
                    for object in attack_type_objects:
                        if object.id == int(row['attacktype1']):
                            attack_object = object
                            break
                    db_object.attack_types.append(attack_object)

                if not row['attacktype2'] == '':
                    attack_object = None
                    for object in attack_type_objects:
                        if object.id == int(row['attacktype2']):
                            attack_object = object
                            break
                    db_object.attack_types.append(attack_object)

                if not row['attacktype3'] == '':
                    attack_object = None
                    for object in attack_type_objects:
                        if object.id == int(row['attacktype3']):
                            attack_object = object
                            break
                    db_object.attack_types.append(attack_object)

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
