from taskplanner import app
from taskplanner.model import db, User, Task, Project
from taskplanner.helpers import login_required, in_role
from flask import request, session, redirect, url_for, render_template, flash

@app.route('/')
@login_required
def taskplanner_home():
    return "Hello World!"

@app.route("/admin/")
@login_required
@in_role('admin')
def adminview():
    return render_template("admin/admin.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        theUser = User.query.filter_by(username=request.form['username']).\
                first()
        if not theUser:
            error = 'Invalid username'
        elif not theUser.check_password(request.form['password']):
            error = 'Invalid password'
        else:
            session['user'] = theUser.username
            flash('You were logged in')
            if session.get('next'):
                return redirect(session.pop('next'))
            else:
                return redirect(url_for('taskplanner_home'))
    else:
        # check for next url
        if request.args.get('next'):
            session['next'] = request.args.get('next')
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('login'))
