from actions import ActionManager, EmailAction
from flask import current_app
from database import db_session

kw = {
    'recipient': ('Reuven Koblick', 'reuven@koblick.com'),
    'bcc':'groovyroovy@gmail.com',
    'subject': 'Actions test',
    'body': {'text': 'This is a test.', 'context': {}} }


act_mgr = ActionManager(current_app, db_session)


email_action = EmailAction('database', 'users', 'dirty', **kw)
email_action.verify_params = {'users': ['first_name', 'Rosalie'],}

act_mgr.register_db_event(email_action)


