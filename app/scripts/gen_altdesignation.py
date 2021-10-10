from db.models import AlternativeDesignation
from db.database_connection import initialize, create_session
from db.db_utils import get_or_create

def gen_alt():
    initialize()
    session = create_session()
    object, created = get_or_create(session, AlternativeDesignation, id=1, defaults={
        'description': 'Insurgency/Guerilla Action'
    })
    object, created = get_or_create(session, AlternativeDesignation, id=2, defaults={
        'description': 'Other Crime Type'
    })
    object, created = get_or_create(session, AlternativeDesignation, id=3, defaults={
        'description':  'Inter/Intra-Group Conflic'
    })
    object, created = get_or_create(session, AlternativeDesignation, id=4, defaults={
        'description': 'Lack of Intentionality'
    })
    object, created = get_or_create(session, AlternativeDesignation, id=5, defaults={
        'description': 'State Actors'
    })
    session.commit()