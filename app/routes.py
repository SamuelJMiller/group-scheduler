from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from datetime import datetime
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreateEngagementForm, EmptyForm, EditProfileForm, UserSearchForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, UserEngagement, UserGroup, GroupEngagement, FriendRequest

@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)

@app.route('/newevent', methods=['GET', 'POST'])
@login_required
def newevent():
    form = CreateEngagementForm()
    if form.validate_on_submit():
        event = UserEngagement(
            user_id=current_user.id, description=form.description.data, weekday=form.weekday.data, month=form.month.data, day=form.day.data,
            time=form.time.data, am_pm=form.am_pm.data, is_published_mates=form.is_published_mates.data,
            is_published_groupies=form.is_published_groupies.data
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_eng.html', title='New Event', form=form)

@app.route('/event/<eventid>', methods=['GET', 'POST'])
@login_required
def edit_event(eventid):
    form = CreateEngagementForm()
    event = UserEngagement.query.filter_by(id=eventid).first()
    if form.validate_on_submit():
        event.weekday = form.weekday.data
        event.month = form.month.data
        event.day = form.day.data
        event.time = form.time.data
        event.am_pm = form.am_pm.data
        event.description = form.description.data
        event.is_published_mates = form.is_published_mates.data
        event.is_published_groupies = form.is_published_groupies.data

        db.session.commit()

        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.weekday.data = event.weekday
        form.month.data = event.month
        form.day.data = event.day
        form.time.data = event.time
        form.am_pm.data = event.am_pm
        form.description.data = event.description
        form.is_published_mates.data = event.is_published_mates
        form.is_published_groupies.data = event.is_published_groupies
    if current_user.id == event.user_id:
        return render_template('edit_eng.html', title='Edit Event', event_desc_title=event.description, form=form)
    else:
        return render_template('not_allowed.html', title='Restricted Access')

@app.route('/delete_event/<eventid>', methods=['GET'])
@login_required
def delete_event(eventid):
    event = UserEngagement.query.filter_by(id=eventid).first()
    if current_user.id == event.user_id:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted!')
        return redirect(url_for('index'))
    else:
        flash('You do not have permission to do that.')
        return redirect(url_for('index'))

@app.route('/user/<userid>')
@login_required
def user_profile(userid):
    form = EmptyForm()
    user = User.query.filter_by(id=userid).first()
    if user != current_user:
        return render_template('user.html', title='Profile - ' + user.username, user=user, form=form)
    else:
        return redirect(url_for('my_profile'))

@app.route('/my_profile')
@login_required
def my_profile():
    return render_template('my_profile.html', title='My Profile', me=current_user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Info updated!')
        return redirect(url_for('my_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/friends/list')
@login_required
def friends_list():
    return render_template('friends_list.html', title='Friends List')

@app.route('/friends/requests')
@login_required
def friend_requests():
    a_form = EmptyForm()
    d_form = EmptyForm()
    return render_template('friend_requests.html', title='Friend Requests', user=User, acc_form=a_form, dec_form=d_form)

@app.route('/friends/find', methods=['GET', 'POST'])
@login_required
def find_friends():
    form = UserSearchForm()
    search_query = ""
    if form.validate_on_submit():
        search_query += form.text.data
    return render_template('find_friends.html', title='Find Friends', form=form, search_query=search_query, User=User)

@app.route('/unfriend/<userid>', methods=['GET'])
@login_required
def unfriend(userid):
    target_user = User.query.filter_by(id=userid).first()
    current_user.remove_friend(target_user)
    db.session.commit()
    flash('Unfriended ' + target_user.username)
    return redirect(url_for('friends_list'))

@app.route('/add_friend/<userid>', methods=['POST'])
def add_friend(userid):
    FriendRequest.send_friend_request(current_user.id, userid)
    db.session.commit()
    return redirect(url_for('user_profile', userid=userid))

@app.route('/accept_friend/<userid>', methods=['POST'])
@login_required
def accept_friend(userid):
    user = User.query.filter_by(id=userid).first()
    old_request = FriendRequest.query.filter_by(sender_id=userid, receiver_id=current_user.id).first()
    form = EmptyForm()
    if form.validate_on_submit():
        current_user.add_friend(user)
        db.session.delete(old_request)
        db.session.commit()
        flash('You are now friends with ' + user.username + '!')
        return redirect(url_for('friends_list'))

@app.route('/decline_friend/<userid>', methods=['POST'])
@login_required
def decline_friend(userid):
    old_request = FriendRequest.query.filter_by(sender_id=userid, receiver_id=current_user.id).first()
    form = EmptyForm()
    if form.validate_on_submit():
        db.session.delete(old_request)
        db.session.commit()
        return redirect(url_for('friend_requests'))

@app.route('/my_groups/current')
@login_required
def my_groups():
    return render_template('my_current_groups.html', title='My Groups')

@app.route('/my_groups/find')
@login_required
def find_groups():
    return render_template('find_new_groups.html', title='Find Groups')

@app.route('/my_admin')
@login_required
def my_admin():
    return render_template('groups_i_run.html', title='My Admin')

@app.route('/group/<groupid>')
@login_required
def group_profile(groupid):
    group = UserGroup.query.filter_by(id=groupid).first()
    return render_template('group.html', title=group.group_name, group=group)

@app.route('/group/<groupid>/members')
@login_required
def group_members(groupid):
    group = UserGroup.query.filter_by(id=groupid).first()
    return render_template('group_members.html', title='Members - ' + group.group_name, group=group)