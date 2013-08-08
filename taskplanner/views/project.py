from taskplanner import app
from taskplanner.model import (db,
                               User,
                               Task,
                               TaskNote,
                               TaskAttachment,
                               Project,
                               Role,
                               Client)
from taskplanner.helpers import (login_required,
                                 required_roles,
                                 get_client_select_group)
from taskplanner.forms import (LoginForm,
                               RoleForm,
                               UserForm,
                               EditUserForm,
                               DeleteUserForm,
                               ClientForm,
                               AddProjectForm,
                               EditProjectForm,
                               EditTaskForm,
                               AddTaskForm,
                               DeleteProjectForm)
from flask import (request,
                   session,
                   redirect,
                   url_for,
                   render_template,
                   flash,
                   abort)
from werkzeug import secure_filename
import datetime
import os

@app.route('/')
@app.route('/projects')
@login_required
@required_roles('reader')
def project_list():
    project_list = Project.query.all()
    return render_template("project/projects.html", project_list=project_list)

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
@required_roles('editor')
def add_project():
    error = None
    form = AddProjectForm()
    form.client.choices = get_client_select_group()
    if form.validate_on_submit():
        p = Project()
        p.title = form.title.data
        p.description = form.description.data
        p.client_id = form.client.data
        p.start_date = form.start_date.data
        if form.due_date.data:
            p.due_date = form.due_date.data
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('project_list'))
    return render_template("project/addproject.html", error=error, form=form)

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
@required_roles('editor')
def edit_project(project_id):
    error = None
    theProj = Project.query.get_or_404(project_id)
    form = EditProjectForm(obj=theProj)
    form.client.choices = get_client_select_group()
    if request.method == 'GET':
        form.client.data = theProj.client_id
    if form.validate_on_submit():
        theProj.start_date = form.start_date.data
        theProj.description = form.description.data
        theProj.due_date = form.due_date.data
        theProj.title = form.title.data
        theProj.percent_complete = form.percent_complete.data
        theProj.client_id = form.client.data
        msg = "{0} updated!".format(theProj.title)
        flash(msg)
        db.session.commit()
        return redirect(url_for('project_view', project_id=theProj.id))
    return render_template("project/editproject.html", form=form, theProj=theProj)

@app.route('/delete_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
@required_roles('editor')
def delete_project(project_id):
    theProj = Project.query.get_or_404(project_id)
    form = DeleteProjectForm()
    if form.validate_on_submit():
        if form.delete.data:
            db.session.delete(theProj)
            msg = "{0} deleted".format(theProj.title)
            flash(msg)
            db.session.commit()
            return redirect(url_for('project_list'))
        else:
            msg = "{0} not delted".format(theProj.title)
            return redirect(url_for('project_view', project_id=theProj.id))
    return render_template("project/deleteproject.html", form=form, theProj = theProj)

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
@required_roles('editor')
def add_task():
    error = None
    form = AddTaskForm()
    form.project.choices = [(x.id, x.title) for x in Project.query.order_by('title')]
    form.owner.choices = [(x.id, x.fullname) for x in User.query.order_by('lname')]
    if request.method == 'GET' and request.args.get('project_id'):
        Project.query.get_or_404(request.args.get('project_id'))
        form.project.data = int(request.args.get('project_id'))
    if form.validate_on_submit():
        theTask = Task()
        theTask.project_id = form.project.data
        theTask.title = form.title.data
        theTask.description = form.description.data
        theTask.owner = User.query.get_or_404(form.owner.data)
        theTask.start_date = form.start_date.data
        theTask.percent_complete = form.percent_complete.data
        theTask.due_date = form.due_date.data
        if form.attachment.data:
            filename = form.attachment.data.filename
            if filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
                safeFN = secure_filename(form.attachment.data.filename)
                form.attachment.data.save(os.path.join(app.config['UPLOAD_FOLDER'], safeFN))
                ta = TaskAttachment()
                ta.filename = safeFN
                theTask.attachments.append(ta)
            else:
                error = "Not a valid file"
        if not error:
            db.session.add(theTask)
            db.session.commit()
            return redirect(url_for('project_view', project_id=theTask.project_id))
    return render_template("project/addtask.html", error=error, form=form)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
@required_roles('editor')
def edit_task(task_id):
    error = None
    theTask = Task.query.get_or_404(task_id)
    form = EditTaskForm(obj=theTask)
    form.project.choices = [(x.id, x.title) for x in Project.query.order_by('title')]
    form.owner.choices = [(x.id, x.fullname) for x in User.query.order_by('lname')]
    if request.method == 'GET':
        form.project.data = theTask.project_id
        form.owner.data = theTask.owner_id
    if form.validate_on_submit():
        theTask.project_id = form.project.data
        theTask.title = form.title.data
        theTask.description = form.description.data
        theTask.owner = User.query.get_or_404(form.owner.data)
        theTask.start_date = form.start_date.data
        theTask.percent_complete = form.percent_complete.data
        if theTask.percent_complete == 100:
            theTask.complete_date = datetime.date.today()
        else:
            theTask.complete_date = None
        theTask.due_date = form.due_date.data
        if form.task_note.data:
            tn = TaskNote()
            tn.description = form.task_note.data
            theTask.notes.append(tn)
        db.session.commit()
        return redirect(url_for('project_view', project_id=theTask.project_id))
    return render_template("project/edittask.html", error=error, theTask=theTask, form=form)

@app.route('/task_view/<int:task_id>')
@login_required
@required_roles('reader')
def task_view(task_id):
    theTask = Task.query.get_or_404(task_id)
    return render_template("project/taskview.html", theTask=theTask)

@app.route('/tasks')
@login_required
@required_roles('reader')
def tasks():
    pageStr = request.args.get('page', '1')
    page = int(pageStr)
    tasks = Task.query.order_by(Task.start_date).paginate(page, 20)
    return render_template("project/tasks.html", tasks=tasks)

# @app.route('/active_tasks')
# @login_required
# @required_roles('reader')
# def active_tasks():
#     pageStr = request.args.get('page', '1')
#     page = int(pageStr)
#     tasks = Task.query.filter(Task.complete_date == None).order_by(Task.start_date).paginate(page, 2)
#     return render_template("project/activetasks.html", tasks=tasks)

@app.route('/project/<int:project_id>')
@login_required
@required_roles('reader')
def project_view(project_id):
    theProject = Project.query.get_or_404(project_id)
    return render_template("project/project.html", theProject=theProject)

@app.route('/add_client', methods=['GET', 'POST'])
@login_required
@required_roles('editor')
def add_client():
    error = None
    form = ClientForm()
    theSource = request.args.get('source', None)
    if theSource:
        session['add_client_redirect'] = theSource
    theProject = request.args.get('project_id', None)
    if theProject:
        session['add_client_project_id'] = theProject
    if form.validate_on_submit():
        if Client.query.filter_by(email=form.email.data).count() > 0:
            error = "That client already exists"
        else:
            client = Client()
            client.name = form.name.data
            client.email = form.email.data
            client.company = form.company.data
            db.session.add(client)
            db.session.commit()
            msg = "{0} added as a client".format(client.name)
            flash(msg)
            theRedir = session.pop('add_client_redirect', None)
            if theRedir == 'add_project':
                return redirect(url_for(theRedir))
            elif theRedir == 'edit_project':
                return redirect(url_for(theRedir, project_id=session.pop('add_client_project_id')))
            return redirect(url_for('project_list'))
    return render_template("project/addclient.html", error=error, form=form)
