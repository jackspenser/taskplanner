from taskplanner import app
from taskplanner.model import db, User, Task, Project, Role
from taskplanner.helpers import login_required, required_roles
from taskplanner.forms import LoginForm, RoleForm, UserForm
from flask import request, session, redirect, url_for, render_template, flash

@app.route('/')
@login_required
@required_roles('reader')
def taskplanner_home():
    return "Hello World!"

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
@required_roles('admin')
def add_user():
    error = None
    form = UserForm(request.form)
    form.roles.choices = [(x.name, x.name) for x in Role.query.order_by('name')]
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count() > 0:
            error = "User already exists"
        else:
            user = User(form.username.data, form.password.data)
            user.fname = form.fname.data
            user.lname = form.lname.data
            user.email = form.email.data
            for role in form.roles.data:
                theRole = Role.query.filter_by(name=role).one()
                user.roles.append(theRole)            
            raise Exception('Stop')
    return render_template("admin/adduser.html", error=error, form=form)


@app.route("/admin/")
@login_required
@required_roles('admin')
def adminview():
    return render_template("admin/admin.html")

@app.route("/add_role", methods=['GET', 'POST'])
@login_required
@required_roles('admin')
def add_role():
    error = None
    form = RoleForm(request.form)
    theRoles = Role.query.all()
    if form.validate_on_submit():
        if Role.query.filter_by(name=form.name.data).count() > 0:
            error = "%s role already exists" % form.name.data
        else:
            role = Role(form.name.data)
            db.session.add(role)
            db.session.commit()
            flash("%s role added", role.name)
            return redirect(url_for('adminview'))
    return render_template("admin/addrole.html", roles = theRoles, form=form, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if form.validate_on_submit():
        theUser = User.query.filter_by(username=form.username.data).first()
        if not theUser:
            error = 'Invalid username'
        elif not theUser.check_password(form.password.data):
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
    return render_template('login.html', error=error, form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('login'))
