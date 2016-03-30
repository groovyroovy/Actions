from actions import ActionManager, EmailAction
from flask import current_app
from database import db_session
from models import User

act_mgr = ActionManager(current_app, db_session)

msg = {
    'recipients': ('Reuven Koblick', 'reuven@koblick.com'),
    'bcc':'groovyroovy@gmail.com',
    'subject': 'Actions test',
    'body': {'text': 'This is a {{ adj }} test.', 'context': {'adj': 'bad'}} }

email_action = EmailAction('database', 'users', 'dirty', **msg)

rows = db_session.query(User).all()
email_action.load_params('users', 'first_name', 'id', rows)
act_mgr.register_db_event(email_action)

