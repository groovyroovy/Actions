try:
    # only works in debug mode
    from flask_debugtoolbar import DebugToolbarExtension

    toolbar = DebugToolbarExtension()
except ImportError:
    print('debugtoolbar extension not available.')
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()



