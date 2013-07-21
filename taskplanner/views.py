from taskplanner import app
from taskplanner.model import (db,
                               User,
                               Task,
                               Project,
                               Role,
                               Client)
from taskplanner.helpers import (login_required,
                                 required_roles)
from taskplanner.forms import (LoginForm,
                               RoleForm,
                               UserForm,
                               EditUserForm,
                               DeleteUserForm,
                               ClientForm,
                               AddProjectForm)
from flask import (request,
                   session,
                   redirect,
                   url_for,
                   render_template,
                   flash,
                   abort)

@app.route('/')
@app.route('/projects')
@login_required
@required_roles('reader')
def project_list():
    project_list = Project.query.all()
    return render_template("projects.html", project_list=project_list)

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
@required_roles('editor')
def add_project():
    error = None
    form = AddProjectForm()
    form.client.choices = [(x.id, x.name) for x in Client.query.order_by('name')]
    if form.validate_on_submit():
        p = Project()
        p.title = form.title.data
        p.description = form.description.data
        p.client_id = form.client.data
        p.start_date = form.startdate.data
        if form.due_date.data:
            p.due_date = form.due_date.data
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('project_list'))
    return render_template("addproject.html", error=error, form=form)

#@app.route('/edit_project/<int:project_id>')
#@login_required
#@required_roles('editor')
#def edit_project(project_id):
#    error = None
#    theProj = Project.query.get_or_404(project_id)
    
@app.route('/project/<int:project_id>')
@login_required
@required_roles('reader')
def project_view(project_id):
    theProject = Project.query.get_or_404(project_id)
    return render_template("project.html", theProject=theProject)

@app.route('/add_client', methods=['GET', 'POST'])
@login_required
@required_roles('editor')
def add_client():
    error = None
    form = ClientForm()
    theSource = request.args.get('source', None)
    if theSource:
        session['add_client_redirect'] = theSource
    if form.validate_on_submit():
        client = Client()
        client.name = form.name.data
        client.email = form.email.data
        client.company = form.company.data
        db.session.add(client)
        db.session.commit()
        msg = "{0} added as a client".format(client.name)
        flash(msg)
        theRedir = session.pop('add_client_redirect', None)
        if theRedir:
            return redirect(url_for(theRedir))
        return redirect(url_for('project_list'))
    return render_template("addclient.html", error=error, form=form)

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
@required_roles('admin')
def add_user():
    error = None
    form = UserForm()
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
            db.session.add(user)
            db.session.commit()
            msg = "{0} added".format(user.fullname)
            flash(msg)
            return redirect(url_for('users'))
    return render_template("admin/adduser.html", error=error, form=form)

@app.route('/edit_user/<username>', methods=['GET', 'POST'])
@login_required
@required_roles('admin')
def edit_user(username):
    error = None
    user = User.query.filter_by(username=username).first() or abort(404)
    form = EditUserForm(obj=user)
    form.roles.choices =  [(x.name, x.name) for x in Role.query.order_by('name')]
    if request.method == 'GET':
        form.roles.data = [x.name for x in user.roles]  
    if form.validate_on_submit():
        edited = False
        if user.fname <> form.fname.data:
            edited = True
            user.fname = form.fname.data
        if user.lname <> form.lname.data:
            edited = True
            user.lname = form.lname.data
        if user.email <> form.email.data:
            edited = True
            user.email = form.email.data
        uroles = [x.name for x in user.roles]
        if uroles <> form.roles.data:
            edited = True
            user.roles = []
            for role in form.roles.data:
                theRole = Role.query.filter_by(name=role).one()
                user.roles.append(theRole)
        if form.password.data:
            edited = True
            user.set_password(form.password.data)
        if edited:
            db.session.commit()
            msg = "{0} updated".format(user.fullname)
            flash(msg)
            return redirect(url_for('users'))
        else:
            flash("No data was updated")
    return render_template("admin/edituser.html", error=error, username=username, form=form)

@app.route('/delete_user/<username>', methods=['GET', 'POST'])
@login_required
@required_roles('admin')
def delete_user(username):
    form = DeleteUserForm()
    user = User.query.filter_by(username=username).first() or abort(404)
    if form.validate_on_submit():
        if form.delete.data:
            db.session.delete(user)
            msg = "{0} deleted".format(user.fullname)
            db.session.commit()
        else:
            msg = "{0} not deleted".format(user.fullname)
        flash(msg)
        return redirect(url_for('users'))
    return render_template("admin/deleteuser.html", form=form, user=user)

@app.route('/users')
@login_required
@required_roles('admin')
def users():
    users = User.query.order_by('lname')
    return render_template("admin/users.html", users=users)

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
                return redirect(url_for('project_list'))
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
