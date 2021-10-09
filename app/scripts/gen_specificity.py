from db.models import Specificity
from db.database_connection import initialize, create_session
from db.db_utils import get_or_create

def gen_spec():
    initialize()
    session = create_session()
    object, created = get_or_create(session, Specificity, id=1, defaults={
        'description': 'event occurred in city/village/town and lat/long is for that location'
    })
    object, created = get_or_create(session, Specificity, id=2, defaults={
        'description': 'event occurred in city/village/town and no lat/long could be found, so coordinates are for centroid of smallest subnational administrative region identified'
    })
    object, created = get_or_create(session, Specificity, id=3, defaults={
        'description': 'event did not occur in city/village/town, so coordinates are for centroid of smallest subnational administrative region identified'
    })
    object, created = get_or_create(session, Specificity, id=4, defaults={
        'description': 'no 2nd order or smaller region could be identified, so coordinates are for center of 1st order administrative region'
    })
    object, created = get_or_create(session, Specificity, id=5, defaults={
        'description': 'no 1st order administrative region could be identified for the location of the attack, so latitude and longitude are unknown'
    })
    session.commit()