from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()


def add_to_db(db_entry):
    """
    Safely add an entry to the database.

    :param db_entry: SQLAlchemy model instance to add to the database.
                     Must implement a `to_dict()` method for serialization.
    :return: Dictionary representation of the entry if successful, otherwise `None`.
    """
    try:
        # Add the entry to the session and commit the transaction
        db.session.add(db_entry)
        db.session.commit()
        return db_entry.to_dict()

    except SQLAlchemyError as e:
        # Roll back the session on error to maintain database consistency
        db.session.rollback()
        return None

    finally:
        # Close the session to release resources
        db.session.remove()
