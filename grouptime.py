from app import app, db
from app.models import User, UserEngagement, UserGroup, GroupEngagement

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'UserEngagement': UserEngagement,
            'UserGroup': UserGroup, 'GroupEngagement': GroupEngagement,
            'sam': User.query.filter_by(username='sam').first(),
            'logan': User.query.filter_by(username='logan').first(),
            'group': UserGroup.query.first()}