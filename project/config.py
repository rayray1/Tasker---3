# project/config.py - Holds apps settings & configuration global variables

import os

# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))


DATABASE = 'flasktaskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True # for cross-site request forgery prevention(makes app more secure)
SECRET_KEY = 'random_key_gen' # used with CSRF to create a cryptographic token used to validate a form



# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)
