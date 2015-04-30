# project/db_create.py - Sets up & creates the database

from views import db
from models import Task
from datetime import date



# create the database and the db table - initialize db schema
db.create_all()

# insert data
# db.session.add(Task("Visit the Museum", date(2015, 4, 12), 10, 1))
# db.session.add(Task("Go Shopping", date(2015, 4, 12), 10, 1))


# commit changes
db.session.commit()