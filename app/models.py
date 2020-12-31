from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db, login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

friends = db.Table('friends',
    db.Column('friender_id', db.Integer, db.ForeignKey('user.id')), #Gotta have your commas
    db.Column('friended_id', db.Integer, db.ForeignKey('user.id'))
)

group_members = db.Table('group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('user_group.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    engagements = db.relationship('UserEngagement', backref='scheduler', lazy='dynamic')
    groups_is_managing = db.relationship('UserGroup', backref='admin', lazy='dynamic')
    friend_requests = db.relationship('FriendRequest', backref='receiver', lazy='dynamic')

    user_friends = db.relationship(
        'User', secondary=friends,
        primaryjoin=(friends.c.friender_id == id),
        secondaryjoin=(friends.c.friended_id == id),
        backref=db.backref('friends', lazy='dynamic'), lazy='dynamic'
    )

    def add_friend(self, user):
        if not self.is_friends_with(user):
            self.user_friends.append(user)
            user.user_friends.append(self)

    def remove_friend(self, user):
        if self.is_friends_with(user):
            self.user_friends.remove(user)
            user.user_friends.remove(self)

    def is_friends_with(self, user):
        return self.user_friends.filter(friends.c.friended_id == user.id).count() > 0

    def in_group(self, group):
        return self.groups.filter(group_members.c.group_id == group.id).count() > 0

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def send_friend_request(sender, receiver):
        fr = FriendRequest(sender_id=sender, receiver_id=receiver)
        db.session.add(fr)

class UserEngagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(100), default='Unavailable')
    weekday = db.Column(db.String(20))
    month = db.Column(db.String(20))
    day = db.Column(db.String(10))
    time = db.Column(db.String(20))
    am_pm = db.Column(db.String(2))
    is_published_mates = db.Column(db.Boolean, default=False)
    is_published_groupies = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return 'Engagement number {} takes place on {}, {} {} at {} {} and is described as: {}'.format(
            self.id, self.weekday, self.month, self.day, self.time, self.am_pm, self.description
        )

class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), index=True, unique=True)
    group_admin = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_desc = db.Column(db.String(128), default='')

    engagements = db.relationship('GroupEngagement', backref='scheduler', lazy='dynamic')

    members = db.relationship('User', secondary=group_members, backref=db.backref('groups', lazy='dynamic'), lazy='dynamic')

    def add_member(self, user):
        if not user.in_group(self):
            self.members.append(user)

    def remove_member(self, user):
        if user.in_group(self):
            self.members.remove(user)

    def __repr__(self):
        return 'Group {} is administered by {}, and is described as: {}'.format(
            self.group_name, self.group_admin, self.group_desc
        )

class GroupEngagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'))
    description = db.Column(db.String(100), default='Group Activity')
    weekday = db.Column(db.String(20))
    month = db.Column(db.String(20))
    day = db.Column(db.Integer)
    time = db.Column(db.String(20))
    am_pm = db.Column(db.String(2))

    def __repr__(self):
        return 'Group number {} has an engagement on {}, {} {} at {} {} which is scheduled by {} and is described as: {}'.format(
            self.group_id, self.weekday, self.month, self.day, self.time, self.am_pm, self.scheduler.group_name, self.description
        )