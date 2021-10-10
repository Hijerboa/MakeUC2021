from db.models import PropertyDamageExtent
from db.database_connection import initialize, create_session
from db.db_utils import get_or_create

def gen_prop_dam():
    initialize()
    session = create_session()
    object, created = get_or_create(session, PropertyDamageExtent, id=1, defaults={
        'description': 'Catastrophic (likely ≥ $1 billion)'
    })
    object, created = get_or_create(session, PropertyDamageExtent, id=2, defaults={
        'description': 'Major (likely ≥ $1 million but < $1 billion)'
    })
    object, created = get_or_create(session, PropertyDamageExtent, id=3, defaults={
        'description': 'Minor (likely < $1 million)'
    })
    object, created = get_or_create(session, PropertyDamageExtent, id=4, defaults={
        'description': 'Unknown'
    })
    session.commit()