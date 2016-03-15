import flask
from exceptions import ValueError

from sqlalchemy import event
from sqlalchemy.engine import reflection

# db_session and db should be passed to ActionManager on initialization.
from database import db_session
from database import db


event_registry = {}


def db_event(session, stat, instances):
    """Dispatcher for database events
    """

    def event_scan(session_itr):
        """Scans the event objects (db table create/update/delete actions).
        """
        
        for obj in session_itr:
            import pdb
            pdb.set_trace()
            evt_name =  obj.__tablename__
            model_name = '%s%s' % (evt_cat, evt_name)
            specific = '%s:%s:%s' % (evt_cat, evt_name, evt_type)

            key_combo = set([evt_cat, model_name, specific])
            registey_keys = set(event_registry.keys())
            outcomes = list(key_combo & registry_keys)

            for kk in outcomes:
                actions = event_registry.get(kk, None)

                # Shouldn't happen possible keys were anded with registry entries.
                if not actions:  
                    continue

            for action in actions:
                if action.verify(obj, evt_type):
                    action.dispatch(obj, event_type=evt_type)
    
    evt_cat = 'database'

    if session.deleted:
        print session.deleted
        evt_type = 'deleted'
        event_scan(session.deleted)
    if session.new:
        print session.new
        evt_type = 'new'
        event_scan(session.deleted)        
    if session.dirty:
        print session.dirty
        evt_type = 'dirty'
        event_scan(session.dirty)





def db_rollback(session):
    print 'rolled back'


class ActionManager(object):
    """
    Instantiated upon app initialization. Store instance globally and use it to 
    register actions.
    """
    name = 'Action Manager'
    description = 'Base Action Manager'
    
    def __init__(self, session=None):

        self.session = session if session else db_session
        self.db = db

        event.listen(self.session, 'before_flush', db_event)

        event.listen(self.session, 'after_rollback', db_rollback)

        
    def register_db_event(self, action):
        """Registers an action's event.
        Wild cards are permitted for tablenames and event_types.
        """
        valid_categories = ['database']
        valid_tablenames = reflection.Inspector.from_engine(db.engine).get_table_names()
        valid_tablenames.append('*')
        valid_event_types = ['new', 'deleted', 'dirty', '*']

        # The registry is a flat dict by combining category and name.
        k = action.event_category
        if not k in valid_categories:
            raise ValueError, '%s is not a valid category %s' % \
                (k, str(valid_categories))
        if action.event_name:
            if action.event_name not in valid_tablenames:
                raise ValueError, '%s is not a valid tablename %s' % \
                    (action.event_name, str(valid_tablenames))
            k = k + ':' + action.event_name
        if action.event_type:
            if action.event_type not in valid_event_types:
                raise ValueError, '%s is not a valid event type %s, %s' % \
                    (action.event_type, k, str(valid_event_types))
            k = k + ':' + action.event_type

        event_registry.setdefault(k, []).append({'action':action})


    def unregister(self, action):
        return True


class Action(object):
    """Base class for actions.
    Events are database, cron, or application specified.
    For database events, names are the model name, and type is dirty, new, or deleted.
    """
    name = 'Action'
    description = 'Base Action class for database events.'
    
    def __init__(self, cat='database', name=None, event_type=None):
        self.event_category = cat if cat else ""
        self.event_name = name if cat and name else ""
        self.event_type = event_type if cat and name and event_type else ""
        

    def verify(self, obj, evt_type):
        """Validate event. 
        Returning  means the event is a don't care. 
        Otherwise, returning True (default)  validates the object.
        """
        return True


    def dispatch(self, obj, **kwargs):
        """Enqueue the object for a signal. 
        False return means nothing enqueued.
        """
        import pdb
        pdb.set_trace()
        return False

    def execute(self, obj, kwargs):
        "execute the action"
        return

